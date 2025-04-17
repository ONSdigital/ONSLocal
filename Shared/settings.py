import ast
import os

from pathlib import Path

import pandas as pd
from dotenv import dotenv_values


class DataLoader:
    def __init__(self, env_path):
        config = env_load(env_path)

        for variable in config:
            try:
                # Convert key into a list if possible
                key = ast.literal_eval(config[variable])
            except (ValueError, SyntaxError):
                # Error raised when config[variable] cannot be converted into a list
                key = config[variable]

            if isinstance(key, str):
                data = read_file(config[variable])
            elif isinstance(key, list):
                data = []
                for file in key:
                    data.append(read_file(file))
            else:
                raise TypeError(f"Variable {variable} type in .env not recognised.")

            setattr(self, variable, data)


def env_load(env_path):
    if not Path(env_path).exists():
        raise FileNotFoundError(f".env file not found: {env_path}")

    # Parse .env file
    return dict(dotenv_values(env_path))


def read_file(data_path):
    data_path = os.path.join("data", data_path)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File {data_path} not found.")
    else:
        return pd.read_csv(data_path)
