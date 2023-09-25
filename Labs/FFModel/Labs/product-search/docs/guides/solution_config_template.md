# Solution Config Template

A solution config template is used as input to the hyperparameter sweeping capability (see sweeper.py script) to perform sweeping at 3 levels and any combinations of them:

- component
- argument (`args` field)
- supporting data (`supporting_data` field)

## Syntax

Add the `sweep` keyword under the level to sweep at, and list the sweeping options under it. The following sections include the syntax and examples for sweeping at the various levels.

### Sweep at the argument level

#### Syntax

```yaml
- name: "<component_name>" 
  args:
    <argument_name>:
      sweep:
        - <value_option_1>
        - <value_option_2>
        - ...
```

#### Example

Session selector is a pre-processor that selects certain number of sequences from a session. A fully populated component configuration (as part of a solution config) specifies the name of the component and a value for its argument `count`:

```yaml
- name: "components.pre_processors.session_selector" 
  args:
    count: 5
```

The argument `count` is often tweaked to select different ranges of sequences in a session. To sweep on different counts, add a `sweep` keyword under the argument, and list the values under it.

```yaml
- name: "components.pre_processors.session_selector" 
  args:
    count:
      sweep:
        - 5
        - 10
        - 15
```

Given the 3 options for the argument `count` to sweep on, this will result in 3 different solution configs.

To sweep at multiple arguments and the combinations of them, add the `sweep` keyword under each arguments. For example,

```yaml
- name: "components.pre_processors.few_shot_embedding"
  args:
    count: 
      sweep:
        - 5
        - 10
        - 15
    reverse:
      sweep:
        - True
        - False
  supporting_data:
    few_shot_file:
      file_path: "../../data/few_shots/test_02172023_44cm_filled_preprocessed_generated_data_text-similarity-ada-001.pkl"
```

Given the 2 arguments (`count` and `reverse`) to sweep at and 3 and 2 options, respectively, this will result in 3 x 2 = 6 different solution configs.

### Sweep at the supporting data level

#### Syntax

To sweep at the supporting data level, add the keyword `sweep` under the `supporting_data` field, and a list of `Dict[str, DataConfig]`, each of which represents a sweeping option.

Note that an additional `label` field is required under `DataConfig` for each file in each sweeping option in order to uniquely name the generated solution configs. Since the supporting data options might have the same file names but different file paths, the file names won't necessarily unique identify a generated solution config. And the file paths tend to be long strings that include slashes, underscores and other characters, they are not the most readable pieces to include in the generated solution config file names either.

```yaml
- name: "<component_name>" 
  args:
    ...
  supporting_data:
    sweep:
      - file_1:
          file_path: "<path_1>"
          # label is required
          label: "fs1"
        file2:
          file_path: "<path_2>"
          label: "model1"
      - file_3:
          file_path: "<path_3>"
          label: "fs2"
        file_4:
          file_path: "<path_4>"
          label: "model2"
      - ...
```

#### Example

A fully defined sentiment_few_shot_embedding component configuration looks like:

```yaml
- name: "components.pre_processors.sentiment_few_shot_embedding"
  args:
    count: 10
    reverse: true
    top_n_predictions: 3
  supporting_data:
    few_shot_file:
      file_path: "../../data/few_shots/test_02172023_44cm_filled_preprocessed_generated_data_text-similarity-ada-001.pkl"
    model_file:
      file_path: "../../models/sentiment_classifiers/sentiment_rbf_svm_model_sub_cat_info.pkl"
```

The following example sweeps its `supporting_data` by listing 2 options.

```yaml
- name: "components.pre_processors.sentiment_few_shot_embedding"
  args:
    count: 10
    reverse: true
    top_n_predictions: 3
  supporting_data:
    sweep:
      - few_shot_file:
          file_path: "../../data/few_shots/test_02172023_44cm_filled_preprocessed_generated_data_text-similarity-ada-001.pkl"
          # label is required
          label: "fs1"
        model_file:
          file_path: "../../models/sentiment_classifiers/sentiment_rbf_svm_model_sub_cat_info.pkl"
          label: "model1"
      - few_shot_file:
          file_path: "few_shot_bank.pkl"
          label: "fs2"
        model_file:
          file_path: "new_model.pkl"
          label: "model2"
```

Given the 2 options for `supporting_data` to sweep at, this will result in 2 different solution configs.

### Sweep at the component level

The script also supports sweeping at the component-level, in addition to sweeping at the components' argument and supporting data, in a nested way.

#### Syntax

Add the keyword `sweep` and a list of options as an item under the `components` list.

```yaml
components:
  - sweep:
      - name: component_x
        args:
          # can include sweeping options here too
          ...
        supporting_data:
          # can include sweeping options here too
          ...
      - name: component_y
        ...
      - ...
```

#### Example

To compare the performance of sentiment_few_shot_embedding and few_shot_embedding components, at the `sweep` keyword at the component level.

```yaml
components:
  - sweep:
    - name: "components.pre_processors.sentiment_few_shot_embedding"
      args:
        count: 10
        reverse: true
        top_n_predictions: 3
      supporting_data:
        few_shot_file:
          file_path: "../../data/few_shots/test_02172023_44cm_filled_preprocessed_generated_data_text-similarity-ada-001.pkl"
        model_file:
          file_path: "../../models/sentiment_classifiers/sentiment_rbf_svm_model_sub_cat_info.pkl"
    - name: "components.pre_processors.few_shot_embedding"
      args:
        count: 10
        reverse: True
      supporting_data:
        few_shot_file:
          file_path: "../../data/few_shots/test_02172023_44cm_filled_preprocessed_generated_data_text-similarity-ada-001.pkl"
```

Given 2 component options, this will result in 2 different solution configs.

The `sweep` keyword can also be added to the `args` and `supporting_data` fields under the components to provide nested sweeping.
