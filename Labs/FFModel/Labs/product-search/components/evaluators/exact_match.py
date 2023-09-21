# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import ExperimentDataModel


class Component(BaseSolutionComponent[ExperimentDataModel]):
    """
    Exact Match evaluator returns 1 for an exact string match between a completion and expected output, 0 otherwise.
    """

    def execute(self, data_model: ExperimentDataModel) -> ExperimentDataModel:
        """Executes the component for the given data model and returns an
        updated data model."""

        expected_output = data_model.request.expected_output
        completions = data_model.model_output.completions

        results = []

        for e in expected_output:
            for c in completions:
                if e == c:
                    results.append(1)
                else:
                    results.append(0)

        data_model.experiment_metrics[self.get_id()] = {"exact_match": results}

        return data_model
