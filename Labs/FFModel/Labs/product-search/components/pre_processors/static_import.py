# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel, InferenceRequest, ModelState


class Component(BaseSolutionComponent[InferenceDataModel[InferenceRequest, ModelState]]):
    """
    Static import statement component.
    Adds the `import_statement` field from the component config to the model state.

    Component Config:
        - import_statement: import statement to add
    """

    def _post_init(self):
        if "import_statement" not in self.args:
            raise ValueError("Import statement component requires a `import_statement` field in the component config.")
        self.import_statement = self.args["import_statement"]

    def execute(
        self, data_model: InferenceDataModel[InferenceRequest, ModelState]
    ) -> InferenceDataModel[InferenceRequest, ModelState]:
        """
        Executes the component for the given data model and returns an updated data model.
        """

        import_statements = data_model.state.component_data.get("import_statements", [])
        import_statements.append(self.import_statement)
        data_model.state.component_data["import_statements"] = import_statements

        return data_model
