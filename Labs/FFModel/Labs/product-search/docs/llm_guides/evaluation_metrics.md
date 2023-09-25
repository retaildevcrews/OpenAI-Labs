# Evaluation Metrics

Evaluating the performance of machine learning models is crucial for determining their effectiveness and reliability. To do that, quantitative measurement with reference to ground truth output (a.k.a. evaluation metrics) are needed. While several metrics have been proposed in the literature for evaluating the performance of LLM-based solutions, it is essential to use the right metrics that are suitable for the problem we are attempting to solve.

This document aims to cover several widely used evaluation metrics and methods that could be useful for evaluating these large models over a variety of Natural Language Processing related tasks.

## Text Similarity Metrics

Text similarity metrics are evaluators that focus primarily on computing similarity by comparing the overlap of words or word sequences between text elements. They’re very useful for producing a similarity score for predicted output from an LLM and reference ground truth text and they give an indication as to how well the model is performing for each respective task.

### Levenshtein Similarity Ratio

The Levenshtein Similarity Ratio is a string metric for measuring the similarity between two sequences based on Levenshtein Distance. Informally, the Levenshtein Distance between two strings is the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one string into the other. The Levenshtein Similarity Ratio can be calculated using Levenshtein Distance value and the total length of both sequences in the following definitions:

***Levenshtein Similarity Ratio (Simple Ratio):***
$$Lev.ratio(a, b) = {(|a|+|b|)-Lev.dist(a,b) \over |a|+|b|}$$
where `|a|` and `|b|` are the lengths of strings `a` and `b`.

Note: **exact match** of two sequences is the special case when Simple Ratio equals 1.

A few different methods are derived from **Simple Levenshtein Similarity Ratio**. They are alternative metrics that might be useful depending on specific text evaluation tasks.

- **Partial Ratio:**: Calculates the similarity by taking the shortest string, and compares it against the sub-strings of the same length in the longer string,
- **Token-sort Ratio:** Calculates the similarity by first splitting the strings into individual words or tokens, sorts the tokens alphabetically, and then recombines them into a new string. This new string is then compared using the simple ratio method.
- **Token-set Ratio:** Calculates the similarity by first splitting the strings into individual words or tokens, and then matches the intersection and union of the token sets between the two strings.

[ffmodel Fuzzy Distance Evaluator](../../components/evaluators/fuzzy.py) implements this evaluator.

### BLEU Score

The BLEU (bilingual evaluation understudy) score evaluates the quality of text that has been translated by a machine from one natural language to another. Therefore, it’s typically used for Machine-translation tasks, however, it’s also being used in other tasks such as text generation, paraphrase generation, and text summarization. The basic idea involves computing the precision – which is the fraction of candidate words in the reference translation. Scores are calculated for individual translated segments—generally sentences—by comparing them with a set of good quality reference translations. Those scores are then averaged over the whole corpus to reach an estimate of the translation's overall quality. Punctuation or grammatical correctness are not taken into account when scoring.

With this measure, few human translations will attain a perfect score, since this would indicate that the candidate is identical to one of the reference translations. For this reason, it is not necessary to attain a perfect score. Given that there are more opportunities to match with the addition of multiple reference translations, it is often encouraged to have one or more reference translations that will be useful for maximizing the BLEU score.

$$P = {m \over w_t}$$
$m: \text{Number of candidate words in reference.}$
$w_t : \text{Total number of words in candidate.}$

Typically, the above computation considers individual words or unigrams of candidate that occur in target. However, for more accurate evaluations of a match, one could compute bi-grams or even trigrams and average the score obtained from various n-grams to compute the overall BLEU score.

### ROUGE

As opposed to the BLEU score, the Recall-Oriented Understudy for Gisting Evaluation (ROUGE) evaluation metric measures the recall. It’s typically used for evaluating the quality of generated text and in machine translation tasks — However, since it measures recall, it's mainly used in summarization tasks since it’s more important to evaluate the number of words the model can recall in these types of tasks.
The most popular evaluation metrics from the ROUGE class are ROUGE-N  and ROUGE-L:

***Rouge-N:*** measures the number of matching 'n-grams' between a reference (a) and test (b) strings.

$$Precision= {\text{number of n-grams found in both a and b} \over \text{number of n-grams in b}}$$
$$Recall= {\text{number of n-grams found in both a and b} \over \text{number of n-grams in a}}$$
***Rouge-L:*** measures the longest common subsequence (LCS) between a reference (a) and test (b) strings.
$$Precision= {LCS(a,b) \over \text{number of uni-grams in b}}$$
$$Recall= {LCS(a,b) \over \text{number of uni-grams in a}}$$
***For both Rouge-N and Rouge-L:***
$$F1={2 \times\text{precision} \over recall}$$

[ffmodel Rouge Score Evaluator](../../components/evaluators/rouge.py) implements this evaluator.

### Semantic Similarity

The semantic similarity between two sentences refers to how closely related their meanings are. To do that, each string is first represented as a feature vector that captures its semantics/meanings. One commonly used approach is generating embeddings of the strings (e.g., using a LLM) and then using cosine similarity to measure the similarity between the two embedding vectors. More specifically, given an embedding vector (A) representing a target string, and an embedding vector (B) representing a reference one, the cosine similarity is computed as follows:

$$ \text{cosine similarity} = {A \cdot B \over ||A|| ||B||}$$

As shown above, this metric measures the cosine of the angle between two non-zero vectors and ranges from -1 to 1, where 1 means the two vectors are identical and -1 means they are completely dissimilar.

## Functional Correctness

Functional correctness can be used to evaluate the accuracy of NL-to-code generation tasks, where the LLMs are tasked with generating code for a specific task in natural language. In this context, functional correctness evaluation is used to assess whether the generated code produces the desired output for a given input.

For example, To use functional correctness evaluation, we can define a set of test cases that cover different inputs and their expected outputs. For instance, we can define the following test cases:

```text
Input: 0
Expected Output: 1
Input: 1
Expected Output: 1
Input: 2
Expected Output: 2
Input: 5
Expected Output: 120
Input: 10
Expected Output: 3628800
```

We can then use the LLM-generated code to calculate the factorial of each input and compare the generated output to the expected output. If the generated output matches the expected output for each input, we consider the test case to have passed and conclude that the LLM-based solution is functionally correct for that task.

The challenge of functional correctness evaluation is that sometimes it is cost prohibitive to set up an execution environment for implementing generated code. Additionally, functional correctness evaluation does not take into account other important factors such as the readability, maintainability, and efficiency of the generated code. Moreover, it is difficult to define a comprehensive set of test cases that cover all possible inputs and edge cases for a given task, which can limit the effectiveness of functional correctness evaluation.

## Rule-based Metrics

For domain specific applications and experiments, it might be useful to implement rule-based metrics. For instance, assuming we ask the model to generate multiple completions for a given task. We might be interested in selecting output that maximizes the probability of certain keywords being present in the prompt. Additionally, there are situations in which the entire prompt might not be useful – only key entities might be of use. Creating a model that performs entity extraction on generated output could be useful for evaluating the quality of the predicted output as well. Given a number of possibilities, it is good practice to think of custom, rule-based metrics that are tailored to domain specific tasks. Here we provide examples of some widely used rule-based evaluation metrics for both NL2Code and NL2NL use cases:

- **Syntax correctness:** This metric measures whether the generated code conforms to the syntax rules of the programming language being used. This can be evaluated using a set of rules that check for common syntax errors, such as missing semicolons, incorrect variable names, or incorrect function calls.
- **Format check:** Another metric that can be used to evaluate NL2Code models is the format of the generated code. These metric measures whether the generated code follows a consistent and readable format. This can be evaluated using a set of rules that check for common formatting issues, such as indentation, line breaks, and whitespace.
- **Language check:** A language check metric can be used to evaluate whether the generated text or code is written in a way that is understandable and consistent with the user's input. This can be evaluated using a set of rules that check for common language issues, such as incorrect word choice or grammar.
- **Keyword presence:** This metric measures whether the generated text includes the keywords or key phrases that were used in the natural language input. This can be evaluated using a set of rules that check for the presence of specific keywords or key phrases that are relevant to the task being performed.

## Human Feedback

Human based feedback is always going to be a good (if not the gold standard) option for evaluating the quality of output generated by an LLM. Depending on the application, reviewers with domain expertise may be required. This process can be as simple as having a human being verify output and assign it a pass/fail mark. However, for a more refined human evaluation process the following steps can be taken:

- Identifying a group of domain experts or people familiar with the problem space
- Generating a shareable asset that can be viewed by multiple reviewers (for example, a shared excel spreadsheet that can be saved and converted to a CSV file for later use in experiments)
- Having each individual review each sample and assign a score for each completion. Alternatively, reviewers could split up work and review different sets of data points to get through the review process much faster.
- Additionally, having notes assigned to each reviewed data point will give an insight as to how each specific reviewer interpreted each completion for each data point. This is very useful as it serves as a reference point for users who may have not reviewed the dataset before but want to understand the thought process involved with each review. Notes could also serve as a convention for standardizing the evaluation process as learnings derived from each reviewed note could potentially be applied to other samples within the dataset.
  
Depending on human resources available, this might be a tedious task. Scenarios that might involve this sort of evaluation need to be carefully assessed.

## LLM-based Evaluation

Another developing method of evaluating the performance of LLMs is asking the model to score itself, or using another LLM to do that.  The idea is that we can take output produced by the model and prompt the model itself (or another advanced model) to determine the quality of the completions generated. This method of evaluation is likely to become more popular with the emergence GPT-4 given the model's ability to accurately score the quality of predicted output. The following steps are typically required to leverage this means of evaluation:

1. Generate output predictions from a given test set.
2. Prompt the model to focus on assessing the quality of output given reference text and sufficient context (e.g., criteria for evaluation).
3. Feed the prompt into the model and analyze results.

 While LLMs such as GPT-4 have yielded fairly good results with this method of evaluation, a human-in-the-loop may still be required to verify the output generated by the model. The model may not perform as well in domain specific tasks or situations that involve leveraging very specific methods to evaluate output, so the behavior of the model should be studied closely depending on the nature of the dataset. Keep in mind that performing LLM-based evaluation requires its own prompt engineering. Below is a sample prompt template used in an NL2Python application.

```text
You are an AI-based evaluator. Given an input (starts with --INPUT) that consists or a user prompt (denoted by STATEMENT)

and the two completions (labelled EXPECTED and GENERATED), please do the following:

1- Parse user prompt (STATEMENT) and EXPECTED output to understand task and expected outcome.

2- Check GENERATED code for syntax errors and key variables/functions.

3- Compare GENERATED code to EXPECTED output for similarities/differences, including the use of appropriate Python functions and syntax.

4- Perform a static analysis of the GENERATED code to check for potential functional issues, such as incorrect data types, uninitialized variables,

   and improper use of functions.

5- Evaluate the GENERATED code based on other criteria such as readability, efficiency, and adherence to best programming practices.

6- Use the results of steps 2-5 to assign a score to the GENERATED code between 1 to 5, with a higher score indicating better quality.

   The score can be based on a weighted combination of the different criteria.

7- Come up with an explanation for the score assigned to the GENERATED code. This should also mention if the code is valid or not

When the above is done, please generate an ANSWER that includes outputs:

--ANSWER

EXPLANATION:

SCORE:

Below are two example:

# Example 1

--INPUT

STATEMENT = create a cube

EXPECTED = makeCube()

GENERATED = makeCube(n='cube1')

--ANSWER

SCORE: 4

EXPLANATION: Both completions are valid for creating a cubes . However, the GENERATED one differs by including the cube name (n=cube1), which is not necessary.

# Example 2

--INPUT

STATEMENT = make cube1 red

EXPECTED = changeColor(color=(1, 0, 0), objects=["cube1"])

GENERATED = makeItRed(n='cube1')

--ANSWER

SCORE: 0

EXPLANATION: There is no function in the API called makeItRed. Therefore, this is a made-up function.


Now please process the example blow

--INPUT

STATEMENT = {prompt}

EXPECTED = {expected_output}

GENERATED = {completion}

--ANSWER
```
