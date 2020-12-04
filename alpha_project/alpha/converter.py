from enum import Enum

from alpha import to_event_log


class Variants(Enum):
    TO_EVENT_LOG = to_event_log
    TO_EVENT_STREAM = None
    TO_DATA_FRAME = None


TO_EVENT_LOG = Variants.TO_EVENT_LOG
TO_EVENT_STREAM = Variants.TO_EVENT_STREAM
TO_DATA_FRAME = Variants.TO_DATA_FRAME


def apply(log, parameters=None, variant=Variants.TO_EVENT_LOG):
    return variant.value.apply(log, parameters=parameters)
