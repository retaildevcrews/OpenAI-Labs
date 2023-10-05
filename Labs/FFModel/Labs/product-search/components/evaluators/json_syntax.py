# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import ExperimentDataModel


class Component(BaseSolutionComponent[ExperimentDataModel]):
    """
    Evaluator component for evaluating that the generated completions are valid json
    and optionally that they contain the expected keys.

    Metrics:
        - valid_syntax: whether the completion is json (1) or not (0)
        - found_keys: The percentage of expected keys that were found, from 0 to 1

    Component Args:
        - expected_keys: list of keys that are checked for if it is valid

    Fields used:
        - data_model.model_output.completions: the list of completions to evaluate

    Fields updated:
        - data_model.experiment_metrics[<component-id>]: a dictionary of metrics for
            the component. This dictionary will contain one entry for each measure,
            where the key is the name of the measure and the value is a list of
            metrics, one entry for each completion.
            e.g. data_model.experiment_metrics[<component-id>] = {
                "valid_syntax": [1, 0, 1, ...]
            }
    """

    def _post_init(self):
        # Sets defaults for other values
        self.expected_keys = self.args.get("expected_keys", [])

    def execute(self, data_model: ExperimentDataModel) -> ExperimentDataModel:
        """Executes the component for the given data model and returns an
        updated data model."""

        completions = data_model.model_output.completions

        results = {k: [] for k in ["valid_syntax", "found_keys"]}

        for c in completions:
            try:
                completion = json.loads(c)
                results["valid_syntax"].append(1)
            except json.JSONDecodeError:
                results["valid_syntax"].append(0)
                results["found_keys"].append(0)
                continue

            matched_keys = 0
            for k in self.expected_keys:
                if k in completion:
                    matched_keys += 1

            results["found_keys"].append(matched_keys / len(self.expected_keys))

        data_model.experiment_metrics[self.get_id()] = results

        return data_model
