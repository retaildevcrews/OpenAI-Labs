# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import sqlglot

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import ExperimentDataModel


class Component(BaseSolutionComponent[ExperimentDataModel]):
    """Evaluator to check the completions for being valid, non-empty SQL"""

    def execute(self, data_model: ExperimentDataModel) -> ExperimentDataModel:
        """
        Executes the component for the given data model and returns an
        updated data model.
        """

        completions = data_model.model_output.completions

        results = {k: [] for k in ["non-empty", "syntax-valid"]}

        for completion in completions:
            results["non-empty"].append(int(len(completion) > 0))
            try:
                sqlglot.parse_one(completion)
                results["syntax-valid"].append(1)
            except:
                results["syntax-valid"].append(0)

        data_model.experiment_metrics[self.get_id()] = results

        return data_model
