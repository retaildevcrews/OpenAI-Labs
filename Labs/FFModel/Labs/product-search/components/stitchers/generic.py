# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import logging

from prompt_engine.interaction import Interaction
from prompt_engine.model_config import ModelConfig
from prompt_engine.prompt_engine import PromptEngine, PromptEngineConfig

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """
    Generic stitcher for putting ModelState into a ModelInput.
    Wrapper around the prompt-engine-py package.
    Github page: https://github.com/microsoft/prompt-engine-py

    The configuration for a prompt contains the following order:
    1. Description: Context for the model
    2. Completion pair examples
    3. Description: Flow reset text to distinguish between examples and session history
    4. Session history examples
    5. User provided NL prompt

    Anything that is a description is plain text.

    Component Config:
        - max_tokens: Max tokens for the input to the model
        - description_prefix: Symbols that prefix any description (context, flow text)
        - description_postfix: Symbols that postfix any description (context, flow text)
        - prompt_prefix: Symbols that prefix any prompt (examples, NL user input, etc)
        - prompt_postfix: Symbols that postfix any prompt (examples, NL user input, etc)
        - flow_reset_text: Text the goes between the completion pair examples and session history examples
    """

    def _post_init(self):
        self.max_tokens = self.args.get("max_tokens", 1024)
        self.description_prefix = self.args.get("description_prefix", '"""')
        self.description_postfix = self.args.get("description_postfix", '"""')
        self.prompt_prefix = self.args.get("prompt_prefix", "#")
        self.prompt_postfix = self.args.get("prompt_postfix", "")
        self.flow_reset_text = self.args.get("flow_reset_text", "Past requests")

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:

        promptEngineConfig = PromptEngineConfig(
            ModelConfig(max_tokens=self.max_tokens),
            description_prefix=self.description_prefix,
            description_postfix=self.description_postfix,
            input_prefix=self.prompt_prefix,
            input_postfix=self.prompt_postfix,
        )

        newline = "\n"
        context = newline.join(data_model.state.context)

        examples = []
        if len(data_model.state.completion_pairs) > 0:
            for (nl, code) in data_model.state.completion_pairs:
                examples.append(Interaction(nl, code))

        dialog = []
        if len(data_model.state.session) > 0:
            for (nl, code) in data_model.state.session:
                dialog.append(Interaction(nl, code))

        engine = PromptEngine(promptEngineConfig, context, examples, self.flow_reset_text, dialog)

        try:
            prompt = engine.build_prompt(data_model.state.user_nl)
        except:
            # Warn the user that they've exceeded their token limit, but create the prompt anyway
            # Using a large max_token value to ensure the prompt gets created
            engine.config.model_config.max_tokens = 10000000
            prompt = engine.build_prompt(data_model.state.user_nl)

            logging.warning("Issue building out the prompt. The token length limit may have been exceeded.")

        data_model.model_input.prompt = prompt

        return data_model
