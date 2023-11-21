# Deploy Azure Cognitive Search Loaded With Sample Data Set


## Prerequisites

- Azure subscription with permissions to create:
  - Resource Groups, Service Principals, Key Vault, Cosmos DB, Azure Container Registry, Azure Monitor, App Service or AKS
- Bash shell (tested on Visual Studio Codespaces, Mac, Ubuntu, Windows with WSL2)
  - Will not work in Cloud Shell or WSL1

### Check for latest Azure CLI Upgrades

```bash
az upgrade
```

## Setup

### Login to Azure and select subscription

```bash

az login

# show your Azure accounts
az account list -o table

# select the Azure subscription if necessary
az account set -s MCAPS-43649-AUS-DEVCREWS

```

### Choose a deployment name and location

```bash

export deploymentName=crew512upskill
export location=southcentralus

```

### Create Resource Group and Resources

```bash

az group create -n "rg-$deploymentName" -l $location

az search service create --name "search-$deploymentName" --resource-group "rg-$deploymentName" --sku Standard --partition-count 1 --replica-count 1

az storage account create --name "storage$deploymentName" --resource-group "rg-$deploymentName"

```
