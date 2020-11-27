import pkgutil
from enum import Enum
import alpha.constants as constants

import alpha.constants as pmutil
import alpha.classic as alpha_classic
from alpha.dfg.pandas import get_dfg_graph, get_concurrent_events_dataframe, get_partial_order_dataframe


import alpha.converter as log_conversion
from util import exec_utils
from util import xes_constants as xes_util


class Variants(Enum):
    ALPHA_VERSION_CLASSIC = alpha_classic
    ALPHA_VERSION_PLUS = None


ALPHA_VERSION_CLASSIC = Variants.ALPHA_VERSION_CLASSIC
ALPHA_VERSION_PLUS = Variants.ALPHA_VERSION_PLUS
DEFAULT_VARIANT = ALPHA_VERSION_CLASSIC
VERSIONS = {Variants.ALPHA_VERSION_CLASSIC, Variants.ALPHA_VERSION_PLUS}


def apply(log, parameters=None, variant=DEFAULT_VARIANT):
    """
    Apply the Alpha Miner on top of a log

    Parameters
    -----------
    log
        Log
    variant
        Variant of the algorithm to use:
            - Variants.ALPHA_VERSION_CLASSIC
            ######### Not implemented in this version
            - Variants.ALPHA_VERSION_PLUS
    parameters
        Possible parameters of the algorithm, including:
            Parameters.ACTIVITY_KEY -> Name of the attribute that contains the activity

    Returns
    -----------
    net
        Petri net
    marking
        Initial marking
    final_marking
        Final marking
    """


    if parameters is None:
        parameters = {}
    case_id_glue = exec_utils.get_param_value(constants.PARAMETER_CONSTANT_CASEID_KEY, parameters, pmutil.CASE_CONCEPT_NAME)
    activity_key = exec_utils.get_param_value(constants.PARAMETER_CONSTANT_ACTIVITY_KEY, parameters, xes_util.DEFAULT_NAME_KEY)
    start_timestamp_key = exec_utils.get_param_value(constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY, parameters,
                                                     None)
    timestamp_key = exec_utils.get_param_value(constants.PARAMETER_CONSTANT_TIMESTAMP_KEY, parameters, xes_util.DEFAULT_TIMESTAMP_KEY)

    if pkgutil.find_loader("pandas"):
        import pandas
        if isinstance(log, pandas.core.frame.DataFrame) and variant == ALPHA_VERSION_CLASSIC:
            dfg = get_dfg_graph(log, case_id_glue=case_id_glue,
                                              activity_key=activity_key,
                                              timestamp_key=timestamp_key, start_timestamp_key=start_timestamp_key)
            return exec_utils.get_variant(variant).apply_dfg(dfg, parameters=parameters)
    return exec_utils.get_variant(variant).apply(log_conversion.apply(log, parameters, log_conversion.TO_EVENT_LOG),
                                                 parameters)


def apply_dfg(dfg, parameters=None, variant=ALPHA_VERSION_CLASSIC):
    """
    Apply Alpha Miner directly on top of a DFG graph

    Parameters
    -----------
    dfg
        Directly-Follows graph
    variant
        Variant of the algorithm to use (classic)
    parameters
        Possible parameters of the algorithm, including:
            activity key -> Name of the attribute that contains the activity

    Returns
    -----------
    net
        Petri net
    marking
        Initial marking
    final_marking
        Final marking
    """
    if parameters is None:
        parameters = {}
    return exec_utils.get_variant(variant).apply_dfg(dfg, parameters)
