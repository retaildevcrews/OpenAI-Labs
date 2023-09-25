# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """Component for stitching a message in the OpenAI chat completion format.

    The format requires a set of messages that are List[Dict[str,str]], so to pass in the
    data_model.model_input.prompt field, we will use json.dumps() to convert the string.

    The paired component `../model_callers/openai_chat_completion.py` will convert the
    prompt back to a string.

    As a guide:
        - state.context will be mapped into the system message
        - state.completion_pairs will be added at the beginning of the user-assistant pairs
        - An optional reset text will go next
        - state.session will go next
        - state.user_nl will go last as a user message

    The response will then be from the assistant

    Component config parameters:
        - user_reset_text: User text to go before the switch from few shots to session history.
        - assistant_reset_text: Assistants response to the user_reset_text.
    """

    def _post_init(self):
        # Load config parameters
        self.user_reset_text = self.args.get("user_reset_text", "$$RESET$$")
        self.assistant_reset_text = self.args.get(
            "assistant_reset_text",
            "Reset acknowledged. Previous messages will be used as a guide for correct syntax and as valid examples, but will not be considered part of the current conversation.",
        )

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        messages = []

        if data_model.state.context:
            messages.append({"role": "system", "content": "\n".join(data_model.state.context)})

        if len(data_model.state.completion_pairs) > 0:
            for (prompt, completion) in data_model.state.completion_pairs:
                messages.append({"role": "user", "content": prompt})
                messages.append({"role": "assistant", "content": completion})

            messages.append({"role": "user", "content": self.user_reset_text})
            messages.append({"role": "assistant", "content": self.assistant_reset_text})

        if len(data_model.state.session) > 0:
            for (prompt, completion) in data_model.state.session:
                messages.append({"role": "user", "content": prompt})
                messages.append({"role": "assistant", "content": completion})

        messages.append({"role": "user", "content": data_model.state.user_nl})

        prompt = json.dumps(messages, indent=2)

        data_model.model_input.prompt = prompt

        return data_model
