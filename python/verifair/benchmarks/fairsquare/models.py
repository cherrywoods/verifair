from .helper import *

from . import M_BN_F_DT_A_Q
from . import M_BN_F_DT_V2_D2_N16_Q
from . import M_BN_F_DT_V2_D2_N4_Q
from . import M_BN_F_DT_V2_D3_N14_Q
from . import M_BN_F_DT_V3_D2_N44_Q
from . import M_BN_F_NN_V2_H1_Q
from . import M_BN_F_NN_V2_H2_Q
from . import M_BN_F_NN_V3_H2_Q
from . import M_BN_F_SVM_A_Q
from . import M_BN_F_SVM_V3_Q
from . import M_BN_F_SVM_V4_Q
from . import M_BN_F_SVM_V5_Q
from . import M_BN_F_SVM_V6_Q

from . import M_BNc_F_DT_A_Q
from . import M_BNc_F_DT_V2_D2_N16_Q
from . import M_BNc_F_DT_V2_D2_N4_Q
from . import M_BNc_F_DT_V2_D3_N14_Q
from . import M_BNc_F_DT_V3_D2_N44_Q
from . import M_BNc_F_NN_V2_H1_Q
from . import M_BNc_F_NN_V2_H2_Q
from . import M_BNc_F_NN_V3_H2_Q
from . import M_BNc_F_SVM_A_Q
from . import M_BNc_F_SVM_V3_Q
from . import M_BNc_F_SVM_V4_Q
from . import M_BNc_F_SVM_V5_Q
from . import M_BNc_F_SVM_V6_Q

from . import M_ind_F_DT_A_Q
from . import M_ind_F_DT_V2_D2_N16_Q
from . import M_ind_F_DT_V2_D2_N4_Q
from . import M_ind_F_DT_V2_D3_N14_Q
from . import M_ind_F_DT_V3_D2_N44_Q
from . import M_ind_F_NN_V2_H1_Q
from . import M_ind_F_NN_V2_H2_Q
from . import M_ind_F_NN_V3_H2_Q
from . import M_ind_F_SVM_A_Q
from . import M_ind_F_SVM_V3_Q
from . import M_ind_F_SVM_V4_Q
from . import M_ind_F_SVM_V5_Q
from . import M_ind_F_SVM_V6_Q

from . import M_BN_F_NN_V2_H1
from . import M_BN_F_NN_V2_H2
from . import M_BN_F_NN_V3_H2

from . import M_BNc_F_NN_V2_H1
from . import M_BNc_F_NN_V2_H2
from . import M_BNc_F_NN_V3_H2

from . import M_ind_F_NN_V2_H1
from . import M_ind_F_NN_V2_H2
from . import M_ind_F_NN_V3_H2

_DISTS = {
    'dist0': 'ind',
    'dist1': 'BN',
    'dist2': 'BNc',
}

_MODELS = {
    'nn0': 'NN_V2_H1',
    'nn1': 'NN_V2_H2',
    'nn2': 'NN_V3_H2',
}

def all_dists():
    return _DISTS.keys()

def all_models():
    return _MODELS.keys()

def get_model_name(model, dist, is_qual):
    name = ''
    name += 'M_'
    name += _DISTS[dist]
    name += '_F_'
    name += _MODELS[model]
    if is_qual:
        name += '_Q'
    return name

def get_model(model, dist, is_qual):
    name = get_model_name(model, dist, is_qual)
    ldict = locals()
    exec('fn = {}.sample'.format(name))
    return ldict['fn']
