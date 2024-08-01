#  Copyright (c) 2024. David Boetius
#  Licensed under the MIT License
import argparse
from collections import defaultdict
from pathlib import Path

import pandas as pd

from python.verifair.benchmarks.fairsquare.models import _MODELS, _DISTS


def parse_case_name(line):
    model, distr, is_qual = line.split(",")
    _, model = model.split(":")
    _, distr = distr.split(":")
    _, is_qual = is_qual.split(":")
    model = _MODELS[model.strip()]
    distr = _DISTS[distr.strip()]
    return model, distr, is_qual.strip() == "True"


def read_until(line_prefix):
    line = next(file_iter)
    while not line.startswith(line_prefix):
        line = next(file_iter)
    return line


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Collect FairSquare Experiment Results",
        description="Summaries log files of several runs of the FairSquare experiment.",
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="Path to a directory containing one or several log files of the "
        "FairSquare experiment.",
    )
    args = parser.parse_args()

    log_files = [
        p for p in args.output_dir.iterdir() if p.is_file() and p.suffix != ".csv"
    ]
    data = defaultdict(list)
    for i, log_file in enumerate(log_files):
        with open(log_file, "rt") as file:
            file_iter = iter(file)
            try:
                while True:
                    model, distr, is_qual = parse_case_name(
                        read_until("Running model:")
                    )
                    line = read_until("Is fair:")
                    is_fair = line.split(":")[1].strip() == "1"
                    line = read_until("Is ambiguous:")
                    is_ambiguous = line.split(":")[1].strip() == "1"
                    line = read_until("Running time:")
                    runtime = float(line.split(":")[1].strip().split(" ")[0].strip())
                    if not is_fair or is_ambiguous:
                        print(i, model, distr, is_qual, runtime)
                    data[(model, distr, is_qual)].append(
                        pd.Series(
                            [is_fair, is_ambiguous, runtime],
                            index=pd.MultiIndex.from_tuples(
                                [
                                    (i, "Fair"),
                                    (i, "Ambiguous"),
                                    (i, "Runtime"),
                                ]
                            ),
                        )
                    )
            except StopIteration:
                pass
    table = []
    for key, values in data.items():
        table.append(
            pd.concat(
                [
                    pd.Series(
                        key,
                        index=pd.MultiIndex.from_tuples(
                            [("", "Model"), ("", "Distribution"), ("", "Qualified")]
                        ),
                    ),
                    *values,
                ],
            )
        )
    table = pd.DataFrame(table)
    runtimes = [table[(i, "Runtime")] for i in range(len(log_files))]
    runtimes = pd.DataFrame(runtimes).transpose()
    min_runtime = runtimes.min(axis=1)
    max_runtime = runtimes.max(axis=1)
    median_runtime = runtimes.median(axis=1)
    mean_runtime = runtimes.mean(axis=1)
    summary = pd.concat(
        [min_runtime, median_runtime, mean_runtime, max_runtime], axis=1
    )
    summary.columns = pd.MultiIndex.from_tuples(
        [
            ("", "MinRuntime"),
            ("", "MedianRuntime"),
            ("", "MeanRuntime"),
            ("", "MaxRuntime"),
        ]
    )
    table = pd.concat([table, summary], axis=1)
    print(table)

    # collapse multi-index
    table.columns = table.columns.to_series().apply(
        lambda vals: " ".join([str(v) for v in reversed(vals)])
        .strip()
        .replace(" ", "_")
    )
    table.to_csv(args.output_dir / "results.csv", index=False)

    # Runtimes table
    runtimes = table[
        ["MinRuntime", "MedianRuntime", "MeanRuntime", "MaxRuntime"]
    ].copy()
    runtimes["Nr"] = range(1, len(table) + 1)
    runtimes.to_csv(args.output_dir / "runtimes.csv", index=False)
