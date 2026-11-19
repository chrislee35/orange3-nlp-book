# Chapter 16: Capstone Project

## Learning Objectives

By the end of this chapter, you will be able to:

- Choose a real text dataset and a narrow, answerable question about it.
- Define what "success" means before you run any method.
- Build a simple classical baseline and a modern (embedding, LLM, or RAG) solution, and compare them fairly on the same test examples.
- Report cost (time, hardware, effort) alongside accuracy, and say which method you would deploy and why.
- Write up results honestly, including failures.

---

## 16.1 What the Capstone Is

The capstone is one small research project. You pick a messy, real collection of text, ask one question of it, and answer that question twice: once with a **classical** method (Chapters 3 to 10) and once with a **modern** method (Chapters 11 to 15). Then you compare the two.

The comparison is the point. A project that shows the LLM scoring 90% is not finished until it also shows what a plain TF-IDF model scores on the same examples, and what each one cost.

---

## 16.2 Choose a Problem You Can Finish

Start from the question, not the tool. Good capstone questions are narrow and can be checked:

| Strong scope | Weak scope |
|--------------|------------|
| Sort 1,500 support emails into 4 topics, and compare TF-IDF + Logistic Regression with an LLM zero-shot classifier. | "Analyze customer feedback." |
| Answer questions about one organization's policy documents with RAG, and check each answer against the source. | "Build a chatbot." |
| Find which of 3 summaries (extractive, abstractive, LLM) of 20 news articles readers prefer. | "Make summaries better." |
| Find out whether sentiment scores track star ratings in 2,000 reviews. | "Understand sentiment." |

A project is the right size when:

1. **One task.** Classification, clustering or topic modeling, sentiment, summarization, question answering (with or without RAG), or entity extraction.
2. **A way to check answers.** Either the data already has the right labels (topic, rating, category), or you can write them by hand for a small test set. If you cannot say what a correct answer is, you cannot compare methods.
3. **A size that fits your computer.** See section 16.5.

---

## 16.3 Choose the Data

**Where to look**

- **Shipped with the book or Orange:** `movie-reviews.tab` (2,000 labeled reviews), the `BBC3` corpus from the *Datasets* widget (1,407 labeled news articles; it is for non-commercial and research use), and the other corpora that come with Orange3-Text.
- **Public repositories** such as Kaggle or the UCI Machine Learning Repository. Check the licence and any rule on sharing before you use a dataset.
- **Your own material:** a club's documents, course notes, a set of reviews you collected by hand. Make sure you are allowed to use it, and remove personal information.

**What to look for**

- **Labels, or a plan to make them.** A few hundred labeled rows is enough to test with, and labeling 100 by hand is a reasonable amount of work.
- **Some mess.** Real data has duplicates, empty rows, odd characters, and several languages. Say what you found and what you did about it.
- **Enough rows for a fair test.** A few thousand rows for a classical model is comfortable. An LLM does not need that many, because you will probably run it only on the test sample (section 16.5).
- **Language.** The book's models are English. Another language is possible, but check that your embedding and LLM models support it.

Write down where the data came from, its licence, how many rows it has, and what a row looks like. You need these for the report.

---

## 16.4 Plan the Comparison Before You Run It

Decide these five things first and write them down:

1. **The question.** One sentence.
2. **The metric.** For classification: accuracy, plus precision, recall, and F1 per class if the classes are unbalanced (Chapter 6). For question answering, summarization, or generation: a short rubric you apply by hand, such as "correct", "partly correct", "wrong", and "not in the documents", with a count of each.
3. **The test set.** A set of examples that no method sees while you are building or tuning it. **Both methods must be scored on exactly the same examples.** If the classical model is tested on 500 rows and the LLM on 50, you are comparing luck.
4. **The baseline.** The simplest reasonable method. For classification that is always predicting the most common class, plus a Bag of Words model with Logistic Regression. If your fancy method cannot beat this, say so.
5. **What would change your mind.** For example: "If the LLM is no more than 3 points more accurate but 100 times slower, I would still use the classical model."

### Classical and modern methods

| Task | Classical | Modern |
|------|-----------|--------|
| Classification | Preprocess, Bag of Words or TF-IDF, Logistic Regression or Naive Bayes, scored with *Test & Score* | Embed documents (*Document Embedding*) and train a simple model on the vectors; or ask an LLM (*Ollama Text Classification*, or *Text Generator* with your own prompt) |
| Clustering and topics | TF-IDF, distances, *Hierarchical Clustering* or *Topic Modelling* (LDA) | Embeddings with *t-SNE* or clustering on the vectors |
| Sentiment | VADER (*Sentiment Analysis*) | *Ollama Sentiment Analyzer* |
| Summarization | Extractive (*Summarization*) | *Abstractive Summary* or *Ollama Summarizer* |
| Question answering | Keyword search | *Question Answering* (extractive), or RAG: *Text Chunker*, *Text Embedder*, *Reference Library*, *Ollama RAG* |
| Entity extraction | *Named Entity Recognition* | A prompt that asks the LLM for entities |

Each of these has an exercise in an earlier chapter. Look back at it for the workflow.

---

## 16.5 Time, Hardware, and Scale

The two kinds of method differ greatly in cost, so measure it.

- **Time a small run first.** Run the LLM on 20 rows, note how long it took, and multiply to estimate the full run. Do this before you start the full run, not after.
- **LLMs run when you press the button.** The Ollama widgets send one request per row and are not repeatable unless you control temperature and seed (the *Text Generator* does; the Ollama task widgets do not). Run the LLM on the test sample only, and say so.
- **Keep a log.** Note the model name, the widget settings, the prompt, and the date. The same prompt on a different model, or on the same model on another day, can give different results.
- **Memory.** `phi4-mini` needs about 2.5 GB. If your computer struggles, use a smaller test sample rather than a smaller model, unless you are comparing models.

---

## 16.6 Evaluate Beyond the Number

A single accuracy figure hides most of what you need to know. Add:

- **A confusion matrix** (Chapter 6) for classification. Which classes does each method mix up? Do they make the *same* mistakes?
- **A look at the errors.** Read at least 20 wrong answers from each method. Group them: label noise (the "truth" is arguable), ambiguous text, a missing instruction, or a real model failure.
- **For RAG:** record for every question whether the right passage was retrieved and whether the answer was correct (Chapter 15). A wrong answer with the right passage is a different problem from a wrong answer with the wrong passage.
- **Cost:** time to run, memory needed, effort to set up, and whether the result is the same on a second run.
- **Explainability:** a classical model can show which words pushed a document to a class. An LLM gives an answer and possibly an explanation that sounds right but may not describe how it decided. How would you check?

If a result looks too good, look for leaks: duplicate rows in both the training and test sets, labels hidden in the text, or an LLM that has seen a famous dataset in training.

---

## 16.7 The Report

Write for a reader who has not seen your workflow. Aim for 4 to 8 pages, or a short slide deck with notes.

1. **Question and data.** The question, where the data came from, its licence, size, and one or two example rows.
2. **Cleaning.** What was wrong with the data, and what you did. Include the counts removed or changed.
3. **Methods.** The classical method and the modern method, with the workflow screenshot and the settings. Include the model names and the exact prompt.
4. **Results.** A table of the metric on the shared test set for the baseline, the classical method, and the modern method, plus the time each took.
5. **Error analysis.** Examples of failures, grouped as in 16.6.
6. **Recommendation.** Which method you would use for real, why, and what you would check before deploying.
7. **Limits.** What you did not test and what could make your conclusion wrong.

Attach your saved `.ows` workflow files and the list of test examples so someone else can repeat your work.

> **A note on using AI tools while you write.** Follow your course's rules. Whatever the rules, a model's output is a claim to check and not a source, and the numbers in your results must come from your own runs.

---

## 16.8 Capstone Rubric

| Criterion | What earns the points | Points |
|-----------|-----------------------|--------|
| **Data and cleaning** | Suitable dataset with a source and licence; cleaning described with counts | 15 |
| **Problem and plan** | A narrow question; metric, test set, and baseline chosen before running | 15 |
| **Classical method** | Correct workflow with a baseline, evaluated on the test set | 20 |
| **Modern method** | Correct workflow, with prompt and settings recorded, evaluated on the same test set | 20 |
| **Evaluation and analysis** | Fair comparison, error analysis, and cost (time and resources) | 20 |
| **Report** | Clear, honest, organized, and repeatable | 10 |

Total: 100.

---

## Comprehension Questions

1. Why must both methods be scored on exactly the same test examples?
2. What is a baseline, and why does a result mean little without one?
3. What makes a capstone question "narrow"? Rewrite "analyze customer reviews" into a question you could finish.
4. You have 50,000 reviews and an LLM that takes 3 seconds per row. How long would a full run take, and what would you do instead?
5. Your LLM gets 91% and your TF-IDF model gets 89%. What else would you look at before saying the LLM is better?
6. In a RAG project, why record both whether the right passage was retrieved and whether the answer was correct?

---

## Key Terms

- Baseline
- Test set / held-out data
- Metric
- Data leakage
- Error analysis
- Reproducibility
- Classical vs. modern pipeline

---

## Notes

- Save your workflows and the report together.
- This is the last chapter. If you build something you like, the next step is to put your own documents through the RAG workflow from Chapter 15.
