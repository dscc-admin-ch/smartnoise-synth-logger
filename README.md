# smartnoise_synth_logger
Logger for Smartnoise Synth Transformers
¨
# DiffPrivLib Logger

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![ci tests](https://github.com/dscc-admin-ch/diffprivlib-logger/actions/workflows/tests.yml/badge.svg)](https://github.com/dscc-admin-ch/diffprivlib-logger/actions/workflows/tests.yml?query=branch%3Amain)

Serialize and deserialize DiffPrivLib pipelines to and from JSON.

It is inspired from [opendp-logger](https://github.com/opendp/opendp-logger/tree/main) and a first version was made by [Oblivious](https://www.oblivious.com/) for the [UN PET Lab Hackathon 2022](https://petlab.officialstatistics.org/).

## Example

```python
from sklearn.pipeline import Pipeline
from diffprivlib import models

pipeline = Pipeline(
    [
        (
            "scaler",
            models.StandardScaler(
                bounds=([17, 1, 0, 0, 1], [90, 160, 10000, 4356, 99])
            ),
        ),
        ("pca", models.PCA(2, data_norm=5, centered=True)),
        ("lr", models.LogisticRegression(data_norm=5)),
    ]
)
```

## Serialise
```python
from diffprivlib_logger import serialise_pipeline

serialised_pipeline = serialise_pipeline(pipeline)
```

## Deserialise
```python
from diffprivlib_logger import deserialise_pipeline

deserialised_pipeline = serialise_pipeline(serialised_pipeline)
```
