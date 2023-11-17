# RAG Vectorstore Setup Guide

This guide provides instructions on how to set up the RAG Vectorstore using open source and free approaches, as an alternative to Azure Cognitive Search. The instructions and examples provided in this guide are based on the notebooks and files available in this folder.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)

## Introduction

The RAG Vectorstore is a powerful tool for semantic search and retrieval. It allows you to index and search large collections of documents using advanced natural language processing techniques. This guide will walk you through the process of setting up the RAG Vectorstore using open source and free approaches.

## Prerequisites

Before you begin, make sure you have the following prerequisites:

- Python 3.x installed
- Jupyter Notebook installed
- Setup your environment variables to access OpenAI and AZURE services in this [your.env](./your.env)
- Required Python libraries (specified in the [requirments.txt](./requirements.txt) file)

## Installation

To install the RAG Vectorstore, follow these steps:

1. Clone or download the repository to your local machine.
2. Open the Jupyter Notebook environment.
3. Open the the two notebook [azure](./azure-search.ipynb) and [langchain](./langchain.ipynb)
4. Follow the instructions in the notebook to install the required dependencies and set up the RAG Vectorstore.

## Usage

Once the RAG Vectorstore is set up, you can use it for various tasks, such as:

- Indexing documents
- Searching for similar documents
- Extracting semantic information from documents

Refer to the notebooks in this folder for detailed examples and usage instructions.

## Examples

This folder contains several example notebooks that demonstrate the usage of the RAG Vectorstore on [HTML](./test_doc.html) and [PDF](./test_doc.pdf)  versions of the governement holiday schedule. You can find the following examples:

- `azure-search.ipynb`: Using azure cognitive search.
- `langchain.ipynb`: Using langchain and pinecone.

Feel free to explore these examples and adapt them to your specific use case.