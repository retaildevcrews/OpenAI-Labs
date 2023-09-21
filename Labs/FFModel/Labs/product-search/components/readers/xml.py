# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import xml.etree.ElementTree as ET
from typing import Any, List

from ffmodel.components.base import DMT
from ffmodel.components.base import BaseReaderComponent as BaseReader


class Reader(BaseReader):
    """
    Reader for reading in data that follows an XML format.
    """

    def execute(self, data: Any) -> DMT:
        raise NotImplementedError("XML reader does not support single data points.")

    def execute_batch(self) -> List[DMT]:
        """Loads the experiment requests from the CSV file"""
        if self.data_config is None:
            raise ValueError("data config must be provided.")

        file_path = self.data_config.file_path

        tree = ET.parse(file_path)
        root = tree.getroot()

        data_points = []

        for item in root.findall("./record"):
            record = {}
            for child in item:
                record[child.tag] = child.text
            data_points.append(record)

        data_models = BaseReader.create_data_models(data_points, self.data_model_type)
        return data_models
