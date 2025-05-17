# Chapter 2: Getting Started with Orange

## Learning Objectives

By the end of this chapter, you will be able to:

- Install and launch Orange with the necessary NLP add-ons.
- Understand the Orange interface and core widget types.
- Load text datasets into Orange.
- Build a basic workflow for text exploration.

---

## 2.1 Installing Orange and Required Add-ons

### Step 1: Installing Orange

Visit [https://orange.biolab.si](https://orange.biolab.si) and download the latest version of Orange for your platform (Windows, macOS, or Linux). Follow the installation instructions provided on the website.

> 💡 For advanced users: Orange can also be installed via pip using `pip install orange3`.

### Step 2: Installing Add-ons

To work with text data, install the **Text** add-on:

1. Launch Orange.
2. Go to *Options* → *Add-ons*.
3. Select and install **Text**.
4. Restart Orange if prompted.

---

## 2.2 Exploring the Orange Interface

Orange is a visual programming environment organized around **workflows**. A workflow is a collection of connected **widgets** that process and visualize data.

### Key Interface Elements

- **Canvas** – where you build workflows by placing and connecting widgets.
- **Widget Toolbox** – categories like *Data*, *Visualize*, *Model*, *Evaluate*.
- **Right Panel** – settings and options for the currently selected widget.
- **Top Bar** – save/load workflow, run/pause execution.

![Figure 2. Orange Canvas Interface with labels for the different sections of the user interface.](2%20Orange%20Interface.png)

---

## 2.3 Understanding Widgets

Widgets are the building blocks of an Orange workflow. Each widget performs a specific function, such as:

- Loading data (*File*)
- Visualizing data (*Word Cloud*, *Distributions*)
- Transforming data (*Preprocess*, *Select Columns*)
- Training models (*Naive Bayes*, *Logistic Regression*)
- Evaluating performance (*Test & Score*)

### Text-Specific Widgets

Once the Text add-on is installed, you will see additional widgets under the **Text Mining** category, such as:

- *Corpus*
- *Preprocess Text*
- *Word Cloud*
- *Sentiment Analysis*

---

## 2.4 Loading Your First Dataset

Let’s load a sample text dataset and build your first workflow.

### Sample Dataset: `book-excerpts.tab`

This dataset contains short excerpts from books along with genre labels (e.g., Sci-Fi, Romance, Fantasy).

### Basic Workflow Steps:

1. From the Text Mining toolbox section, drag the *Corpus* widget onto the canvas.
2. Select `book-excerpts.tab` from the sample datasets.
3. Add a *Word Cloud* widget and connect it to *Corpus*.

> 📝 **Reflection:** Look at the most frequent words. Do they help with understanding the topic of a story?

> ⚠️ If you receive an error about WebviewWidget, install the `pyqtwebengine` Python package.

![Figure 3. Orange canvas using the Corpus and Word Cloud widgets](4%20First%20Dataset.png)

Running this workflow, [2-4 First Dataset](4%20First%20Dataset.ows), will output a Word Cloud akin to the follow figure.

![Figure 4. Wordcloud display of some sample text](4b%20Wordcloud.png)

---

## Lab Exercise 2: Building a Text Exploration Workflow

**Goal**: Build a workflow that loads and visualizes book excerpts.

**Steps**:

1. Set up the following widgets:
   - *Corpus*
   - *Preprocess Text*
   - *Word Cloud*
2. Explore the differences when you apply different preprocessing options.
3. Add a *Data Table* widget to view the tokenized text.

**Questions to Consider**:
- How does removing stopwords affect the Word Cloud?
- What genres appear to have the most unique vocabulary?

> 📝 **Reflection:** Which preprocessing steps had the largest impact on your results? Why?

---

## Comprehension Questions

1. What is the purpose of the *Corpus* widget in Orange?
2. How do you install an add-on in Orange?
3. What effect does tokenization have on raw text?
4. Why might lowercase conversion be helpful in NLP?

---

## Key Terms

- Widget
- Workflow
- Preprocessing
- Corpus
- Tokenization
- Stopwords

---

## Notes

- In later chapters, we’ll add modeling and evaluation steps to this workflow.
- You can save your workflow using *File → Save As* and reopen it later to continue.

---

