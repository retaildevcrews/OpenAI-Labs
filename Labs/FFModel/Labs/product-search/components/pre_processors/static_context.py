# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """
    Static context component.
    Adds the `static_context` field from the component config to the context.

    Component Config:
        - static_context: Context text to add
    """

    def _post_init(self):
        if "static_context" not in self.args:
            raise ValueError("Static context component requires a `static_context` field in the component config.")

        self.static_context = self.args["static_context"]

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        """
        Executes the component for the given data model and returns an
        updated data model.
        """
        data_model.state.context.append(self.static_context)

        return data_model
