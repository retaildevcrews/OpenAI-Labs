# FFModel Solution Config

FFModel provides a config driven approach to define a solution you want to experiment with.
This approach enables you to reuse and customize your solutions with minimal overhead and with no code changes to your components.

As a user, you do not need to modify the solution config between experimenting locally, on the cloud, and deploying the solution for inference.
The current implementation for FFModel is integrated with Azure Machine Learning (AML) to experiment and deploy your solution to the cloud.

## The Solution Config

A solution is defined using a YAML file with the following fields:

- `id` is your identifier for the solution defined in the YAML file. This id will be used to track outcomes produced from running or deploying your solutions.
  - The `id` needs to be in [snake case](https://www.pluralsight.com/blog/software-development/programming-naming-conventions-explained#:~:text=snake_case%20is%20a%20variable%20naming). It can have alphanumeric characters.
- `description` is a textual description of your solution and what you are trying to do.
- `environment_config_overrides` this config enables you to override you FFModel environment configurations in case you need different configs for this solution.
  - It is strongly discouraged to pass secrets as overrides. Please ensure that you are handling your secrets in a secure manner via KeyVault or otherwise.
- `project_root` points to the root of your local workspace, this is required to consume your components when running the solution.
- `experimentation` holds the following experimentation specific configurations:
  - `data` is a [data config](#data-config) config that points to your evaluation data set locally or in the cloud.
  - `reader` is your [reader component](./solution_components.md#reader-components) to load your dataset declared in the `data` config.
  - `writer` is **an optional** [writer component](./solution_components.md#writer-components) to capture the data models at the end of the experiment run and dump them.
- `inference` holds the following inference specific configurations:
  - `reader` is **an optional** [reader component](./solution_components.md#reader-components) to process the incoming inference requests to a format accepted by your data models.
  - `writer` is **an optional** [writer component](./solution_components.md#writer-components) to capture the data models at the end of the inference flow and dump them.
- `components` holds the definition of your solution as a list of FFModel components. The components will be executed in the order they are listed. More on this [later](#component-config).

Here is a [bare bone solution config template](../../experiments/templates/solution_config_template.yaml):

```yaml
id: "my_solution_id"
description: "This is an example solution description"

environment_config_overrides:
  AML_ENVIRONMENT_NAME: ffmodel

project_root: "relative/path/to/project_root"

# experiment-specific configs
experimentation:
  data:
    file_path: "path/to/data/file"
  reader:
    name: "components.readers.jsonl"
  writer:
    - name: "components.writers.mywriter"
      args:
        output_path: "my/outputs/path"

# inference-specific configs
inference:
  reader:
    name: "components.readers.jsonl"
  writers:
    - name: "components.writers.myfirstwriter"
    - name: "components.writers.mysecondwriter"

# The solution definition
components:
  - name: "<<component1.module.path>>"
        args: {}
        supporting_data: {}
  - name: "<<component2.module.path>>"
        args: {}
        supporting_data: {}
```

### Data Config

A data config represents a data file that you need to use in your solution.
It has the following configurations:

- `file_path` is a required configuration that holds the dataset file path.
  - If your file is local, then the path is relative to where you are running the experiment from.
  - If you are referencing an AML dataset, the file path is where on your local machine FFModel downloads the dataset to.
- `aml_dataset_name` if your dataset has been uploaded to AML, it can be consumed by sharing your AML dataset name.
- `aml_dataset_version` the version of the AML dataset to consume.

Here is an example data config, as defined in the experimentation section:

```yaml
experimentation:
  data:
    file_path: ./my/exp/data.jsonl
    aml_dataset_name: my_aml_dataset
    aml_dataset_version: "1"
  ...
```

This indicates that the file within `my_aml_dataset` version `1` will be downloaded to `./my/exp/data.jsonl`.

### Environment Configs

Check the [environment configs guide](./environment_configs.md) for additional information on environment configs.

### Component Config

The solution is defined as a sequence of components, a component is configured using the following configurations:

- `name`: is the Python module path for your component. The module path needs to be relevant to the `project_root` config (e.g., `components.stitchers.sql`).
- `args`: a list of arguments that the components needs in order to run. These are defined as part of the component's implementation. FFModel will capture them and pass them as a dictionary to the component's `_post_init` method.
- `supporting_data`: a list of supporting data files that the component needs. This is a dictionary of strings to [data configs](#data-config).

You can check the [components guide](./solution_components.md) to learn more about components.

## Executing your Solution

FFModel provides orchestrators that take in your solution config yaml file along with an [environment config](./environment_configs.md) file to execute or deploy your solution.
Before getting started with this section, please create an `.ffmodel.env` environment config file.
You can execute and deploy your solution via the FFModel SDK or the CLI. The following sections cover each of those scenarios.

Make sure your project root doesn't have any files with the same name as the following experimentation execution code files, since they will get copied over:

- ffmodel_execute_reader.py
- ffmodel_execute_component.py
- ffmodel_execute_writer.py

### Execute Locally

To run the solution locally you need to import the `orchestrator` module and use the `execute_experiment_on_local` function.
You can check the [run experiment notebook template](../../experiments/templates/run_experiments_template.ipynb) for an example.
Here is an example:

```python
from ffmodel.core import orchestrator

# Update the parameters to point to your solution config and environment config files.
data_models = orchestrator.execute_experiment_on_local(
    "./path/to/solution/config.yaml",
    "./path/to/.ffmodel.env"
)
```

If you are planning to use the CLI, you need to use the `ffmodel local` option. Check the help for the CLI on the parameters needed `ffmodel local --help`.
Here is an example:

```bash
ffmodel local "./path/to/solution/config.yaml" "./path/to/.ffmodel.env"
```

### Execute and Deploy on Azure Machine Learning (AML)

Please refer to the [infrastructure](../infrastructure/infrastructure.md) guide to set up your AML workspace.
When running FFModel from your local workspace, FFModel relies on you as a user to authenticate with Azure.
You need to be logged into Azure from your local workspace whenever you need to run against AML.

When running experiments on AML, make sure your solution configs don't repeat the same component (referenced by its name) more than once. The current caching mechanism when packaging and uploading the solution components to be run on AML only processes the first occurrence of a component and throws an error for the rest. For example, if you list multiple `static_context` components in a row with the intention to format the content, the orchestrator will fail. (This is being tracked in [issue #249](https://github.com/microsoft/ffmodel/issues/249)) on GitHub. This is not an issue when running the experiments locally.

Follow these steps to connect to Azure:

1. Open your terminal.
2. Log into Azure using the Azure CLI by executing `az login` in your terminal. Follow the browser prompts until you've successfully logged in.
   - Note: If your subscription lives in a tenant different from your default tenant, be sure to execute `az login --tenant <tenant-id>` instead.
3. Set the subscription to your AML workspace subscription `az account set -s <subscription-name>` or `az account set -s <subscription-id>`.
4. Verify the correct subscription was selected by executing `az account show`. You should see information about your subscription in the terminal output.

#### Experiment with Solutions on AML

To experiment with your solution on AML, you need to import the `orchestrator` module and use the `execute_experiment_on_aml` function.
Here is an example:

```python
from ffmodel.core import orchestrator

# Update the parameters to point to your solution and environment config files.
data_models = orchestrator.execute_experiment_on_aml(
    "./path/to/solution/config.yaml",
    "./path/to/.ffmodel.env"
)
```

If you are planning to use the CLI, you need to use the `ffmodel aml` option.
Check the help for the CLI on the parameters needed `ffmodel aml --help`.
Here is an example:

```bash
ffmodel aml "./path/to/solution/config.yaml" "./path/to/.ffmodel.env"
```

In both scenarios, your environment config file needs to have all [AML required](./environment_configs.md#ffmodel-pre-defined-configs) configurations.

#### Deploy Solutions to an AML Managed Endpoint

To deploy the solution on AML you need to import the `deployment_orchestrator` module (`from ffmodel.core.aml import deployment_orchestrator`) and use the `deploy_solution` function. Make sure your project root doesn't have any files with the same name as the inference code file (`ffmodel_execute_inference.py`), since this will get copied over while preparing the files to execute on AML.

An example:

```python
from ffmodel.core.aml import deployment_orchestrator
    
deployment_orchestrator.deploy_solution(
    solution_config_path="./path/to/solution/config.yaml",
    environment_config_path="./path/to/.ffmodel.env",
    endpoint_name="your-endpoint-name",
    deployment_name="your-deployment-name",
    deployment_description="your-deployment-description",
    sku_type="Standard_DS1_v2",
    traffic_volume=100,
)
```

If you are planning to use the CLI, you need to use the `ffmodel deploy` option.
Check the help for the CLI on the parameters needed `ffmodel deploy --help`.
Here is an example:

```bash
ffmodel deploy "./path/to/solution/config.yaml" "./path/to/.ffmodel.env" "your-endpoint-name" \
"your-deployment-name" "your-deployment-name" "your-deployment-description" "Standard_DS1_v2" 100
```
