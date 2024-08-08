import inspect
import json
import pkg_resources

import snsynth
from ssynth_logger.constants import SSYNTH, SSYNTH_INSTANCE, SSYNTH_TYPE

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
            return SSYNTH_INSTANCE + o.__class__.__name__
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

def get_filtered_params(obj):
    """Get filtered parameters based on the object's signature."""
    params = list(inspect.signature(type(obj)).parameters)
    return {k: v for k, v in vars(obj).items() if k in params}

def handle_chain_transformer(col_name, col_constraints):
    """Handle ChainTransformer-specific logic."""
    transformers = col_constraints.transformers
    return {
        "type": SSYNTH_TYPE + "ChainTransformer",
        "name": "ChainTransformer",
        "params": [
            {
                "type": SSYNTH_TYPE + t.__class__.__name__,
                "name": t.__class__.__name__,
                "params": get_filtered_params(t),
            }
            for t in transformers
        ],
    }

def handle_anonymization_transformer(col_name, col_constraints):
    """Handle AnonymizationTransformer-specific logic."""
    faker_name = col_constraints.fake.__name__
    return {
        "type": SSYNTH_TYPE + "AnonymizationTransformer",
        "name": "AnonymizationTransformer",
        "params": faker_name,
    }

def handle_default_operator(col_name, col_constraints):
    """Handle default operator logic."""
    operator_name = col_constraints.__class__.__name__
    return {
        "type": SSYNTH_TYPE + operator_name,
        "name": operator_name,
        "params": get_filtered_params(col_constraints),
    }

def serialise_constraints(constraints: dict):
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
        "module": SSYNTH,
        "version": pkg_resources.get_distribution(SSYNTH).version,
        "constraints": {},
    }

    for col_name, col_constraints in constraints.items():
        operator_name = col_constraints.__class__.__name__
        
        if operator_name == "ChainTransformer":
            transformer_dict = handle_chain_transformer(col_name, col_constraints)
        elif operator_name == "AnonymizationTransformer":
            transformer_dict = handle_anonymization_transformer(col_name, col_constraints)
        else:
            transformer_dict = handle_default_operator(col_name, col_constraints)
        
        json_body["constraints"][col_name] = transformer_dict

    return json.dumps(json_body, cls=SSynthConstraintsEncoder)
