# Hyperparameter Sweep

## Introduction

Glossary:

- Hyperparameter is a parameter whose value is used to control the training process and optimize the models.
- Hyperparameter sweep (also called "tuning"): choose the best combination of hyperparameter values that gives the best results

Common Hyperparameter Sweeping Methods:

- Grid: exhaustive searching
- Random
- Other optimizations/variations of them

In FFModel, a sample hyperparameter is the `count` in the session selector component to choose the range of sequences in a session to select. Other examples are the parameters for the OpenAI API (e.g., `model`, `temperature`, `top_p`) or any combinations of them that are passed through the openai model caller component.

## Goal

This document outlines the hyperparameter sweeping functionalities that FFModel will support and the syntax in the solution config to provide the sweeping options.

## User flow

Users will go through the following steps when using this capability:

1. Prepare a solution config **template** file that defines the sweeping option
1. Run the orchestrator that parses the solution config
1. Get back **a set of fully defined solution config files** to evaluate and run at their own schedule

## Scoping

Assumptions:

- Users are expected to define the order of the components in a solution config.

In scope:

- Define the syntax for the solution config templates
- Validation
  - The existence of components in the solution config templates
  - The existence of the code snippets referenced in the solution config templates
- Reference code snippets (.yaml files) in the solution config templates to allow code reusability
- Sweep at components, arguments and supporting data level. Sweeping options are provided by introducing a `sweep` keyword and a list of options.
- Sweep comprehensively over a range of user provided hyperparameter options.
  - The tool will output an exhaustive list of solution configs without further optimization or filtering.
- Store the generated solution configs in user's local directory for them to validate, evaluate and run.

Out of scope:

- Validate the argument and supporting data of the components.
  - The tool will not validate the type and value of the component arguments and the existence and the content of the supporting data, which is consistent with the existing experiment orchestrators. Users are expected to provide valid arguments and files. Providing such validation will require modifying the input data model to define the validation rules.
  - Due to the complexity of defining the evaluation criteria (the feasibility of running an experiment, and its expected performance), the evaluation will be done by users manually and the generated solution configs will be named and grouped logically to facilitate the process.
- Run the generated solution configs automatically.
  - Due to the cost consideration, potential resource constraints, and possibly a large number of output generated, the tool will not automatically trigger the experiments but instead, provide the solution configs for users to run on their own pace. Currently, our data scientists run experiments in batches, with the intention to figure out the optimal values for one or a few variables at once, before proceeding to optimize the rest of the variables, so we don't see the value of running all the experiments upfront.
- UI and more interactive user experience (drag and drop) will not be implemented in version one.
- Sweep over a range of values. This will allow users to provide a range of values and an increment to sweep on, and will be nice to have in the future since AML also supports a similar feature. The tool will require users to list each sweeping options for now for simplicity.

## Solution

A sweeping script will be implemented to parse the user provided solution config templates and to generate fully defined solution configs.

Input:

- `solution_config_template`: the path to a solution config template yaml file
- (optional) `output path`: the path to which the generated solution configs where be stored in. Default to a folder named with the solution config template file and the current timestamp

Output:

- a collection of fully defined solution configs stored in a folder

The generated solution configs will

- be named with a concatenation of component names in the short form (e.g., `components.pre_processors.few_shot_embedding` becomes `fewShotEmbedding`), argument name and value, using underscores (`_`) to separate the components, and hyphens (`-`) to separate the args within a component. Given that Windows and Mac have a file max path limit of ~256 characters, this naming strategy should be revisited if we see a usage pattern of sweeping over a larger number of hyperparameters.
- have a brief summary at the beginning which references the solution config template used to generate this file, and a list of component-level and argument-level sweeping performed, to help users quickly identity what to look for in this file.

Future considerations:

- There's the possibility for conflict in the component names in the short form. An hypothetical example is `components.pre_processor.nl2python` and `components.pre_processor.nl2python`. If these components are all swept on, their names will all appear in the generated solution config file names, causing confusion in differentiating them, especially if they happen to have arguments with the same name to sweep on. We don't currently any built-in components that cause the concern, but it's worth revisiting the file naming in the future when the confusion arises. One possible solution is to include the component type in the file names, and it comes with the tradeoff of the name length.

## Solution Config Template Syntax

See [solution_config_template.md](../guides/solution_config_template.md) for details.

## Code snippet support

The solution config syntax proposed above provides an easy way to start using the functionality by keeping track of all the sweeping options in a single file, which comes with the limitations of reusability and readability.

If hyperparameter sweeping is considered as a collaborative or iterative effort, the tool can additionally support defining the component configurations in their own files and referencing them in the solution config to reuse the files, while the inline definition of the sweeping options is still available for as a quick start.

A snippet can include one or more component configurations, which are either their arguments values populated or have sweeping options.

For example, a snippet that has argument-level sweeping looks like:

```yaml
- name: "components.pre_processors.session_selector" 
  args:
    count:
      sweep:
        - 5
        - 10
        - 15
```

Another example of a snippet that has a list of component configurations to be reused in multiple experiment is a list of evaluators in a sequence:

```yaml
- name: "components.evaluators.python_syntax"
  args: {}

- name: "components.evaluators.fuzzy"
  args: {}

- name: "components.evaluators.rouge"
  args: {}

- name: "components.evaluators.exact_match"
  args: {}

- name: "components.evaluators.few_shot_evaluation"
  args: {}
```

### Syntax

The snippets can exist anywhere in user's directory. They are referenced in the solution config template with the `snippet` keyword and the path (relative to the location of the templates) to the file. The content of the referenced file will be used to fill in the template.

```yaml
components:
  - snippet: "docstring/no_docstring.yaml"
  - sweep:
      - snippet: "history/history-h10.yaml"
      - snippet: "history/history-h15.yaml"
  - snippet: "few_shots/sentiment_few_shot_template.yaml"
```

### Pros and cons

- Pros
  - reusability
    - any component configurations that are identified as useful can be shared and referenced in a future sweeping effort
    - any good combinations or ordering of component configurations can be saved and referenced
  - readability
    - fully and explicitly defined component configuration won't require user to mentally map the permutations
    - more concise solution config that focuses on the overall experiment flow and the order of the components, v.s. individual component argument values
- Cons
  - Overhead of creating new files
  - Requires thoughtful naming and grouping of the files to easily keep track of them
