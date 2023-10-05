# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
from pathlib import Path
from typing import List

import pandas as pd


def load_experiments_outputs(outputs_dir: str) -> pd.DataFrame:
    """
    Given a folder with the JSONL outputs from FFModel experiments, load them into a Panda DataFrame.

    Parameters:
    outputs_dir (str): The path to the directory holding the experiments outputs.

    Returns
    -------
    pd.DataFrame: Output results loaded and stored as a DataFrame.
    """

    experiments = []

    for exp in os.listdir(outputs_dir):
        if exp[-6:] == ".jsonl" and exp:
            experiments.append(Path(f"{exp}"))

    # load each experiment
    dfs = []
    for path in experiments:
        df = pd.read_json(os.path.join(outputs_dir, Path(path)), lines=True)
        session_ids = [df.iloc[idx]["request"]["complementary_data"]["session_id"] for idx, _ in df.iterrows()]
        expected_output = [df.iloc[idx]["request"]["expected_output"] for idx, _ in df.iterrows()]
        df.insert(0, "session_id", session_ids)
        df.insert(0, "experiment", path.stem)
        df.insert(0, "expected_output", expected_output)
        dfs.append(df)

    # concatenate dfs to single df
    df = pd.concat(dfs)
    return df


def extract_metrics(df: pd.DataFrame, metrics: List[str] = None):
    """
    Function used to extract metrics from output results from FFModel Experiments

    Parameters:
    df (pd.DataFrame): Input df consisting of output results
    metrics (List[str]): A list of metrics to extract

    Returns
    -------
    pd.DataFrame: Output Dataframe consisting of metrics calculated for each respective experiment
    """

    # instantiate dict to hold metrics in
    metrics_dict = {}

    # grab values from dataframe
    exp_metrics = df["experiment_metrics"].values

    # loop and extract metrics
    for element in exp_metrics:
        # grab metric class
        for key in element:

            metric_class = key.split(".")[-1]
            sub_dict = element[key]

            # iterate through sub dict and extract results
            for sub_key, sub_values in sub_dict.items():
                metric_name = f"{metric_class}.{sub_key}"
                # if metrics is not None, only extract metrics in list
                if metrics is not None:
                    if metric_name not in metrics:
                        continue
                if metric_name not in metrics_dict:
                    metrics_dict[metric_name] = []

                if len(sub_values) > 1:
                    metrics_dict[metric_name].append(max(sub_values))
                else:
                    metrics_dict[metric_name].append(sub_values[0])

    print(f"Extracted the following metrics {metrics_dict.keys()}")
    # set columns
    columns = ["experiment"]
    for item in metrics_dict:
        columns.append(item)

    for column in columns[1:]:
        df[column] = metrics_dict[column]

    # update df to only hold metrics columns
    df = df[columns]
    return df
