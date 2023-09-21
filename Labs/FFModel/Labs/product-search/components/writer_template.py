# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from typing import List

from ffmodel.components.base import BaseWriterComponent
from ffmodel.data_models.base import InferenceDataModel


class Writer(BaseWriterComponent[InferenceDataModel]):
    """
    Include a description of your writer component here

    Args:
    - List the arguments, their defaults and descriptions here
    """

    def _post_init(self):
        """
        This is called when a new instance of the writer component is initialized.
        Add the necessary logic to:
            - Read your configurations from the solution config/yaml file.
            - Initialize your custom writer component.

        You can read a config using:
            <<config_var_name>> = self.args.get("<<config-name>>", "<<optional-default>>"")
        You need to declare your variable name to hold the config in `config_var_name`.
        Also, replace `config-name` with your config name in the solution config file.
        """
        pass

    def execute(self, data_model: InferenceDataModel) -> InferenceDataModel:
        """
        This holds the core logic to execute for your writer component to write whatever
        data you wish to record from your data model. Be sure to return the data model!
        """
        return data_model

    def execute_batch(self, data_models: List[InferenceDataModel]) -> List[InferenceDataModel]:
        """
        This holds the core logic to execute for your writer component, only to do so in batches on
        a list of data models. Feel free to override this or default to the default batch execution
        logic in the base class--whatever makes sense for your writer logic. Be sure to return the
        data models once the writer logic has completed executing!
        """
        return super().execute_batch(data_models)
