# Smartnoise Synth Logger
Logger for Smartnoise Synth Transformers


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![ci tests](https://github.com/dscc-admin-ch/smartnoise-synth-logger/actions/workflows/tests.yml/badge.svg)](https://github.com/dscc-admin-ch/smartnoise-synth-logger/actions/workflows/tests.yml?query=branch%3Amain)

Serialize and deserialize Smartnoise Synth constraints to and from JSON.

## Installation
Install with pip:
```python
pip install smartnoise-synth-logger
```

## Example

```python
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

constraints = {
    "id": AnonymizationTransformer("uuid4"),
    "email": "email", # also possible
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
}
```

## Serialise
```python
from smartnoise_synth_logger import serialise_constraints

serialised_constraints = serialise_constraints(constraints)
```

## Deserialise
```python
from smartnoise_synth_logger import deserialise_constraints

deserialised_constraints = deserialise_constraints(serialised_constraints)
```
