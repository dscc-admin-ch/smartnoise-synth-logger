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
from smartnoise_synth_logger import (
    deserialise_constraints,
    serialise_constraints,
)
from smartnoise_synth_logger.constants import SSYNTH


def test_anon_serialize():
    example_constraints = {"id": AnonymizationTransformer("uuid4")}
    result_json = serialise_constraints(example_constraints)

    expected_json = """{"module": "smartnoise-synth", "version": "1.0.4", "constraints": {"id": {"type": "_ssynth_transformer:AnonymizationTransformer", "params": {"fake": "uuid4"}}}}"""  # noqa
    expected_json_updated = expected_json.replace(
        "1.0.4", pkg_resources.get_distribution(SSYNTH).version
    )
    assert result_json == expected_json_updated


def test_anon_str_serialize():
    example_constraints = {"id": "email"}
    result_json = serialise_constraints(example_constraints)

    expected_json = """{"module": "smartnoise-synth", "version": "1.0.4", "constraints": {"id": "email"}}"""  # noqa
    expected_json_updated = expected_json.replace(
        "1.0.4", pkg_resources.get_distribution(SSYNTH).version
    )
    assert result_json == expected_json_updated


def test_chain_serialize():
    example_constraints = {
        "income": ChainTransformer(
            [
                LogTransformer(),
                BinTransformer(bins=20, lower=0, upper=50),
            ]
        ),
    }
    result_json = serialise_constraints(example_constraints)

    expected_json = """{"module": "smartnoise-synth", "version": "1.0.4", "constraints": {"income": {"type": "_ssynth_transformer:ChainTransformer", "params": [{"type": "_ssynth_transformer:LogTransformer", "params": {}}, {"type": "_ssynth_transformer:BinTransformer", "params": {"lower": 0, "upper": 50, "epsilon": 0.0, "bins": 20, "nullable": false, "odometer": null}}]}}}"""  # noqa
    expected_json_updated = expected_json.replace(
        "1.0.4", pkg_resources.get_distribution(SSYNTH).version
    )
    assert result_json == expected_json_updated


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

    expected_json = """{"module": "smartnoise-synth", "version": "1.0.4", "constraints": {"id": {"type": "_ssynth_transformer:AnonymizationTransformer", "params": {"fake": "email"}}, "income": {"type": "_ssynth_transformer:ChainTransformer", "params": [{"type": "_ssynth_transformer:LogTransformer", "params": {}}, {"type": "_ssynth_transformer:BinTransformer", "params": {"lower": 0, "upper": 50, "epsilon": 0.0, "bins": 20, "nullable": false, "odometer": null}}]}, "height": {"type": "_ssynth_transformer:ChainTransformer", "params": [{"type": "_ssynth_transformer:StandardScaler", "params": {"lower": 0, "upper": 1, "epsilon": 0.0, "nullable": false, "odometer": null}}, {"type": "_ssynth_transformer:BinTransformer", "params": {"lower": 0, "upper": 1, "epsilon": 0.0, "bins": 20, "nullable": false, "odometer": null}}]}, "weight": {"type": "_ssynth_transformer:ChainTransformer", "params": [{"type": "_ssynth_transformer:ClampTransformer", "params": {"upper": 200, "lower": 10}}, {"type": "_ssynth_transformer:BinTransformer", "params": {"lower": null, "upper": null, "epsilon": 0.0, "bins": 20, "nullable": false, "odometer": null}}]}, "age": {"type": "_ssynth_transformer:MinMaxTransformer", "params": {"lower": 0, "upper": 100, "epsilon": 0.0, "negative": true, "nullable": false, "odometer": null}}, "sex": {"type": "_ssynth_transformer:ChainTransformer", "params": [{"type": "_ssynth_transformer:LabelTransformer", "params": {"nullable": true}}, {"type": "_ssynth_transformer:OneHotEncoder", "params": {}}]}, "rank": {"type": "_ssynth_transformer:LabelTransformer", "params": {"nullable": false}}, "job": {"type": "_ssynth_transformer:DropTransformer", "params": {}}}}"""  # noqa
    expected_json_updated = expected_json.replace(
        "1.0.4", pkg_resources.get_distribution(SSYNTH).version
    )
    assert result_json == expected_json_updated


def test_anon_serialize_deserialise():
    example_constraints = {
        "id": AnonymizationTransformer("ssn"),
    }
    serialised = serialise_constraints(example_constraints)
    deserialised = deserialise_constraints(serialised)

    for (e_k, e_v), (de_k, de_v) in zip(
        example_constraints.items(), deserialised.items()
    ):
        assert e_k == de_k
        assert e_v.__class__.__name__ == de_v.__class__.__name__


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

    for (e_k, e_v), (de_k, de_v) in zip(
        example_constraints.items(), deserialised.items()
    ):
        assert e_k == de_k
        assert e_v.__class__.__name__ == de_v.__class__.__name__
        for attr in dir(e_v):
            if not attr.startswith("__"):
                e_attr = getattr(e_v, attr)
                de_attr = getattr(de_v, attr)

                if isinstance(e_attr, (int, float, str, bool, type(None))):
                    assert e_attr == de_attr, f"Mismatch in attribute: {attr}"
                else:
                    assert (
                        e_attr.__class__ == de_attr.__class__
                    ), f"Different types for attribute: {attr}"
