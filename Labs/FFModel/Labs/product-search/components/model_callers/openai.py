# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import (
    ExperimentDataModel,
    InferenceDataModel,
    InferenceRequest,
    ModelState,
)
from ffmodel.utils.openai import (
    OpenAIConfig,
    RetryParameters,
    filter_completion_arguments,
    generate_completion,
    initialize_openai,
)


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """
    OpenAI model caller.

    Calls the OpenAI completion endpoint to generate the completion.

    Component Args:
        - config: Dict[str, str], dictionary of config that control the OpenAI API
            - api_key_config_name: str, name of the config value to pull the api key from, defaults to OPENAI_API_KEY
            - api_endpoint_config_name: str, name of the config value to pull the api endpoint from, defaults to OPENAI_ENDPOINT
            - api_version: str, version of the OpenAI API to use, defaults to "2023-03-15-preview"
        - retry_params: Dict[str, Any], dictionary of retry parameters, with keys of:
            - tries: int, the maximum number of attempts. The first call counts as a try
            - delay: float, initial delay between attempts, in seconds
            - backoff: float, multiplier applied to the delay between attempts
            - max_delay: float, the maximum delay between attempts, in seconds

    In addition the following args from openAI are most common, but any openAI arg can be passed:
        - engine: str, model to use
        - stop: List[str], list of stop tokens
        - temperature: float, temperature as a float, between 0 and 1
        - max_tokens: int, max number of tokens to return from the model
        - best_of: int, number of completions to generate and then sample from
        - For the full list, see: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference#completions
    """

    def _post_init(self):
        """Custom initialization logic for getting the api key and arg list"""
        config_names = self.args.pop("config", {})
        self.openai_config = OpenAIConfig.from_dict(config_names)

        retry_params = self.args.pop("retry_params", {})
        self.retry_params = RetryParameters.from_dict(retry_params)

        self.filtered_kwargs = filter_completion_arguments(self.args)
        self.call_openai_function = generate_completion

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        """
        Calls OpenAI for the model input and stores results to model outputs

        It will raise a ValueError if the prompt is not set
        """
        initialize_openai(self.openai_config)

        if not data_model.model_input.prompt:
            raise ValueError("model_input.prompt must be set")

        completion = self.call_openai_function(
            prompt=data_model.model_input.prompt,
            retry_parameters=self.retry_params,
            **self.filtered_kwargs,
        )

        model_outputs = []
        for choice in completion.choices:
            model_outputs.append(choice.text)

        if data_model.model_output.completions is None:
            data_model.model_output.completions = model_outputs
        else:
            data_model.model_output.completions.extend(model_outputs)

        # Add the token usage to the experiment metrics
        if type(data_model) is ExperimentDataModel:
            formatted_usage = {}
            for key, value in completion.usage.items():
                formatted_usage[key] = [value]
            data_model.experiment_metrics[self.get_id()] = formatted_usage

        return data_model
