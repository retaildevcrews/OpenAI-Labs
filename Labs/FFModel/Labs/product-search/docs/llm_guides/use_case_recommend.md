# Use Case Recommendations

Large language models, such as GPT-3, are powerful tools that can generate natural language across a variety of domains and tasks. However, they are not perfect and have limitations and risks that need to be considered before deciding to use them for real-world use cases. Below, we provide some recommendations for the use cases of large language models.

## These models can be best used for generative applications

Large language models are trained on massive amounts of text, where the objective is to learn the statistical patterns of language and predict the most likely word given the previous words. Therefore, they are most suited for scenarios that require generating coherent and fluent text, such as writing stories, essays, captions, headlines, generating natural language from structured data, writing code from natural language specifications, summarizing long documents, etc. However, they may not perform well on tasks that require more logical reasoning, factual knowledge, or domain-specific expertise. For the latter, sufficient relevant information needs to be augmented to the prompt to ground the model.

## Bad answers, factual errors, and other problematic output will happen

Large language models are not infallible, and they may produce output that is incorrect, misleading, biased, offensive, or harmful. This can happen for various reasons, such as data quality issues, model limitations, adversarial inputs, or unintended consequences. Therefore, the use case should be designed in a way that minimizes the impact and frequency of such failures, and provides mechanisms for detecting, correcting, and reporting them. For example, the use case could include quality checks, feedback loops, human oversight, or ethical guidelines.

## A purpose-built NLP model may outperform GPT-3 for a narrow, non-generation task

Large language models are general-purpose models that can handle a wide range of tasks, but they may not be optimal for specific tasks that require more specialized knowledge or skills. For example, a task that involves classifying text into predefined categories, such as sentiment analysis, spam detection, or topic modeling, may benefit from a model that is trained and fine-tuned on a relevant dataset and objective, rather than a generic model that tries to fit all possible scenarios. A purpose-built NLP model may also be more efficient, interpretable, and explainable than a large language model.

## LLMs output needs to be reviewed before being consumed by end users

Large language models can generate plausible and convincing text, but they cannot guarantee its accuracy, reliability, or suitability for a given purpose. Therefore, we do not recommend use cases where the model outputs are directly presented to an end user who may not have the ability or the incentive to verify their validity, such as providing medical advice, legal guidance, financial information, or educational content. In such cases, a human expert should be involved in the process, either to review, edit, or approve the model outputs, or to provide additional context, clarification, or disclaimer.

In conclusion, large language models are powerful and versatile tools that can enable many novel and useful applications, but they also have limitations and risks that need to be carefully considered and addressed. We hope that these recommendations can help developers and users of large language models to make informed and responsible decisions about their use cases.
