from enum import StrEnum

SSYNTH = "smartnoise-synth"
SSYNTH_TRANSFORMER = "_ssynth_transformer:"
SSYNTH_DATETIME = "_ssynth_datetime_transformer:"

ANON_PARAM = "fake"


class JsonBodyKey(StrEnum):
    """Keys for serialised JSON body"""

    MODULE = "module"
    VERSION = "version"
    CONSTRAINTS = "constraints"
    TYPE = "type"
    PARAM = "params"


class Transformers(StrEnum):
    """Transformer with a specific serialising behaviour"""

    CHAIN = "ChainTransformer"
    ANONIMIZATION = "AnonymizationTransformer"
    DATETIME = "DateTimeTransformer"
