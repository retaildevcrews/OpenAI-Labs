# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
import json

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """
    Pre-processor component for adding a static context from a file to the data
    model as state information to be used to build a prompt.

    Component Supporting Data:
        - few_shot_file: the path to the file containing
            the few shot examples

    Fields used:
        - data_model.state.context: the list of existing context information

    Fields updated:
        - data_model.state.context: the static context gets appended to the list
    """

    def _post_init(self):
        # Loads the few shots
        few_shot_info = self.supporting_data.get("few_shot_file", None)
        if few_shot_info is None:
            raise ValueError("Argument 'few_shot_file' must be provided")

        self.few_shot_file = few_shot_info.file_path
        with open(self.few_shot_file) as f:
            self.shots = json.loads(f.read())

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        """
        Executes the component for the given data model and returns an
        updated data model.
        """
        completion_pairs = [(shot["user_nl"], json.dumps(shot["expected_output"])) for shot in self.shots]
        data_model.state.completion_pairs.extend(completion_pairs)

        return data_model
