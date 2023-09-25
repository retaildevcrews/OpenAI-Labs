# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel


class Component(BaseSolutionComponent[InferenceDataModel]):
    """
    A stitcher component that stitches information and arranges it according
     to a provided prompt template.

    Component Config:
    - template [str]: A string containing the template to be used for stitching.
      Example template:
        ```
        # This is a simple natural language to python scenario, where we'd like to
        # generate python code for the given natural language text from an end user.

        {context}

        {completion_pairs}

        {session}

        {user_nl}
        ```
    - condense_blank_lines [bool]: If True, condenses double blank lines to a single blank
      line. This is useful if certain fields like past session history don't have values in
      the incoming data model state. Default: False
    """

    def _post_init(self):
        self.template = self.args.get("template", "")
        self.condense_blank_lines = self.args.get("condense_blank_lines", False)

    def execute(self, data_model: InferenceDataModel) -> InferenceDataModel:
        """
        Executes the component for the given data model and returns an
        updated data model.
        """
        prompt = self.template

        # Render user nl as single line comment
        if "{user_nl}" in prompt:
            prompt = prompt.replace("{user_nl}", f"# {data_model.state.user_nl}")

        # Render each context as a single line comment
        if "{context}" in prompt:
            context_strs = [f"# {context}" for context in data_model.state.context]
            prompt = prompt.replace("{context}", "\n\n".join(context_strs))

        # Render each completion pair as a python comment and code
        if "{completion_pairs}" in prompt:
            completion_pairs_strs = [
                f"# {prompt}\n{completion}" for prompt, completion in data_model.state.completion_pairs
            ]
            prompt = prompt.replace("{completion_pairs}", "\n\n".join(completion_pairs_strs))

        # Render each session as a python comment and code
        if "{session}" in prompt:
            session_strs = [f"# {prompt}\n{completion}" for prompt, completion in data_model.state.session]
            prompt = prompt.replace("{session}", "\n\n".join(session_strs))

        if self.condense_blank_lines:
            # Replace duplicated blank lines with single blank line
            while "\n\n\n" in prompt:
                prompt = prompt.replace("\n\n\n", "\n\n")

        data_model.model_input.prompt = prompt

        return data_model
