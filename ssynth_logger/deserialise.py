import json
from typing import Union
import pkg_resources

import snsynth
from ssynth_logger.constants import SSYNTH, SSYNTH_INSTANCE, SSYNTH_TYPE


class SSynthConstraintsDecoder(json.JSONDecoder):
    """Decoder for SSynth constraints from str to model"""

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs
        )

    def object_hook(
        self, dct: dict
    ) -> Union[tuple, dict]:  # pylint: disable=E0202
        """Hook for custom deserialisation of a SSynth constraints
        For every element, get the associated Transformer attribute.

        Args:
            dct (dict): decoded JSON object

        Raises:
            ValueError: If the serialised object is not compliant with
                        the expected format.

        Returns:
            dct (dict): value to used in place of the decoded JSON object (dct)
        """
        if "_tuple" in dct.keys():
            return tuple(dct["_items"])

        for k, v in dct.items():
            if isinstance(v, str):
                if v[:len(SSYNTH_TYPE)] == SSYNTH_TYPE:
                    try:
                        dct[k] = getattr(diffprivlib.models, v[len(SSYNTH_TYPE):])
                    except Exception as e:
                        raise ValueError(e) from e

                elif v[:len(SSYNTH_INSTANCE)] == SSYNTH_INSTANCE:
                    try:
                        dct[k] = getattr(snsynth, v[len(SSYNTH_INSTANCE):])()
                    except Exception as e:
                        raise ValueError(e) from e

        return dct


def deserialise_constraints(constraints_json: str) -> dict:
    """Deserialise a DiffPriLip pipeline from string to DiffPrivLib model
    Args:
        constraints_json (str): serialised DiffPrivLib pipeline

    Raises:
        ValueError: If the serialised object is not compliant with
                                    the expected format.

    Returns:
        constraints: DiffPrivLib pipeline
    """
    dct = json.loads(diffprivlib_json, cls=DiffPrivLibDecoder)
    if "module" in dct.keys():
        if dct["module"] != SSYNTH:
            raise ValueError(f"JSON 'module' not equal to '{SSYNTH}'")
    else:
        raise ValueError("Key 'module' not in submitted json request.")

    if "version" in dct.keys():
        if dct["version"] != pkg_resources.get_distribution(SSYNTH).version:
            raise ValueError(
                f"Requested version does not match available version:"
                f" {pkg_resources.get_distribution(SSYNTH).version}."
            )
    else:
        raise ValueError("Key 'version' not in submitted json request.")

    return Pipeline(
        [
            (val["name"], val["type"](**val["params"]))
            for val in dct["pipeline"]
        ]
    )
