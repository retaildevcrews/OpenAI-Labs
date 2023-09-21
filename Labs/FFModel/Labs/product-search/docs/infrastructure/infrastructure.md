# Setting up your cloud infrastructure

This document goes over integrating FFModel with your cloud resources.
If you run into any issues, please cut us an issue in the [FFModel GitHub repo](https://github.com/microsoft/ffmodel).
This is currently a private repo, so if you do not have access to it, please [contact us](mailto:aias-ffmodel@microsoft.com).

## Pre-requisites

- Azure Subscription - [Create one here](https://azure.microsoft.com/en-us/free/)

  - You or someone in your organization will need to have permissions to work with Azure Active Directory (e.g. the ability to set up permissions and access policies).
  - Be sure to note your subscription id or the name of your subscription. This will be referenced later on.

- Azure CLI (at least version 2.34.0) - [Install documentation](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
  - Azure Machine Learning Extension for Azure CLI - [Install and set up for the CLI (v2) - Azure Machine Learning](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli?tabs=public)

## Authenticating with Azure

For authentication to AML and Key Vault, FFModel uses the [DefaultAzureCredential](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python).
Our recommended method for authenticating is by using the Azure CLI.
Please follow [How to install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) to install it on your machine.
Once installed, run `az login` to sign into your Azure account.

If you have multiple tenants and/or subscriptions, login to a tenant using `az login --tenant <<tenant-id>>`.
Once logged in, you can set your default subscription using `az account set -s <<subscription id>>`.

**Note:** If you are not using the environment variable method (found in [EnvironmentCredential Class](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.environmentcredential?view=azure-python)) of signing in, then having any of the following environment variables set will cause an error: "AZURE_TENANT_ID", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_AUTHORITY_HOST".
To fix, unset all the variables to use the az cli for auth.

FFModel has disabled use of the VS Code authentication method due to a bug in VS Code where it does not refresh the access token once it is expired.
Also, we have disabled the interactive login mechanism because this code runs in AML and will cause the job to hang while waiting for user input if it were not disabled.

## Setting up Azure OpenAI Service

The Azure OpenAI service gives you access to the OpenAI models (i.e., GPT3, Codex).
You can follow [this page to get access to the service](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/overview).
Note that you will need to go through a few steps to onboard to Azure OpenAI, which are detailed in link.

Once you've created your Azure OpenAI resource, be sure to note your `Keys and Endpoints` for the resource, as they will be used in later setup steps.
Follow the steps linked [here](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/quickstart?pivots=programming-language-python#retrieve-key-and-endpoint) to identify your Azure OpenAI key and endpoint.

Note that to use the Azure OpenAI instance, you will need to prepare model deployments via the Azure OpenAI `Model Deployments` blade of the Azure Portal or via the [Azure OpenAI Studio](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model).
For the examples available to you in this starter project, be sure to prepare two deployments ahead of time, using the following configurations:

| Model Deployment Name     | Model                     |
| ------------------------- | ------------------------- |
| `text-similarity-ada-001` | `text-similarity-ada-001` |
| `code-cushman-001`        | `code-cushman-001`        |

## Setting up your Azure Machine Learning (AML) workspace

FFModel natively integrates with Azure Machine Learning (AML) to run your solution experiments on the cloud.
Also, it can deploy your solution for inference using [AML Managed Endpoints](https://learn.microsoft.com/en-us/azure/machine-learning/concept-endpoints?view=azureml-api-2).
This section provides guidance on how to provision your AML workspace and set it up for FFModel.

Please read this section in its entirety before creating new resources.
The steps in this sections will rely on the Azure Portal and the Azure CLI to create the infrastructure.
This way you can follow the instructions on any operating system.
The guidance here assumes you are using a bash terminal.
There are a couple of key values that will be reused throughout this sections, those are being tracked as environment variables, be sure to populate them when you have the values.

### Set up your AML workspace

You can follow this [link](https://learn.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources?view=azureml-api-2) to create your AML workspace, if you don't have one already.

Set the following environment variables:

```bash
# The subscription id
export sub_id=
# The resource group name
export rg=
# The AML workspace name
export aml_ws=
```

### Handling Secrets

FFModel relies on [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/overview) to handle your secrets (i.e., authentication keys).
In the following sections, you will be creating resources and need to track their secrets in Key Vault.
Check this [link](https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-cli#add-a-secret-to-key-vault) for guidance on creating and retrieving secrets from Key Vault.

If you are creating a new AML workspace, you can create a Key Vault resource through that process.
This ensures that your AML workspace is configured to consume secrets from its key vault.
If using the AML Key Vault instance, you need to grant your Azure account access by following the steps in this
[link](https://learn.microsoft.com/en-us/azure/key-vault/general/assign-access-policy?tabs=azure-portal).
Grant yourself permissions for all of the `Secret Management Operations`.

Then, set the following environment variable:

```bash
# Key vault instance name. This can be the AML Key Vault instance.
export kv=
```

FFModel gives access to pulling secrets from a Key Vault through the `ffmodel.core.environment_config.EnvironmentConfigs` class.
To enable, the secrets with the same name as the ones in your `~/.ffmodel` file should be uploaded to an Azure Key Vault.
Please note that Key Vault does not support `_` in secret names, so replace the Key Vault secret names with `-` in Key Vault.
The `EnvironmentConfigs` class will automatically do the replacement for you when accessing.

Note that for any custom secrets/configs provided via an environment config file at the time of experimentation or deployment on AML, those secrets are required to be located in Key Vault for AML to be able to to access them.
FFModel will not copy any environment configs beyond those required for AML to successfully run experiments or execution inference solutions.
See `ffmodel.core.enviornment_config.EnviornmentConfigs` class and the respective variable groups `AML_EXPERIMENTATION_CONFIG_GROUP` and `AML_INFERENCE_CONFIG_GROUP` to determine which configs will be captured and which will be excluded (and thus should be stored in your Key Vault).

### Create a User-Assigned Managed Identity

FFModel depends on a User-Assigned Managed Identity (MI) to authenticate set permissions.
This MI is required for deploying FFModel solutions to AML Managed Endpoints.
To set one up:

```bash
# The Azure Managed Identity's Client Id
mi_client_id=$(az identity create -n ffmodel-mi -g $rg --query clientId -o tsv | tr -d '\r')
```

### Create a compute cluster

You need to have a compute cluster to run your experiments on.
You can follow this [link](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-identity-based-service-authentication?view=azureml-api-2&tabs=cli#compute-cluster) to create a new compute cluster.
**Be sure to assign a system assigned managed identity.** A sample `create-cluster.yaml` file is included to get you started, so feel free to edit that file and run:

```bash
# Run this only after updating create-cluster.yaml
az ml compute create -f create-cluster.yaml --resource-group $rg --workspace-name $aml_ws
```

If you have secrets stored in Key Vault, we need to configure the managed identity of the compute cluster for your experiment to have access to reading.
**This must be done per compute cluster.**

1. If you do not have a managed identity for your compute cluster: [Set up a managed identity](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-attach-compute-cluster?tabs=azure-studio#set-up-managed-identity)
2. Give permissions to read secrets to the managed identity in key vault: [Assign a Key Vault access policy](https://learn.microsoft.com/en-us/azure/key-vault/general/assign-access-policy?tabs=azure-portal). You only need to give the `Get` permission for secrets.

### Configure Key Vault Access Policy for Azure Machine Learning Compute Resource

When running an experiment on AML, your compute needs to have access to your key vault to access its secrets.
Do the following to enable this connection:

1. Begin from the terminal where you're connected to Azure via the Azure CLI.
2. Store the cluster's name in an environment variable:

    ```bash
    # The AML cluster name
    export aml_cluster=
    ```

3. Execute the following script to configure the Key Vault resource to have an access policy for the identity of the Azure Machine Learning Compute resource (with permissions to get secrets):

    ```bash
    # Identify the Object Id of the Azure Machine Learning Compute resource
    aml_compute_object_id=$(az ml compute show --name $aml_cluster -g $rg -w $aml_ws --query "identity.principal_id" | tr -d '\r' | xargs)

    # Ensure you got the object id. If this prints an empty string, this means you did not set up a
    # system assigned managed identity to your compute cluster. Please refer to "Create a compute
    # cluster" section.
    echo $aml_compute_object_id

    # Set access policy on key vault for your identity with secret get permissions
    az keyvault set-policy --name $kv --resource-group $rg --object-id $aml_compute_object_id --secret-permissions get
    ```

### Configure Role Assignments for Managed Identity

The Managed Identity (MI) you created earlier needs to have access to the AML Storage Account, AML workspace and key vault secrets.

Execute the following script to configure the Role Assignments (aka RBAC) to the MI.

```bash
# Identify the name of the storage account resource you want to update
storage_account_name=$(az resource list --query "[?type=='Microsoft.Storage/storageAccounts'].name" -g $rg -o tsv | tr -d '\r')

# Configure Storage Blob Data Contributor role
az role assignment create --assignee $mi_client_id --role "Storage Blob Data Contributor" --scope "/subscriptions/$sub_id/resourcegroups/$rg/providers/Microsoft.Storage/storageAccounts/$storage_account_name"

# Identify the name of the container registry resource you want to update
container_registry_name=$(az resource list --query "[?type=='Microsoft.ContainerRegistry/registries'].name" -g $rg -o tsv | tr -d '\r')

# Configure Container Registry Contributor role
az role assignment create --assignee $mi_client_id --role "Contributor" --scope "/subscriptions/$sub_id/resourcegroups/$rg/providers/Microsoft.ContainerRegistry/registries/$container_registry_name"

# Configure AzureML Data scientist role
az role assignment create --assignee $mi_client_id --role "AzureML Data Scientist" --scope "/subscriptions/$sub_id/resourcegroups/$rg/providers/Microsoft.MachineLearningServices/workspaces/$aml_ws"

# Configure Managed Identity Operator role
az role assignment create --assignee $mi_client_id --role "Managed Identity Operator" --scope "/subscriptions/$sub_id"

# Set access policy on key vault with secret get permissions
az keyvault set-policy --name $kv --resource-group $rg --object-id $mi_client_id --secret-permissions get
```

#### Configure Role Assignment on Azure Machine Learning Workspace for Azure Machine Learning Compute Resource

1. Open your terminal and log into Azure if you haven't already:

    ```bash
    az login
    az account set -s $sub_id
    ```

2. Assign the "AzureML Data Scientist" role to the Azure Machine Learning compute resource.

    ```bash
    # Define the role assignment to use the custom role FFModel Experiment Compute
    az role assignment create --assignee "$aml_compute_object_id" --role "AzureML Data Scientist" --scope "/subscriptions/$sub_id/resourcegroups/$rg/providers/Microsoft.MachineLearningServices/workspaces/$aml_ws"
    ```

3. Navigate to the custom role definition in `ffmodel/roles/ffmodel_experiment_compute.json` and replace the placeholders for `<ffmodel-subscription-id>` and `<ffmodel-resource-group>` with the values stored in the variables `$sub_id` and `$rg` respectively.
4. From the `ffmodel/roles/` directory, create a custom role for compute resources by executing the following script:

    ```bash
    # Prepare a Custom Role for the Azure Machine Learning Compute Resource
    az role definition create --role-definition ffmodel_experiment_compute.json
    ```

5. Wait a few minutes for the role to become available for use, then proceed to create a role assignment for the Azure Machine Learning compute resource using the custom role definition created in step 3 by executing the following script:

    ```bash
    # Retrieve object id of AML compute resource's identity
    # Define the role assignment to use the custom role FFModel Experiment Compute
    az role assignment create --assignee "$aml_compute_object_id" --role "FFModel Experiment Compute" --scope "/subscriptions/$sub_id/resourcegroups/$rg/providers/Microsoft.MachineLearningServices/workspaces/$aml_ws"
    ```

If you get the error message "Role 'FFModel Experiment Compute' does not exist.", wait a few minutes and then retry executing the last role assignment command in the script.

### Updating the Azure Machine Learning environment

To update the AML environment with the latest version of FFModel, you need to
first install the [Azure CLI ML extensions]. Then, run the `deploy-env.sh`
script:

```bash
# Log into Azure
az login

# Set your default subscription
az account set -s $sub_id

# Deploy the environment
# This accepts the same arguments as `az ml environment create`
./deploy-env.sh --name <environment-name> --resource-group $rg --workspace $aml_ws
```

[azure cli ml extensions]: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli?tabs=public

### Create an environment on AML

Create an environment configuration file that includes `AML_SUBSCRIPTION_ID`, `AML_RESOURCE_GROUP` and `AML_WORKSPACE_NAME` variables, and execute the CLI command by providing the path to it, for example:

```bash
ffmodel aml_env --environment-name=ffmodel --environment-config-path=~/.ffmodel
```

Alternatively, these same environment configurations can exist as OS environment variables, which will be used by default if not `environment_config_path` is provided.

Check the help for the CLI on the parameters needed `ffmodel aml_env --help`.

### Authenticate with AML using a Service Principal

If you have a use case where you need to do a service to service authentication with AML, you should not be using your credentials, instead, you need to utilize a [service principal](https://learn.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals?tabs=browser).
For example, setting up a CI pipeline to test experiments on AML.
To do this, follow these steps:

1. Navigate to the Azure Portal
2. Check to see if you have sufficient permissions to set up a Service Principal by following the instructions here: [Check Azure Active Directory Permissions](https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#check-azure-ad-permissions). Note that if you do not have sufficient permissions, you will likely need to get into touch with your Azure administrator to set one up for you.
3. Create a new Service Principal with a name of your choice by following the instructions here: [Create a New Service Principal](https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#register-an-application-with-azure-ad-and-create-a-service-principal)
4. To authenticate when using the new Service Principal, create a secret following the instructions here: [Create a New Secret](https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#option-2-create-a-new-application-secret). Be sure to copy the secret **value** because you won't be able to retrieve the key later. To store it securely, you can create a new secret in your [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts), your AML Workspace gets provisioned with a Key Vault instance by default.
5. Navigate to the overview page for the Service Principal/App Registration and copy the values for the `Application (client) ID` and the `Azure Tenant ID`.
6. Then using [the Azure CLI](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-cli),
grant your service principal the [`AzureML Data Scientist`](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-assign-roles?view=azureml-api-2&tabs=labeler#default-roles) role using the following command. Replace the `<place holders>` with your respective values:

 ```bash
 az role assignment create --assignee "<Client ID>" --role "AzureML Data Scientist" --scope "/subscriptions/$oasis_sub_id/resourcegroups/$oasis_rg/providers/Microsoft.MachineLearningServices/workspaces/$aml_workspace_name"
 ```

Use this service principal to authenticate a non-Azure resource to integrate with AML.
For example, if you are using a GitHub codespace, you need to use this service principal to [login into](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli#sign-in-with-a-service-principal) your Azure subscription to run your AML experiments.
