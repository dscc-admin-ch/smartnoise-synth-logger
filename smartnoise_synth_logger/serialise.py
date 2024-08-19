import inspect
import json

import pkg_resources
from smartnoise_synth_logger.constants import (
    ANON_PARAM,
    JsonBodyKey,
    SSYNTH,
    SSYNTH_DATETIME,
    SSYNTH_TRANSFORMER,
    Transformers,
)


def get_filtered_params(obj) -> dict:
    """Get filtered parameters based on the object's signature."""
    params = list(inspect.signature(type(obj)).parameters)
    return {k: v for k, v in vars(obj).items() if k in params}


def handle_chain_transformer(col_constraints: dict) -> dict:
    """Handle ChainTransformer-specific logic."""
    transformers_list = []
    for t in col_constraints.transformers:
        operator_name = t.__class__.__name__

        if operator_name == Transformers.DATETIME:
            transformer_dict = handle_datetime_transformer(t)
        else:
            transformer_dict = handle_default_transformer(t)

        transformers_list.append(transformer_dict)

    return {
        JsonBodyKey.TYPE: SSYNTH_TRANSFORMER + Transformers.CHAIN,
        JsonBodyKey.PARAM: transformers_list,
    }


def handle_datetime_transformer(col_constraints: dict) -> dict:
    """Handle DatetimeTransformer-specific logic."""
    operator_name = col_constraints.__class__.__name__
    datetime_params = get_filtered_params(col_constraints)
    datetime_params["epoch"] = datetime_params["epoch"].isoformat()
    return {
        JsonBodyKey.TYPE: SSYNTH_DATETIME + operator_name,
        JsonBodyKey.PARAM: datetime_params,
    }


def handle_anon_transformer(col_constraints: dict) -> dict:
    """Handle AnonymisationTransformer-specific logic."""
    operator_name = col_constraints.__class__.__name__
    return {
        JsonBodyKey.TYPE: SSYNTH_TRANSFORMER + operator_name,
        JsonBodyKey.PARAM: {ANON_PARAM: col_constraints.fake.__name__},
    }


def handle_default_transformer(col_constraints: dict) -> dict:
    """Handle default transformer logic."""
    operator_name = col_constraints.__class__.__name__
    return {
        JsonBodyKey.TYPE: SSYNTH_TRANSFORMER + operator_name,
        JsonBodyKey.PARAM: get_filtered_params(col_constraints),
    }


def serialise_constraints(constraints: dict) -> str:
    """Serialise the SmartnoiseSynth constraints to send it through FastAPI

    Args:
        constraints (dict): a SmartnoiseSynth TableTransformer constraints

    Raises:
        ValueError: If the input argument is not a SmartnoiseSynth constraint.

    Returns:
        serialised (str): SmartnoiseSynth constraints as a serialised string
    """
    if not isinstance(constraints, dict):
        raise ValueError("Input constraints must be an instance of dict")

    json_body = {
        JsonBodyKey.MODULE: SSYNTH,
        JsonBodyKey.VERSION: pkg_resources.get_distribution(SSYNTH).version,
        JsonBodyKey.CONSTRAINTS: {},
    }

    for col_name, col_constraints in constraints.items():
        if isinstance(col_constraints, str):
            json_body[JsonBodyKey.CONSTRAINTS][col_name] = col_constraints
        else:
            operator_name = col_constraints.__class__.__name__

            if operator_name == Transformers.CHAIN:
                transformer_dict = handle_chain_transformer(col_constraints)
            elif operator_name == Transformers.ANONIMIZATION:
                transformer_dict = handle_anon_transformer(col_constraints)
            elif operator_name == Transformers.DATETIME:
                transformer_dict = handle_datetime_transformer(col_constraints)
            else:
                transformer_dict = handle_default_transformer(col_constraints)

            json_body[JsonBodyKey.CONSTRAINTS][col_name] = transformer_dict

    return json.dumps(json_body)
