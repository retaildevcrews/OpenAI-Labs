# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from typing import List

from rouge_score import rouge_scorer

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import ExperimentDataModel


class Component(BaseSolutionComponent[ExperimentDataModel]):
    """
    The base Rouge evaluator class. Estimate the difference between two strings
    using a Rouge1 score. See the brief explanation within the [library
    here](https://github.com/google-research/google-research/tree/master/rouge).
    Note that the out-of-box rouge calculation done in score() will likely need
    to be overwritten/post-processed for any particular scenario.

    The output values will range from 0 to 1, with 1 being an exact match.
    """

    def _post_init(self):
        self.modes = self.args.get("modes", ["rouge1"])
        self.mode_score_details = ["precision", "recall", "fmeasure"]

        self._validate_modes()

    def _validate_modes(self):
        valid_modes = ["rouge1", "rougeL"]

        for mode in self.modes:
            if mode not in valid_modes:
                raise ValueError(f"Invalid ratio method: {mode}")

    def score(self, expected_output: List[str], completions: List[str]) -> dict[str, float]:
        """
        Calculates rouge scoring for two outputs, one that is expected and
        one that is generated, for all defined modes.
        """

        scorer = rouge_scorer.RougeScorer(self.modes, use_stemmer=False)
        results = {f"{k}_{j}": [] for k in self.modes for j in self.mode_score_details}

        for e in expected_output:
            for c in completions:
                score = scorer.score(e, c)

                for mode in self.modes:
                    mode_score = score[mode]

                    results[f"{mode}_precision"].append(mode_score.precision)
                    results[f"{mode}_recall"].append(mode_score.recall)
                    results[f"{mode}_fmeasure"].append(mode_score.fmeasure)

        return results

    def execute(self, data_model: ExperimentDataModel) -> ExperimentDataModel:
        """Executes the component for the given data model and returns an
        updated data model."""

        expected_output = data_model.request.expected_output
        completions = data_model.model_output.completions

        results = self.score(expected_output, completions)
        data_model.experiment_metrics[self.get_id()] = results

        return data_model
