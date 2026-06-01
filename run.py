import argparse
import json
import logging
import time
from io import StringIO

import numpy as np
import pandas as pd
import yaml


def write_error_metrics(output_file, version, error_message):
    metrics = {
        "version": version,
        "status": "error",
        "error_message": error_message
    }

    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=2)

    print(json.dumps(metrics, indent=2))


def main():
    start_time = time.time()

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    try:
        logging.basicConfig(
            filename=args.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        logging.info("Job Started")

        # Load Config
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        required_fields = ["seed", "window", "version"]

        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required config field: {field}")

        np.random.seed(config["seed"])

        logging.info(
            f"Config Loaded: seed={config['seed']}, "
            f"window={config['window']}, "
            f"version={config['version']}"
        )

        # Load Dataset
        with open(args.input, "r") as f:
            lines = [line.strip().strip('"') for line in f]

        csv_text = "\n".join(lines)

        df = pd.read_csv(StringIO(csv_text))

        if df.empty:
            raise ValueError("Dataset is empty")

        if "close" not in df.columns:
            raise ValueError("Missing required column: close")

        logging.info(f"Rows Loaded: {len(df)}")

        # Rolling Mean
        df["rolling_mean"] = df["close"].rolling(
            window=config["window"]
        ).mean()

        logging.info("Rolling Mean Computed")

        # Signal
        df["signal"] = (
            df["close"] > df["rolling_mean"]
        ).astype(int)

        logging.info("Signals Generated")

        rows_processed = len(df)
        signal_rate = float(df["signal"].mean())

        latency_ms = int(
            (time.time() - start_time) * 1000
        )

        metrics = {
            "version": config["version"],
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": config["seed"],
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=2)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job Completed Successfully")

        print(json.dumps(metrics, indent=2))

    except Exception as e:
        version = "v1"

        try:
            if "config" in locals():
                version = config.get("version", "v1")
        except:
            pass

        write_error_metrics(
            args.output,
            version,
            str(e)
        )

        logging.exception("Job Failed")
        raise


if __name__ == "__main__":
    main()