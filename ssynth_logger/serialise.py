import inspect
import json

import pkg_resources
from ssynth_logger.constants import SSYNTH, SSYNTH_TRANSFORMER


def get_filtered_params(obj) -> dict:
    """Get filtered parameters based on the object's signature."""
    params = list(inspect.signature(type(obj)).parameters)
    return {k: v for k, v in vars(obj).items() if k in params}


def handle_chain_transformer(col_constraints: dict) -> dict:
    """Handle ChainTransformer-specific logic."""
    transformers = col_constraints.transformers
    return {
        "type": SSYNTH_TRANSFORMER + "ChainTransformer",
        "params": [
            {
                "type": SSYNTH_TRANSFORMER + t.__class__.__name__,
                "params": get_filtered_params(t),
            }
            for t in transformers
        ],
    }


def handle_anonymization_transformer(col_constraints: dict) -> dict:
    """Handle AnonymizationTransformer-specific logic."""
    return {
        "type": SSYNTH_TRANSFORMER + "AnonymizationTransformer",
        "params": {"fake": col_constraints.fake.__name__},
    }


def handle_default_operator(col_constraints: dict) -> dict:
    """Handle default operator logic."""
    return {
        "type": SSYNTH_TRANSFORMER + col_constraints.__class__.__name__,
        "params": get_filtered_params(col_constraints),
    }


def serialise_constraints(constraints: dict) -> str:
    """Serialise the SmartnoiseSynth constraints to send it through FastAPI

    Args:
        constraints (dict): a SmartnoiseSynth TableTransformer constraints

    Raises:
        ValueError: If the input argument is not a SmartnoiseSynth constraint.

    Returns:
        serialised (str): SmartnoiseSynth pipeline as a serialised string
    """
    if not isinstance(constraints, dict):
        raise ValueError("Input constraints must be an instance of dict")

    json_body = {
        "module": SSYNTH,
        "version": pkg_resources.get_distribution(SSYNTH).version,
        "constraints": {},
    }

    for col_name, col_constraints in constraints.items():
        operator_name = col_constraints.__class__.__name__

        if operator_name == "ChainTransformer":
            transformer_dict = handle_chain_transformer(col_constraints)
        elif operator_name == "AnonymizationTransformer":
            transformer_dict = handle_anonymization_transformer(
                col_constraints
            )
        else:
            transformer_dict = handle_default_operator(col_constraints)

        json_body["constraints"][col_name] = transformer_dict

    return json.dumps(json_body)
