# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """Cut the model outputs to only the first completion."""

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        data_model.model_output.completions = data_model.model_output.completions[:1]

        return data_model
