# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
import os
import pickle

import numpy as np

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState
from ffmodel.utils.openai import (
    OpenAIConfig,
    RetryParameters,
    get_embedding,
    initialize_openai,
)

REQUIRED_FIELDS = ["context", "embedding"]


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """
    Adds the relevant context to the prompt. The context selection is done by cosine similarity.

    This component is used to add the context for a specific NL prompt request.
    The context bank data is loaded from a pickle file. The pickle file should be in the following format:
    {
        "metadata": {
            "embedding_model": "embedding model used to generate the context embeddings"
        },
        "data": [
            {
                "context": "context strings, can be text corpus, or programming docstring",
                "embedding": "embedding vector for context"
            },
            ...
        ]
    }

    Component Config args:
        - count: The number of context strings to select, defaults to 1
        - reverse: When true, the closest match is at the end, defaults to true
        - config: Dict[str, str], dictionary of config that control the OpenAI API
            - api_key_config_name: str, name of the config value to pull the api key from, defaults to OPENAI_API_KEY
            - api_endpoint_config_name: str, name of the config value to pull the api endpoint from, defaults to OPENAI_ENDPOINT
            - api_version: str, version of the OpenAI API to use, defaults to "2023-03-15-preview"
        - retry_params: Dict[str, Any], dictionary of retry parameters, with keys of:
            - tries: int, the maximum number of attempts. The first call counts as a try
            - delay: float, initial delay between attempts, in seconds
            - backoff: float, multiplier applied to the delay between attempts
            - max_delay: float, the maximum delay between attempts, in seconds
    Component Config supporting_data:
        - context_file: Path to the pickle file containing the context files.
        - cached_embeddings: Path to a pickle file containing prior embeddings, this follows the format as context_file.
          The idea is to cache the embeddings for your evaluation data set and reuse them when rerunning the experiment.
    """

    call_embedding_function = get_embedding

    def get_embedding_with_cache(self, user_nl: str) -> list:
        """
        This function will return a cached embedding if a match is found for the given user_nl.
        Otherwise, it will call OpenAI to generate the embedding.
        """
        embedding = None

        # Note: please use the same `few_shot_embedding.create_few_shot_file` function to generate the cache file for evaluation data set.
        if self.cached_embeddings:
            # search for a match based on the prompt
            embedding = self.cached_embeddings.get(user_nl, None)

        if embedding is None:
            initialize_openai(self.openai_config)
            embedding = Component.call_embedding_function(user_nl, self.embedding_model, self.retry_params)

        return embedding

    def _load_cached_embeddings(self, cache_file: str):
        data_file = None
        with open(cache_file, "rb") as f:
            # The pickled file has a dict with metadata and data that holds prompts
            # with their embeddings, thus, we only care for data.
            data_file = pickle.load(f)["data"]

        if data_file:
            self.cached_embeddings = {data["user_nl"]: data["embedding"] for data in data_file}

    def _post_init(self):
        # Load the context file
        context_arg = self.supporting_data.get("context_file", None)
        if context_arg is None:
            raise ValueError("Argument 'context_file' must be provided")

        self.context_file = context_arg.file_path
        self._load_context()

        # Loads the cached embeddings
        self.cached_embeddings = None
        cached_embeddings_config = self.supporting_data.get("cached_embeddings", None)
        if cached_embeddings_config:
            self._load_cached_embeddings(cached_embeddings_config.file_path)

        # Parse the input arguments
        config_names = self.args.pop("config", {})
        self.openai_config = OpenAIConfig.from_dict(config_names)

        retry_params = self.args.pop("retry_params", {})
        self.retry_params = RetryParameters.from_dict(retry_params)

        # Sets defaults for other values
        self.count = self.args.get("count", 1)
        self.reverse = self.args.get("reverse", True)

    def _load_context(self):
        """
        Loads the context data from the given file.

        Performs validation on each data point to make sure the required information is present
        """
        # Load the context file - See "create_context_file" for the contents
        with open(self.context_file, "rb") as f:
            context_bank = pickle.load(f)

        try:
            self.embedding_model = context_bank["metadata"]["embedding_model"]
        except KeyError:
            raise ValueError("Context file does not contain metadata with embedding_model specified")

        # Validate data
        for d in context_bank["data"]:
            for field in REQUIRED_FIELDS:
                if field not in d:
                    raise ValueError(f"Context data point missing required field {field}")

        self.context_bank = context_bank["data"]

        # Pull out the embeddings to a numpy array for faster cosine similarity calculation
        embeddings = []
        for item in self.context_bank:
            normalization = np.linalg.norm(item["embedding"])
            embeddings.append(np.array(item["embedding"]) / normalization)

        self.embeddings = np.array(embeddings)

    def _get_cosine_sim(self, embedding: list):
        "get cosine similarities between context banks embeddings and the prompt embedding"
        embedding = np.array(embedding) / np.linalg.norm(embedding)
        return np.dot(self.embeddings, embedding)

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        """
        Executes the component for the given data model and returns an
        updated data model.
        """
        prompt_text = data_model.request.user_nl
        prompt_embedding = self.get_embedding_with_cache(prompt_text)

        # calculate cosine similarity between prompt embedding and context bank embeddings
        cos_sim_ls = self._get_cosine_sim(prompt_embedding)

        # find top n context string using cosine similarity
        # Reverse is passed so that the closest match is first
        top_n_index = sorted(range(len(cos_sim_ls)), key=lambda i: cos_sim_ls[i], reverse=True)[: self.count]
        context = [self.context_bank[i] for i in top_n_index]

        if self.reverse:
            context = list(reversed(context))

        context_str = "\n".join(d["context"] for d in context)

        # Add to the context
        data_model.state.context.append(context_str)

        return data_model

    @staticmethod
    def create_context_file(
        input_file: str,
        embedding_model: str,
        openai_config: OpenAIConfig = OpenAIConfig(),
        retry_params: RetryParameters = RetryParameters(),
        reporting_interval: int = 500,
    ) -> str:
        """Creates a context data file with embeddings.
        api_key_config_name: The name of the environment variable holding the API key for the Azure OpenAI resource
        api_endpoint_config_name: The name of the environment variable holding the endpoint for the Azure OpenAI resource
        input_file: The path to the input dataset. The input data will be in jsonlines format, with each line being a json object with a required "context" field.
                    The data can have other fields (i.e. )
                    {"context": "context strings, can be text corpus, or programming docstring"
                    "context:...}
        embedding_model: Embedding engine to use when generating embeddings

        The generated context data bank is a pickle file containing a dictionary with two fields:
            - metadata: Currently only key is the embedding model used
            - data: List of dictionaries containing the context text and embedding vectors
        """
        # Load the data in jasonline.
        data = []
        with open(input_file, "r") as f:
            for line in f.readlines():
                data.append(json.loads(line))

        # Generate embeddings for context strings.
        initialize_openai(openai_config)
        print(f"Generating embeddings for {len(data)} points")
        for i, d in enumerate(data):
            d["embedding"] = Component.call_embedding_function(
                prompt=d["context"],
                model=embedding_model,
                retry_parameters=retry_params,
            )

            if i % reporting_interval == 0:
                print(f"Completed {i+1} out of {len(data)} embeddings")

        context_data = {
            "metadata": {"embedding_model": embedding_model},
            "data": data,
        }
        output_file = f"{os.path.splitext(input_file)[0]}_{embedding_model}.pkl"
        with open(output_file, "wb") as f:
            pickle.dump(context_data, f)

        print(f"context data pickle file generated and saved to {output_file}")

        return output_file
