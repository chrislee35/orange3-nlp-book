# Chapter 16: Capstone Project Guidelines

## Learning Objectives

By the end of this chapter, you will be able to:

- Select and prepare a real-world dataset for a Natural Language Processing (NLP) task.
- Formulate a problem statement and choose appropriate methods for analysis.
- Apply both classical NLP techniques and modern RAG/LLM approaches to process and analyze messy textual data.
- Evaluate the effectiveness of different methods and compare results.

---

## 16.1 Capstone Project Overview

The capstone project will involve working with a real-world, messy textual dataset to solve a meaningful NLP problem. You'll be required to apply both **classical methods** (e.g., text cleaning, feature extraction, and model training) and **modern techniques** like **Reference Augmented Generation (RAG)** and **Large Language Models (LLMs)**.

### Key Components:
- **Dataset Selection**
- **Problem Formulation**
- **Methodology**
- **Evaluation Criteria**

Your goal is to clean, process, and analyze the data using a combination of classical and modern methods. You will be expected to compare the effectiveness of these methods and demonstrate how the RAG and LLM approaches improve your results.

---

## 16.2 Dataset Selection

Choose a dataset that provides messy textual data. Ideally, the data should be sufficiently large to allow for meaningful analysis, but not so large that it becomes unwieldy. The dataset can be sourced from:

- **Public Data Repositories**: Kaggle, UCI Machine Learning Repository, or other public datasets.
- **Web Scraping**: Use Python libraries (e.g., `BeautifulSoup` or `Scrapy`) to scrape articles, reviews, or social media content.
- **Custom Data**: If you have a specific domain (e.g., scientific research, news articles, customer feedback), you may curate a dataset.
  
Examples of datasets include:
- **Text Classification**: Categorizing news articles by topics (e.g., politics, sports, technology).
- **Sentiment Analysis**: Analyzing customer reviews from a company or product page.
- **Topic Modeling**: Exploring trends in a collection of research papers, blogs, or news archives.

**Considerations**:
- The data should contain at least a few thousand entries for meaningful analysis.
- It should require some degree of **cleaning** (e.g., removing noise, fixing inconsistencies, normalizing formats).

---

## 16.3 Problem Formulation

Based on your dataset, decide on a clear **problem statement**. Here are a few examples of potential problems:

- **Text Classification**: Predict the category of a text (e.g., sentiment, topic, or genre).
- **Text Summarization**: Automatically generate a summary for a long article or report.
- **Question Answering (QA)**: Build a system that answers questions from a specific document or collection.
- **Named Entity Recognition (NER)**: Identify and classify proper nouns (e.g., names, locations, dates) in unstructured text.
- **Text Generation**: Generate creative text based on a prompt (e.g., poetry, article continuation).

### Guidelines for Problem Formulation:
1. **Be Specific**: Narrow your focus to one clear NLP task.
2. **Define Success**: Specify what success looks like (e.g., accuracy, F1 score, BLEU score, or qualitative results like coherence or relevance).

---

## 16.4 Methodology

You will apply **two approaches** to solving your problem:

### 1. **Classical NLP Techniques**
   - **Text Preprocessing**: Clean and transform the raw data (removing stop words, punctuation, stemming, lemmatization).
   - **Feature Engineering**: Create features like word embeddings, TF-IDF, bag-of-words, etc.
   - **Traditional Models**: Apply classical models like Naive Bayes, Logistic Regression, or SVMs for classification or clustering tasks.

### 2. **Modern Approaches (RAG and LLMs)**
   - **Reference Augmented Generation (RAG)**: Build a reference database using `orange3-ollama`, perform queries with relevant context, and generate responses or summaries.
   - **LLM Application**: Use pre-trained models for tasks like sentiment analysis, summarization, and question answering. You can use both RAG and direct LLM methods.

> **Tip**: Compare how classical methods (based on statistical learning) perform against LLMs that work by leveraging massive language knowledge.

---

## 16.5 Evaluation Criteria

Evaluate the performance of your models based on several criteria:

### 1. **Classical Method Evaluation**:
   - **Accuracy**: For classification tasks, how many predictions were correct?
   - **Precision, Recall, F1-Score**: These are particularly important for imbalanced datasets.
   - **Confusion Matrix**: Analyze false positives and false negatives.
   - **Qualitative Analysis**: Look at example outputs for coherence, relevance, and correctness.

### 2. **Modern Approach Evaluation (RAG and LLMs)**:
   - **Relevance of Generated Responses**: Does the answer make sense in the context of the question and the retrieved documents?
   - **Coherence**: For generative tasks, how well does the generated text flow and make sense?
   - **Comparative Analysis**: Compare the RAG-generated outputs and LLM-generated responses to the classical method's results. Did the LLMs improve accuracy or relevance?

### 3. **Model Comparison**:
   - **Time**: How long did it take to process the data and generate results with each approach?
   - **Scalability**: How well does your model scale with more data? (Classical models vs. LLMs)
   - **Explainability**: How easy is it to explain why a model made a certain decision (particularly important for traditional models)?

---

## 16.6 Capstone Project Report

Submit a report that includes the following:

- **Introduction**: Briefly introduce the dataset and problem you're addressing.
- **Data Preprocessing**: Describe the steps you took to clean and prepare the data.
- **Methodology**: Outline both classical and modern NLP methods you applied.
- **Results and Discussion**: Present the results of your experiments and compare the performance of the different approaches.
- **Conclusions**: Summarize what worked well and where you encountered challenges.

> **Optional**: Include a video or presentation summarizing your project and demonstrating the working solution.

---

## 16.7 Capstone Project Rubric

| Criterion                          | Description                                                                 | Points |
|-------------------------------------|-----------------------------------------------------------------------------|--------|
| **Dataset Selection & Cleaning**   | Appropriateness of the dataset and quality of data preprocessing.            | 20     |
| **Problem Formulation**            | Clarity and relevance of the problem being solved.                           | 15     |
| **Classical Method Implementation**| Correct application of classical NLP methods (e.g., TF-IDF, SVM).           | 25     |
| **Modern Method Implementation**   | Application of RAG/LLM methods and their evaluation.                         | 25     |
| **Evaluation & Analysis**          | Thoroughness of evaluation and comparison of results.                        | 10     |
| **Final Report**                   | Clear, well-organized, and professional report.                             | 5      |

---

## Notes

- Your project should focus on **real-world applicability**. Choose a dataset that could be valuable for a practical application.
- Aim to be creative, but make sure to stick to the scope of the problem.
- You can use the `orange3-ollama` module to incorporate LLMs and RAG into your solution.

Good luck, and have fun with your project!

---

