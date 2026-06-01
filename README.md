# T0 - ML/MLOps Engineering Internship Assessment

## Overview

This project implements a minimal MLOps-style batch job in Python.

Features:

* YAML-based configuration
* Deterministic execution using configurable random seed
* Dataset validation
* Rolling mean computation on close prices
* Binary signal generation
* Structured metrics output (JSON)
* Logging for observability
* Docker-ready deployment

---

## Project Structure

```text
.
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── metrics.json
├── run.log
└── README.md
```

---

## Configuration

config.yaml

```yaml
seed: 42
window: 5
version: "v1"
```

---

## Local Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

---

## Output Example

metrics.json

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4989,
  "latency_ms": 26,
  "seed": 42,
  "status": "success"
}
```

---

## Logging

The application writes detailed execution logs to:

```text
run.log
```

Including:

* Job start
* Config validation
* Dataset loading
* Rolling mean computation
* Signal generation
* Metrics summary
* Job completion

---

## Docker

Build:

```bash
docker build -t mlops-task .
```

Run:

```bash
docker run --rm mlops-task
```

---

## Assumptions

* Dataset contains a valid `close` column.
* First `window - 1` rows produce NaN rolling means.
* Signals are generated as:

```text
signal = 1 if close > rolling_mean
signal = 0 otherwise
```
