# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ffmodel.components.base import BaseSolutionComponent
from ffmodel.data_models.base import InferenceDataModel


class Component(BaseSolutionComponent[InferenceDataModel]):
    """
    Include a description of your solution component here

    Args:
    - List the arguments, their defaults and descriptions here

    Supporting Data:
    - List the supporting data fields, their defaults and descriptions here
    """

    def _post_init(self):
        """
        This is called when a new instance of the component is initialized.
        Add the necessary logic to:
            - Read your configurations from the solution config/yaml file.
            - Initialize your custom component.

        You can read a config using:
            <<config_var_name>> = self.args.get("<<config-name>>", "<<optional-default>>"")
        You need to declare your variable name to hold the config in `config_var_name`.
        Also, replace `config-name` with your config name in the solution config file.

        You can consume supporting data as follows:
            <<data_file_var_name>> = self.supporting_data.get("<<supporting-data-name>>", None)
        This returns a DataConfig construct for your supporting data.
        """
        pass

    def execute(self, data_model: InferenceDataModel) -> InferenceDataModel:
        """
        This holds the core logic to execute for your component and update the data model as needed.
        """
        return data_model
