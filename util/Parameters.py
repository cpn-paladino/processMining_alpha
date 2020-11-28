import util.xes_constants as xes_constants
import util.constants as constants
# 4 change from Enum to enumerate

class Parameters(enumerate):
    TIMESTAMP_SORT = False
    TIMESTAMP_KEY = xes_constants.DEFAULT_TIMESTAMP_KEY
    REVERSE_SORT = False
    INSERT_TRACE_INDICES = False
    MAX_TRACES = 1000000000
    ATTRIBUTE_KEY = constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY
    SINGLE = "single"
    BINARIZE = "binarize"
    POSITIVE = "positive"
    LOWER_PERCENT = "lower_percent"
