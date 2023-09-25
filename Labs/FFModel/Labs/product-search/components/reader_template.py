# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from typing import List

from ffmodel.components.base import DMT, BaseReaderComponent


class Reader(BaseReaderComponent):
    """
    Include a description of your reader component here

    Args:
    - List the arguments, their defaults and descriptions here

    Data Config:
    - List the expectations of the incoming data format that is referenced
      by the data config

    Note that experimentation workflow will generally make use of `execute_batch`
    method while inference workflows will make use of `execute` method. This is
    because inference workflows will generally be ingesting a single data point
    at a time while experimentation workflows will be ingesting a batch of data
    points in the form of the experimentation data config (a batch of data points).
    """

    def _post_init(self):
        """
        This is called when a new instance of the reader component is initialized.
        Add the necessary logic to:
            - Read your configurations from the solution config/yaml file.
            - Initialize your custom reader component.

        You can read a config using:
            <<config_var_name>> = self.args.get("<<config-name>>", "<<optional-default>>"")
        You need to declare your variable name to hold the config in `config_var_name`.
        Also, replace `config-name` with your config name in the solution config file.

        You can also pre-load or parse the data in the data config at this stage.
        Take a look at ./components/readers/jsonl.py for an example implementation.
        """
        pass

    def execute(self, data: str) -> DMT:
        """
        This holds the core execution reader logic to ingest a single data point.
        Be sure to parse it into a data model.
        """
        return {}

    def execute_batch(self) -> List[DMT]:
        """
        This holds the core execution reader logic to ingest a batch of data points.
        Be sure to parse them into a list of data models.
        """
        return []
