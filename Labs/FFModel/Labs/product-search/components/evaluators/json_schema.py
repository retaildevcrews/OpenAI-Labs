# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import ExperimentDataModel


class Component(BaseSolutionComponent[ExperimentDataModel]):
    """
    Evaluator component for evaluating that the generated completions are valid json
    and optionally that they contain the expected keys.

    Metrics:
        - valid_syntax: whether the completion is json (1) or not (0)
        - valid_objec: whether the completion is valid according to the provided json schema (1) or not (0)

    Component Args:
        - schema: json schema that describes expected structure of json object

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
        self.schema = self.args.get("schema")

    def execute(self, data_model: ExperimentDataModel) -> ExperimentDataModel:
        """Executes the component for the given data model and returns an
        updated data model."""

        completions = data_model.model_output.completions

        results = {k: [] for k in ["valid_syntax", "valid_object"]}

        for c in completions:
            try:
                completion = json.loads(c)
                results["valid_syntax"].append(1)
                validate(instance=completion,schema=self.schema)
                results["valid_object"].append(1)
            except json.JSONDecodeError:
                results["valid_syntax"].append(0)
                results["valid_object"].append(0)
                continue
            except ValidationError:
                results["valid_object"].append(0)
                continue

        data_model.experiment_metrics[self.get_id()] = results

        return data_model
