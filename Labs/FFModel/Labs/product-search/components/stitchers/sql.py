# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from typing import List, Tuple

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """Default stitcher for putting ModelState into a ModelInput for NL2SQL requests."""

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        prompt = ""
        newline = "\n"
        if len(data_model.state.context) > 0:
            prompt += f"/*{newline}{newline.join(data_model.state.context)}{newline}*/"
            prompt += newline

        if len(data_model.state.completion_pairs) > 0:
            prompt += Component.render_nl_code_pairs(data_model.state.completion_pairs)

        if len(data_model.state.session) > 0:
            prompt += Component.render_nl_code_pairs(data_model.state.session)

        prompt += f"-- {data_model.state.user_nl}"
        prompt += newline

        data_model.model_input.prompt = prompt

        return data_model

    @staticmethod
    def render_nl_code_pairs(nl_code_pairs: List[Tuple[str, str]]) -> str:
        newline = "\n"
        prompt = ""
        formatted_pairs = []
        for (nl, code) in nl_code_pairs:
            formatted_pairs.append(f"-- {nl}{newline}{code}")
        prompt += newline.join(formatted_pairs)
        prompt += newline

        return prompt
