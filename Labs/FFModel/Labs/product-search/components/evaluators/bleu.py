# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import nltk
from nltk import word_tokenize
from nltk.translate.bleu_score import modified_precision

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import ExperimentDataModel

# download necessary packages to leverage BLEU score function from NLTK
nltk.download("punkt")


class Component(BaseSolutionComponent[ExperimentDataModel]):
    """
    BLEU Score evaluator evaluates the quality and precision of text generated completions that have been translated
    by a machine to the reference human text. It outputs scores between 0 and 1, with 1 being an exact match.

    Component config parameters:
        - n_grams: Sequences of n items from a given sample of text BLEU will be evaluated on.
                   This defaults to 1 for unigram based matching For example, with 1 n-gram,
                   the text `this is a test string` is evaluated as `[this, is, a, test, string]
    """

    def _post_init(self):
        self.n_grams = self.args.get("n_grams", 1)
        self._validate_n_grams()

    def _validate_n_grams(self):
        if type(self.n_grams) != int:
            raise ValueError("n_grams must be an integer")

        if self.n_grams > 4 or self.n_grams < 1:
            raise ValueError(f"Invalid number of n-grams specified: {self.n_grams}")

    def execute(self, data_model: ExperimentDataModel) -> ExperimentDataModel:
        """Executes the component for the given data model and returns an
        updated data model."""

        expected_output = data_model.request.expected_output
        completions = data_model.model_output.completions
        n_grams = self.n_grams
        results = {f"bleu_score_ngrams_{n_grams}": []}

        for e_prompt in expected_output:
            for c_prompt in completions:
                # compute bleu score
                bleu = self.bleu_score(e_prompt, c_prompt, self.n_grams)
                results[f"bleu_score_ngrams_{n_grams}"].append(bleu)

        data_model.experiment_metrics[self.get_id()] = results

        return data_model

    def bleu_score(self, expected_output: str, generated_output: str, n_grams: int) -> float:
        """
        Function used to serve as helper for computing modified ngram precision (unigram)
        for a list of prompts using BLEU score module from NLTK.
        """

        score = float(modified_precision([word_tokenize(expected_output)], word_tokenize(generated_output), n_grams))
        return score
