# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """
    Session selector component.
    Gets the most recent N pairs from the `sessions` and adds it to state.

    Component Config:
        - count: Number of most recent sessions to add to state
    """

    def _post_init(self):
        self.count = self.args.get("count", 3)

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        """
        Executes the component for the given data model and returns an
        updated data model.
        """
        if data_model.request.session is not None and len(data_model.request.session) > 0:
            data_model.state.session = data_model.request.session[-self.count :]
            self.logger.info(f"Selecting {self.count} sessions", data_model=data_model)

        return data_model
