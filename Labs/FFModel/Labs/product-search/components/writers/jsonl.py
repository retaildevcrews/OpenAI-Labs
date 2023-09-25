# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
import os
from time import gmtime, strftime
from typing import List

from ffmodel.components.base import BaseWriterComponent
from ffmodel.core.solution_config import DataConfig
from ffmodel.data_models.base import ExperimentDataModel


class Writer(BaseWriterComponent[ExperimentDataModel]):
    """
    Writes the data models into a JSONL file.

    Component config:
        - output_path: The path to the output file with the appropriate extension (e.g. outputs/output.jsonl).
    """

    def _post_init(self):
        """
        Get the file name from the config
        To ensure uniqueness, we tack the current timestamp onto the end of the file name
        """
        self.output_path = self.args.get("output_path", None)

        if not self.output_path:
            raise ValueError("Missing output_path argument in writer component args.")

        base = os.path.splitext(self.output_path)[0]
        time_string = strftime("%Y%m%d-%H%M%S", gmtime())
        self.output_path = f"{base}-{time_string}.jsonl"

        # Make sure the directory exists
        if os.path.dirname(self.output_path):
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

    def execute(self, data_model: ExperimentDataModel) -> ExperimentDataModel:

        with open(self.output_path, "a") as f:
            f.write(json.dumps(data_model.to_dict()) + "\n")

        return data_model

    def execute_batch(self, data_models: List[ExperimentDataModel]) -> List[ExperimentDataModel]:
        """
        Executes the component for the given data models and returns an
        updated data models.
        """

        with open(self.output_path, "w") as f:
            for data_model in data_models:
                f.write(json.dumps(data_model.to_dict()) + "\n")

        return data_models

    def register_experiment_results(self) -> DataConfig:
        return self._register_experiment_results(file_path=self.output_path)
