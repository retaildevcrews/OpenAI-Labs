# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """
    Static context loaded from a file component.
    Adds the content of the context in file to state.context of the data points

    Component Config supporting_data:
        - static_context_file: Path to the static context file.
    """

    def _post_init(self):
        # Loads the few shots
        static_context_info = self.supporting_data.get("static_context_file", None)
        if static_context_info is None:
            raise ValueError("Argument 'static_context_file' must be provided")

        self.static_context_file = static_context_info.file_path
        with open(self.static_context_file) as f:
            self.static_context = f.read()

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        """
        Executes the component for the given data model and returns an
        updated data model.
        """
        data_model.state.context.append(self.static_context)

        return data_model
