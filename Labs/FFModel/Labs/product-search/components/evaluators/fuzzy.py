# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from thefuzz import fuzz

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import ExperimentDataModel


class Component(BaseSolutionComponent[ExperimentDataModel]):
    """
    Fuzzy evaluator calculates the similarity between the prompt and the completions.
    The output values are normalized between 0 and 1, where 1 is the most similar.

    Component config parameters:
        - ratio_methods: The forms of fuzzy difference to calculate. Default is ["simple", "partial"]
    """

    def _post_init(self):
        self.ratio_methods = self.args.get("ratio_methods", ["simple", "partial"])

        # Lookup from easy to use short hand to corresponding thefuzz function
        self.ratio_functions = {
            "simple": "ratio",
            "partial": "partial_ratio",
            "token_sort": "token_sort_ratio",
            "token_set": "token_set_ratio",
        }

        self._validate_ratio_methods()

    def _validate_ratio_methods(self):
        for ratio_method in self.ratio_methods:
            if ratio_method not in self.ratio_functions.keys():
                raise ValueError(f"Invalid ratio method: {ratio_method}")

    def execute(self, data_model: ExperimentDataModel) -> ExperimentDataModel:
        """Executes the component for the given data model and returns an
        updated data model."""

        expected_output = data_model.request.expected_output
        completions = data_model.model_output.completions

        results = {k: [] for k in self.ratio_methods}

        for e in expected_output:
            for c in completions:
                for ratio in self.ratio_methods:
                    cmd = getattr(fuzz, self.ratio_functions[ratio])
                    distance = cmd(e, c) / 100

                    results[ratio].append(distance)

        data_model.experiment_metrics[self.get_id()] = results

        return data_model
