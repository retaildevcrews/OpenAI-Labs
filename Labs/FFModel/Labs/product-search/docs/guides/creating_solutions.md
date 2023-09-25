# Creating an FFModel Solution

In this guide, we will walk you through creating your first FFModel solution: an experiment that uses a GPT model to generate Python code.

## Pre-requisites

- You have a virtual environment or a conda environment with FFModel installed.
- You have [Jupyter notebook](https://jupyter.org/) installed.
- You have access to an OpenAI service.

## Creating the Solution

Scenario: Let's create a solution that mostly uses the default FFModel components, but with a custom evaluator.
Our evaluator will check if the code that is generated is non-empty and syntactically valid Python.

### Creating a Python Syntax Evaluator

1. Start with copying the [`components/component_template.py`](../../components/component_template.py) to `components/evaluators/python_syntax.py`.
   - Ensure that the directories you create have an empty `__init__.py` file in the directory as well.
2. Update the data model import in the template to import the `ExperimentDataModel` and update your component signature as well, this is needed as evaluators only run during experimentation. Here is the `ExperimentDataModel` import:

   ```python
   from ffmodel.data_models.base import ExperimentDataModel
   ```

3. Next, we can implement the logic (body of the `execute` method) for calculating our metrics,
make sure to update the `execute` method signature to also use the `ExperimentDataModel` data model. Here is the code:

   ```python
   def execute(self, data_model: ExperimentDataModel) -> ExperimentDataModel:
        """
        Executes the component for the given data model and returns an
        updated data model.
        """
        
        # get the model output
        completions = data_model.model_output.completions

        results = { k: [] for k in ["non-empty", "syntax-valid"]}

        # For each completion check if its valid Python or not.
        for completion in completions:
            results["non-empty"].append(int(len(completion) > 0))
            try:
                ast.parse(completion)
                results["syntax-valid"].append(1)
            except:
                results["syntax-valid"].append(0)

        data_model.experiment_metrics[self.get_id()] = results

        return data_model
   ```

   - First, we are using the `ast` module for syntax validation, so we need to add `import ast` to the top of the file
   - Completions is a list, so all of our metrics are a list, where each value corresponds to the completion in that position
   - Evaluator metrics are numeric, which is why we are converting our booleans to 1 or 0 for true and false respectively
   - `self.get_id()` is a method on the BaseComponent which returns the identifier for the given component. It is `{block_name}.{component_name}`

4. Add a new folder for your experiment under the `experiments` folder:
   - Create a subdirectory in your experiment folder for `data`.
   - Copy the [`examples/nl2python/sample_datasets/nl2python_dataset.jsonl`](../../examples/nl2python/sample_datasets/nl2python_dataset.jsonl) file to the `data` folder.
   - Create a subdirectory in your experiment folder for `configs`
   - Copy the [`experiments/templates/solution_config_template.yaml`](../../experiments/templates/solution_config_template.yaml) to the `configs` folder and rename it as needed.

5. The next few steps will build up the solution config file. Start with modifying the `experimentation` section for the data we want to run through the experiment.

   - Here we are pointing to the python_example dataset
   - Note that the path is relative to where we are going to run it from
   - Data should be jsonl formatted and requires fields `user_nl` and `completion`
   - We specify the jsonl reader to load the data into data models
   - We specify the jsonl writer, which will write a json serialization of all the data models to a jsonl file at the end of the experiment

      ```yaml
      experimentation:
         data:
            file_path: data/python_examples.jsonl
         reader:
            name: "components.readers.jsonl"
         writers:
             - name: "components.writers.jsonl"
               args:
                  output_path: "outputs/nl2python_output.jsonl"
      ```

6. For this experiment, we do not need any pre-processors. We will just call the LLM and evaluate the completions. First, update the block id and description in your config file. Then add the following components:

    - Add the FFModel default stitcher to prepare the prompt `components.stitchers.python`. No arguments are needed.
    - Now, we can add the LLM call using FFModel's default model caller `components.model_callers.openai`. This will send your prompt to one of (Azure) OpenAI's LLMs (depending on your environment config and component args) and store the completions in the data model (`model_output`)
      - You need to use a model/engine that was deployed to your Azure OpenAI Service. Here is an example that is using `text-ada-001`:

      ```yaml
      - name: "components.model_callers.openai"
           args:
             engine: "text-ada-001"
             stop:
               - "#"
             temperature: 0.0
             max_tokens: 256
             top_p: 1.0
             best_of: 1
      ```

    - Then we need to add the custom evaluator that you created in step 3, `components.evaluators.python_syntax`. Like with the stitcher, this customer evaluator component has no required arguments.

7. Then, you need to define an [environment config](./environment_configs.md) to pass in your OpenAI endpoint and key.
   - Create a new `.ffmodel.test` file, this can be used by all experiment, so you can put it at the root of your repo.
   - Add two configs:
     - `OPENAI_ENDPOINT` that has the endpoint to your OpenAI service.
     - `OPENAI_API_KEY` that has the key to authenticate with your service.

8. Now, we are ready to execute the experiment from a Jupyter notebook. Copy the [`experiments/templates/run_experiments_template.ipynb`](../../experiments/templates/run_experiments_template.ipynb) to your experiment folder and rename it as you see fit.
   - The template notebook explains how to use it, follow the steps and run the experiment.
   - Make sure to use your virtual/conda environment to run the notebook.

9. To visualize the results, copy the [experiments/templates/result_analysis_template.ipynb](../../experiments/templates/result_analysis_template.ipynb) to your folder.
   - The template notebook explains how to use it, follow the steps and visualize the outputs.
   - Make sure to use your virtual/conda environment to run the notebook.
