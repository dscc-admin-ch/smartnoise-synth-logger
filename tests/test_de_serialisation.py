import pkg_resources
from snsynth.transform import (
    AnonymizationTransformer,
    BinTransformer,
    ChainTransformer,
    ClampTransformer,
    DropTransformer,
    LabelTransformer,
    LogTransformer,
    MinMaxTransformer,
    OneHotEncoder,
    StandardScaler,
)
from ssynth_logger import deserialise_constraints, serialise_constraints
from ssynth_logger.constants import SSYNTH


def test_serialize():
    example_constraints = {
        "id": AnonymizationTransformer("email"),
        "income": ChainTransformer(
            [
                LogTransformer(),
                BinTransformer(bins=20, lower=0, upper=50),
            ]
        ),
        "height": ChainTransformer(
            [
                StandardScaler(lower=0, upper=1),
                BinTransformer(bins=20, lower=0, upper=1),
            ]
        ),
        "weight": ChainTransformer(
            [ClampTransformer(lower=10, upper=200), BinTransformer(bins=20)]
        ),
        "age": MinMaxTransformer(lower=0, upper=100),
        "sex": ChainTransformer(
            [LabelTransformer(nullable=True), OneHotEncoder()]
        ),
        "rank": LabelTransformer(nullable=False),
        "job": DropTransformer(),
        # "date": ChainTransformer(
        #     [DateTimeTransformer(), MinMaxTransformer(nullable=False)]
        # ),
    }
    result_json = serialise_constraints(example_constraints)

    expected_json = """'{"module": "smartnoise-synth", "version": "1.0.4", "constraints": {"id": {"type": "_ssynth_type:AnonymizationTransformer", "name": "AnonymizationTransformer", "params": "email"}, "income": {"type": "_ssynth_type:ChainTransformer", "name": "ChainTransformer", "params": [{"type": "_ssynth_type:LogTransformer", "name": "LogTransformer", "params": {}}, {"type": "_ssynth_type:BinTransformer", "name": "BinTransformer", "params": {"lower": 0, "upper": 50, "epsilon": 0.0, "bins": 20, "nullable": false, "odometer": null}}]}, "height": {"type": "_ssynth_type:ChainTransformer", "name": "ChainTransformer", "params": [{"type": "_ssynth_type:StandardScaler", "name": "StandardScaler", "params": {"lower": 0, "upper": 1, "epsilon": 0.0, "nullable": false, "odometer": null}}, {"type": "_ssynth_type:BinTransformer", "name": "BinTransformer", "params": {"lower": 0, "upper": 1, "epsilon": 0.0, "bins": 20, "nullable": false, "odometer": null}}]}, "weight": {"type": "_ssynth_type:ChainTransformer", "name": "ChainTransformer", "params": [{"type": "_ssynth_type:ClampTransformer", "name": "ClampTransformer", "params": {"upper": 200, "lower": 10}}, {"type": "_ssynth_type:BinTransformer", "name": "BinTransformer", "params": {"lower": null, "upper": null, "epsilon": 0.0, "bins": 20, "nullable": false, "odometer": null}}]}, "age": {"type": "_ssynth_type:MinMaxTransformer", "name": "MinMaxTransformer", "params": {"lower": 0, "upper": 100, "epsilon": 0.0, "negative": true, "nullable": false, "odometer": null}}, "sex": {"type": "_ssynth_type:ChainTransformer", "name": "ChainTransformer", "params": [{"type": "_ssynth_type:LabelTransformer", "name": "LabelTransformer", "params": {"nullable": true}}, {"type": "_ssynth_type:OneHotEncoder", "name": "OneHotEncoder", "params": {}}]}, "rank": {"type": "_ssynth_type:LabelTransformer", "name": "LabelTransformer", "params": {"nullable": false}}, "job": {"type": "_ssynth_type:DropTransformer", "name": "DropTransformer", "params": {}}}}'"""  # noqa
    expected_json_updated = expected_json.replace(
        "1.0.4", pkg_resources.get_distribution(SSYNTH).version
    )
    assert result_json == expected_json_updated


def test_serialize_deserialise():
    example_constraints = {
        "id": AnonymizationTransformer("email"),
        "income": ChainTransformer(
            [
                LogTransformer(),
                BinTransformer(bins=20, lower=0, upper=20),
            ]
        ),
        "height": ChainTransformer(
            [
                StandardScaler(lower=0, upper=1),
                BinTransformer(bins=20, lower=0, upper=1),
            ]
        ),
        "weight": ChainTransformer(
            [ClampTransformer(lower=10, upper=200), BinTransformer(bins=20)]
        ),
        "age": MinMaxTransformer(lower=0, upper=100),
        "sex": ChainTransformer(
            [LabelTransformer(nullable=True), OneHotEncoder()]
        ),
        "rank": LabelTransformer(nullable=False),
        "job": DropTransformer(),
        # "date": ChainTransformer(
        #     [DateTimeTransformer(), MinMaxTransformer(nullable=False)]
        # ),
    }
    serialised = serialise_constraints(example_constraints)
    deserialised = deserialise_constraints(serialised)

    assert example_constraints == deserialised
