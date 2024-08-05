import inspect
import json

import snsynth


class SSynthConstraintsEncoder(json.JSONEncoder):
    """Overwrites JSON Encoder class to serialise SSynth constraints
    of transformers with a specific format.
    """

    def default(self, o: dict):
        """Extends JSON encoder to SmartnoiseSynth class members"""
        types = [
            v[1] for v in inspect.getmembers(snsynth, inspect.isclass)
        ]
        if type(o) in types:
            return "_ssynth_instance:" + o.__class__.__name__
        return super().default(o)  # regular json encoding

    def encode(self, o: dict) -> str:
        """Define JSON string representation of a SmartnoiseSynth constraints"""

        def hint_tuples(item):
            if isinstance(item, tuple):
                return {"_tuple": True, "_items": item}
            if isinstance(item, list):
                return [hint_tuples(e) for e in item]
            if isinstance(item, dict):
                return {key: hint_tuples(value) for key, value in item.items()}
            return item

        return super().encode(hint_tuples(o))


def serialise_pipeline(constraints: dict):
    """Serialise the SmartnoiseSynth constraints to send it through FastAPI

    Args:
        constraints (dict): a SmartnoiseSynth TableTransformer constraints

    Raises:
        ValueError: If the input argument is not a SmartnoiseSynth constraint.

    Returns:
        serialised (str): SmartnoiseSynth pipeline as a serialised string
    """
    if not isinstance(dict, constraints):
        raise ValueError("Input constraints must be an instance of dict")

    json_body = {
        "module": "smartnoise_synth",
        "version": snsynth.__version__,
        "constraints": {},
    }

    for col_name, col_constraints in constraints.items():
        dict_params = vars(step_fn)
        params = list(inspect.signature(type(step_fn)).parameters)
        dict_params = {k: v for k, v in dict_params.items() if k in params}
        json_body["constraints"].append(
            {
                "type": "_ssynth_instance:" + step_fn.__class__.__name__,
                "name": col_name,
                "params": col_constraints,
            }
        )

    return json.dumps(json_body, cls=SSynthConstraintsEncoder)
