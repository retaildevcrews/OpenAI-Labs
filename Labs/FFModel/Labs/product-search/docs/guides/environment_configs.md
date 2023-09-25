# Environment Configurations

FFModel solutions are executed within the context of an environment,
an environment configuration holds the necessary configurations to integrate your solution with your environment.
Example dependencies are your Azure OpenAI service, Azure Machine Learning (AML) workspace, or an Azure Key Vault instance that holds your secrets.

## Sources and Precedence

The following is a list of ways you can provide environment configurations to your solution.
The list shows the sources precedence from highest to lowest:

1. The `environment_config_overrides` defined in your solution config.
2. The environment config file provided during orchestration.
3. The environment variables from your operating system.
4. The key vault secrets.

### Defining an Environment Config File

You can create a key-value pairs files to pass your configurations to FFModel.
Here is an example config file that defines two configs:

```sh
KEY_VAULT_URL="https://my-imaginary-kv.vault.azure.net/"
AZURE_OPEN_AI_KEY="kv-open-ai-secret"
```

This file points FFModel to a key vault instance and passes the secret name for the OpenAI key.
When you call `EnvironmentConfigs.getConfig('AZURE_OPEN_AI_KEY')`, FFModel will retrieve the corresponding secret, following the EnvironmentConfigs precedence logic outlined earlier.

## Accessing Environment Configs

To access your configurations, you need to import the `EnvironmentConfigs` module:

```python
from ffmodel.core.environment_config import EnvironmentConfigs
```

The `EnvironmentConfigs` module acts as a singleton, if you are using an FFModel orchestrator, it would be already loaded with your configurations due to that.
If you are using it in your notebooks to parse a config file, make sure to initialize it.

You can retrieve environment configurations via:

- The `EnvironmentConfigs.getConfig('<environment-config-name>')` function that will attempt to retrieve your config from the sources listed earlier. If the config is not found, it will raise a `KeyError` exception and fail the execution.
- Or the `EnvironmentConfigs.safeGetConfig('<environment-config-name>')` that will attempt to retrieve the config and return `None` if not found.

## Handling Secrets

FFModel natively integrates with Azure Key Vault to consume secrets securely.
To use this feature you need to provide an environment config `KEY_VAULT_URL` that holds a URL to your key vault instance, upload your secret to key vault, and then retrieve it using the `EnvironmentConfigs` module.

## Naming Convention

We recommend using [screaming snake case](https://en.wikipedia.org/wiki/Snake_case) to name your environment configs.
The exception to this rule will be your secrets published to Key Vault, as [its naming convention](https://azure.github.io/PSRule.Rules.Azure/en/rules/Azure.KeyVault.SecretName/#:~:text=The%20requirements%20for%20Key%20Vault,unique%20within%20a%20Key%20Vault.) does not accept underscores.
To work around this limitation, when the `EnvironmentConfigs` module checks for secrets in Key Vault, it automatically converts underscores/`_` to hyphens/`-` (i.e., `OPENAI_API_KEY` will become `OPENAI-API-KEY` when `EnvironmentConfigs` checks Key vault).
This way, you can have the same config names in your environment or in Key Vault.

## FFModel Pre-defined Configs

Depending on what you are experimenting with and using within FFModel, you may need to provide/use specific pre-defined configurations.
You can find a sample `.ffmodel` config in the [`experiments/templates`](../../experiments/templates/.ffmodel.sample).
This table captures key environment configurations that you may want to consider:

| Config Name | Description | Usage | Default value |
| - | - | - | - |
| `KEY_VAULT_URL` | The URL for the key-vault instance that has your environment secrets. | Executing or deploying a solution on AML. | |
| `AML_WORKSPACE_NAME` | Your AML workspace name | Executing or deploying a solution on AML. | |
| `AML_SUBSCRIPTION_ID` | The subscription id for your AML workspace. | Executing or deploying a solution on AML. | |
| `AML_RESOURCE_GROUP` | The resource group that has your AML workspace. | Executing or deploying a solution on AML. | |
| `AML_COMPUTE` | Your AML compute cluster to use during experimentation. | Executing or deploying a solution on AML. | |
| `AML_ENVIRONMENT_NAME` | The FFModel AML environment used during experimentation and inference | Executing or deploying a solution on AML. | ffmodel |
| `AML_ENVIRONMENT_VERSION` | The version of the `AML_ENVIRONMENT_NAME`, FFModel will use the latest if not provided. | Executing or deploying a solution on AML. | latest |
| `AZURE_CLIENT_ID` | The client id for the Azure Managed Identity (MI) used by inference to authenticate with other Azure resources | Deploying a solution on AML. | |
| `AZURE_MI_NAME` | The name of the Azure Managed Identity (MI) used by inference to authenticate with other Azure resources | Deploying an experiment on AML. | |
| `OPENAI_ENDPOINT` | Points to your OpenAI service's endpoint. | Executing or deploying a solution on AML. | |
| `OPENAI_API_KEY` | The key vault secret id holding your key to access the OpenAI service. | Executing or deploying a solution on AML. | |
| `FFMODEL_LOGGING_ENABLED` | The config name to enable or disable logging into Azure Monitor. | Executing or deploying a solution on AML. | true|
| `FFMODEL_METRICS_ENABLED` | The config name to enable or disable logging metrics into Azure Monitor. | Executing or deploying an experiment on AML. | true|
| `FILE_LOGGING_ENABLED` | The config name to enable or disable file logging. | Executing or deploying a solution on AML. | false |
| `FFMODEL_LOGGING_LEVEL` | The config name to set the logging level. | Executing or deploying a solution on AML. | INFO |
