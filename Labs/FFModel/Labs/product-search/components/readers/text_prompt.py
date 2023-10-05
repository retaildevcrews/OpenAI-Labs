from typing import List

from ffmodel.components.base import DMT
from ffmodel.components.base import BaseReaderComponent as BaseReader
from ffmodel.utils.data_model_util import create_data_models


class Reader(BaseReader):
    """
    Reader for reading in data that follows a JSONL format.
    Required fields on the data points: nl_prompt, completion.
    """

    def execute(self, data: str) -> DMT:
        """
        Executes the reader on a json line data point.
        """

        data_point = {"user_nl": data}

        data_models = create_data_models([data_point], self.data_model_type)
        return data_models[0]

    def execute_batch(self) -> List[DMT]:
        raise NotImplementedError("Text prompt reader does not support batch data points.")
