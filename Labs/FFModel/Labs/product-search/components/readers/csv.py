# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import csv
from typing import List

from ffmodel.components.base import DMT
from ffmodel.components.base import BaseReaderComponent as BaseReader
from ffmodel.utils.data_model_util import create_data_models


class Reader(BaseReader):
    """
    Reader for reading in data that follows a CSV format.
    Required fields on the data points: nl_prompt, completion.
    """

    def execute(self, data: str) -> DMT:
        raise NotImplementedError("CSV reader does not support single data points.")

    def execute_batch(self) -> List[DMT]:
        """
        Executes the reader on a list of csv data points.
        """
        if self.data_config is None:
            raise ValueError("data config must be provided.")

        file_path = self.data_config.file_path

        data_points = []
        with open(file_path, "r") as f:
            contents = csv.DictReader(f)
            data_points = list(contents)

        data_models = create_data_models(data_points, self.data_model_type)
        return data_models
