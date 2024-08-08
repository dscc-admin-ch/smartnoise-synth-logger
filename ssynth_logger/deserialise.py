import json

import pkg_resources
import snsynth
from ssynth_logger.constants import SSYNTH, SSYNTH_TRANSFORMER


class SSynthDecoder(json.JSONDecoder):
    """Decoder for SSynth constraints from str to model"""

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs
        )

    def object_hook(self, dct: dict) -> dict:
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
        for k, v in dct.items():
            if isinstance(v, str):
                nb_letters = len(SSYNTH_TRANSFORMER)
                if v[:nb_letters] == SSYNTH_TRANSFORMER:
                    try:
                        dct[k] = getattr(
                            snsynth.transform, v[nb_letters:]  # noqa E203
                        )
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
    json_body = json.loads(constraints_json, cls=SSynthDecoder)
    if "module" in json_body.keys():
        if json_body["module"] != SSYNTH:
            raise ValueError(f"JSON 'module' not equal to '{SSYNTH}'")
    else:
        raise ValueError("Key 'module' not in submitted json request.")

    if "version" in json_body.keys():
        current_version = pkg_resources.get_distribution(SSYNTH).version
        if json_body["version"] != current_version:
            raise ValueError(
                f"Requested version does not match available version:"
                f" {current_version}."
            )
    else:
        raise ValueError("Key 'version' not in submitted json request.")

    deserialised = {}
    for key, val in json_body["constraints"].items():
        deserialised[key] = val['type'](**val['params'])

    return deserialised
