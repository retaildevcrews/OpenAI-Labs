# NL2Python Example

This folder contains examples for a natural language to Python use case,
where the user's input is a description of what they want code for and the output is Python code.

The key features of this example are:

* The use of a dynamic few shot selection provided by the [few shot embedding component](../../components/pre_processors/few_shot_embedding.py).
Please see the few shot example section of [prompt_engineering.md](../../docs/llm_guides/prompt_engineering.md) for more details on few shot selection.
* Deploying the solution to an AML managed endpoint for inference.

## Contents

* nl2python_experiment.ipynb - Start here to run the experiment on your local machine
* ExampleDeploymentAML.ipynb - Deploy your solution to an AML managed endpoint to create an HTTP consumable inference endpoint
* nl2python_solution.yaml - The solution configuration for the example
* sample_datasets - This folder contains the example dataset used in experimentation as well as the files needed to create the few shot bank used by the few_shot_embedding component
* outputs - Directory to store the output files of your experiment runs
