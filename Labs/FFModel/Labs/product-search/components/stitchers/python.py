# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """Default stitcher for putting ModelState into a ModelInput for NL2Python requests."""

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        prompt = ""
        newline = "\n"
        if len(data_model.state.context) > 0:
            prompt += f'"""{newline.join(data_model.state.context)}"""'
            prompt += newline

        if len(data_model.state.completion_pairs) > 0:
            formatted_pairs = []
            for (nl, code) in data_model.state.completion_pairs:
                formatted_pairs.append(f"# {nl}{newline}{code}")
            prompt += newline.join(formatted_pairs)
            prompt += newline

        if len(data_model.state.session) > 0:
            formatted_pairs = []
            for (nl, code) in data_model.state.session:
                formatted_pairs.append(f"# {nl}{newline}{code}")
            prompt += newline.join(formatted_pairs)
            prompt += newline

        prompt += f"# {data_model.state.user_nl}"
        prompt += newline

        data_model.model_input.prompt = prompt

        return data_model
