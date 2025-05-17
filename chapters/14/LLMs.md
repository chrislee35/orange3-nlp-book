# Chapter 14: Using a Large Language Model

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand what large language models (LLMs) are and how they can be applied to many NLP tasks.
- Use the `orange3-ollama` module to interact with local LLMs for multiple purposes.
- Run summarization, sentiment analysis, classification, generation, and question answering using a single LLM interface.
- Compare the versatility of LLMs with task-specific traditional NLP models.

---

## 14.1 What is a Large Language Model?

**Large Language Models (LLMs)** are trained on massive text corpora and can perform a wide range of NLP tasks with little to no fine-tuning.

Examples:
- GPT-3 / GPT-4
- LLaMA
- Mistral
- Gemma
- Mixtral
- Open-source models accessed through **Ollama**

> LLMs are generalists: instead of training a new model for each task, you prompt them with the right instruction.

---

## 14.2 The `orange3-ollama` Module

This module lets you connect Orange workflows to **local language models** served by [Ollama](https://ollama.com/), allowing interactive, private, and efficient model usage.

Supported LLM tasks:
- Text summarization
- Sentiment analysis
- Text classification
- Prompt-based generation
- Question answering

> Note: LLM behavior is determined by the prompt. Widgets in this module handle prompt formatting for you.

---

## 14.3 Widgets for LLM-Powered Workflows

### Available Widgets

- **Ollama Summarizer**
- **Ollama Sentiment**
- **Ollama Classifier**
- **Ollama Generator**
- **Ollama QA**
- **Model Selector / System Prompt Configurator** *(optional)*

Each widget accepts a text field (from Corpus or File) and returns model-generated output using a prompt template.

---

## 14.4 Example Workflows

### Summarization

File → Ollama Summarizer → Data Table


### Sentiment Analysis

Corpus → Ollama Sentiment → Corpus Viewer

### Classification

File → Ollama Classifier (with labels: e.g. Spam/Not Spam) → Data Table

### Generation

Text Input (custom prompts) → Ollama Generator → Text Display

### Question Answering

File (Context) + User Question → Ollama QA → Answer Viewer


---

## Lab Exercise 14A: Multi-Task LLM Explorer

**Goal**: Use one document and apply all five LLM tasks.

**Steps**:

1. Load a file with several reviews or articles.
2. Connect to all of the following widgets in parallel:
    - Ollama Summarizer
    - Ollama Sentiment
    - Ollama Classifier
    - Ollama Generator
    - Ollama QA
3. Use a Data Table to compare the output for each row/document.

**Discussion**:
- How does the same document yield different kinds of outputs?
- Were the summaries accurate? Were the sentiments reasonable?

---

## Comprehension Questions

1. What advantages do LLMs offer over task-specific models?
2. How does prompting change the output of an LLM?
3. What privacy or performance considerations are addressed by using Ollama locally?
4. When might you still prefer traditional NLP pipelines over LLMs?

---

## Key Terms

- Large Language Model (LLM)
- Prompt Engineering
- Ollama
- Summarization
- Sentiment Analysis
- Classification
- Generation
- Question Answering

---

## Notes

- Ensure your Ollama server is running locally before using the widgets.
- Save your workflow as `llm-multitask.ows`.
- Next, we’ll improve on LLMs using **Reference Augmented Generation**.

---

