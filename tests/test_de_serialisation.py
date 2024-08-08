import snsynth
from snsynth.transform import ChainTransformer, LogTransformer, BinTransformer, MinMaxTransformer, AnonymizationTransformer, LabelTransformer, OneHotEncoder, StandardScaler, ClampTransformer, DropTransformer

from ssynth_logger import deserialise_constraints, serialise_constraints
from ssynth_logger.constants import SSYNTH, SSYNTH_INSTANCE, SSYNTH_TYPE

import pkg_resources


def test_serialize():
    example_constraints = {
        'id': AnonymizationTransformer("email"),
        'income':
            ChainTransformer([
                LogTransformer(),
                BinTransformer(bins=20, lower=0, upper=math.log(400_000))
            ]),
        'height':
            ChainTransformer([
                StandardScaler(lower = 0, upper = 1),
                BinTransformer(bins=20, lower=0, upper=1)
            ]),
        'weight':
            ChainTransformer([
                ClampTransformer(lower=10, upper = 200),
                BinTransformer(bins=20)
            ]),
        'age': MinMaxTransformer(lower=0, upper=100),
        'sex': ChainTransformer([
            LabelTransformer(nullable=True), 
            OneHotEncoder()
        ]),
        'rank': LabelTransformer(nullable=False),
        'job': DropTransformer()
        #'date': ChainTransformer([DateTimeTransformer(), MinMaxTransformer(nullable=False)])
    }
    result_json = serialise_constraints(example_constraints)

    expected_json == """'{"module": "smartnoise-synth", "version": "1.0.4", "constraints": {"id": {"type": "_ssynth_type:AnonymizationTransformer", "name": "AnonymizationTransformer", "params": "email"}, "income": {"type": "_ssynth_type:ChainTransformer", "name": "ChainTransformer", "params": [{"type": "_ssynth_type:LogTransformer", "name": "LogTransformer", "params": {}}, {"type": "_ssynth_type:BinTransformer", "name": "BinTransformer", "params": {"lower": 0, "upper": 12.89921982609012, "epsilon": 0.0, "bins": 20, "nullable": false, "odometer": null}}]}, "height": {"type": "_ssynth_type:ChainTransformer", "name": "ChainTransformer", "params": [{"type": "_ssynth_type:StandardScaler", "name": "StandardScaler", "params": {"lower": 0, "upper": 1, "epsilon": 0.0, "nullable": false, "odometer": null}}, {"type": "_ssynth_type:BinTransformer", "name": "BinTransformer", "params": {"lower": 0, "upper": 1, "epsilon": 0.0, "bins": 20, "nullable": false, "odometer": null}}]}, "weight": {"type": "_ssynth_type:ChainTransformer", "name": "ChainTransformer", "params": [{"type": "_ssynth_type:ClampTransformer", "name": "ClampTransformer", "params": {"upper": 200, "lower": 10}}, {"type": "_ssynth_type:BinTransformer", "name": "BinTransformer", "params": {"lower": null, "upper": null, "epsilon": 0.0, "bins": 20, "nullable": false, "odometer": null}}]}, "age": {"type": "_ssynth_type:MinMaxTransformer", "name": "MinMaxTransformer", "params": {"lower": 0, "upper": 100, "epsilon": 0.0, "negative": true, "nullable": false, "odometer": null}}, "sex": {"type": "_ssynth_type:ChainTransformer", "name": "ChainTransformer", "params": [{"type": "_ssynth_type:LabelTransformer", "name": "LabelTransformer", "params": {"nullable": true}}, {"type": "_ssynth_type:OneHotEncoder", "name": "OneHotEncoder", "params": {}}]}, "rank": {"type": "_ssynth_type:LabelTransformer", "name": "LabelTransformer", "params": {"nullable": false}}, "job": {"type": "_ssynth_type:DropTransformer", "name": "DropTransformer", "params": {}}}}'"""   # noqa
    assert result_json == expected_json_updated


def test_serialize_deserialise():
    example_constraints = {
        'id': AnonymizationTransformer("email"),
        'income':
            ChainTransformer([
                LogTransformer(),
                BinTransformer(bins=20, lower=0, upper=math.log(400_000))
            ]),
        'height':
            ChainTransformer([
                StandardScaler(lower = 0, upper = 1),
                BinTransformer(bins=20, lower=0, upper=1)
            ]),
        'weight':
            ChainTransformer([
                ClampTransformer(lower=10, upper = 200),
                BinTransformer(bins=20)
            ]),
        'age': MinMaxTransformer(lower=0, upper=100),
        'sex': ChainTransformer([
            LabelTransformer(nullable=True), 
            OneHotEncoder()
        ]),
        'rank': LabelTransformer(nullable=False),
        'job': DropTransformer()
        #'date': ChainTransformer([DateTimeTransformer(), MinMaxTransformer(nullable=False)])
    }
    serialised = serialise_pipeline(pipeline)
    deserialised = deserialise_pipeline(serialised)

    # for p_step, d_step in zip(pipeline.steps, deserialised.steps):
    #     # Same names
    #     assert p_step[0] == d_step[0]

    #     # Same values accountant
    #     p_step_dict = p_step[1].accountant.__dict__
    #     d_step_dict = d_step[1].accountant.__dict__
    #     assert p_step_dict == d_step_dict

    #     # Same other values
    #     p_step_dict = p_step[1].__dict__
    #     d_step_dict = d_step[1].__dict__
    #     del p_step_dict["accountant"]
    #     del d_step_dict["accountant"]
    #     assert p_step_dict == d_step_dict
