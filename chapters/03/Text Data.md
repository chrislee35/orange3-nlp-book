# Chapter 3: Working with Text Data

## Learning Objectives

By the end of this chapter, you will be able to:

- Load and inspect text data in Orange.
- Apply common preprocessing steps such as tokenization, stopword removal, and lemmatization.
- Understand the role of text normalization in NLP.
- Build a reusable workflow to clean and prepare raw text data.

---

## 3.1 Importing Text Data into Orange

Text data in Orange can be loaded using:

- The *File* widget
- The *CSV File Import* widget
- The *Corpus* widget (specific to Orange Text add-on)

> 📝 **Note:** For text processing, ensure your dataset includes at least one column of free-form text.

### Example Dataset: BBC3 News Classification Dataset

Use Orange's *Dataset* widget and select BBC3. Connect that to *Corpus* and select only the Title field.

Use *Feature Statistics* to understand the distribution of the **category** field.  Use the `color:` selection at the bottom to show a legend of the 3 categories.

### Quick Start

- Use the *Dataset* widget and select BBC3.
- Connect that to *Corpus* and select only the Title field.
  * If you cannot find the *Corpus* widget, install the **Text** add-on.
  * ![Selecting the Title field as the text feature](1-Corpus%20Title.png)
- The *Corpus Viewer* widget


Your current workflow should look something like this:

![Loading workflow for BBC3 News Classification Dataset](1-Import%20Workflow.png)

---

## 3.2 The Text Preprocessing Pipeline

Before analyzing text, it must be cleaned and standardized. This process is called **text preprocessing**.

Common steps include:

| Step             | Description                                               |
|------------------|-----------------------------------------------------------|
| Lowercasing       | Converts all text to lowercase                           |
| Tokenization      | Splits text into words or tokens                         |
| Stopword Removal  | Removes common words (e.g., "the", "and", "is")          |
| Lemmatization     | Reduces words to base form (e.g., "running" → "run")     |
| Punctuation Removal | Deletes symbols and punctuation marks                 |

> 💡 These steps reduce noise and improve the quality of features extracted later.

---

## 3.3 Using the *Preprocess Text* Widget

The *Preprocess Text* widget allows you to apply several preprocessing steps in one place.

### Key Features

- Select columns to preprocess
- Apply transformations such as:
  - Lowercasing
  - Filtering (e.g., by word length or frequency)
  - Lemmatization (using spaCy)
- Add POS filtering (optional)

> 🧠 Try preprocessing the `Title` column using different combinations of these steps and observe the effect on token counts.

---

## 3.4 Visualizing Cleaned Text

After preprocessing, you can visualize the cleaned corpus using:

- *Word Cloud* – Highlights frequent terms
- *Corpus Viewer* – Shows individual processed texts
- *Data Table* – For inspecting the cleaned token list

> 📌 **Tip:** Save your preprocessed corpus with *Save Data* so it can be reused in later experiments.

---

## Lab Exercise 3: Clean and Explore Headlines

**Goal**: Build a workflow to load, clean, and visualize a set of news headlines.

**Widgets Needed**:
- *Dataset*
- *Corpus*
- *Preprocess Text*
- *Word Cloud*
- *Corpus Viewer*
- *Save Data*

**Steps**:

1. Use the *Dataset* widget and select BBC3.
2. Connect that to *Corpus* and select only the Title field.
3. Apply at least 3 preprocessing steps in *Preprocess Text*.
4. Generate a Word Cloud and analyze which terms are most common by category.
5. Use *Corpus Viewer* to compare original vs cleaned text.
6. Use *Save Data* to save the cleaned data as `news-headlines.tab`

> 📝 **Bonus Task**: Try filtering words by minimum length (e.g., > 4 characters) and observe the effect.

---

## Comprehension Questions

1. What is tokenization, and why is it a critical step in NLP?
2. How does lemmatization differ from stemming?
3. Why might you want to remove stopwords from a text corpus?
4. What effect does lowercasing have on feature extraction?
5. What does the *Corpus Viewer* widget allow you to examine?

---

## Key Terms

- Preprocessing
- Tokenization
- Lemmatization
- Stopwords
- Normalization
- Corpus Viewer

---

## Notes

- Preprocessing choices affect downstream performance in classification, clustering, and topic modeling.
- You can chain multiple *Preprocess Text* widgets to experiment with different cleaning stages.
- Save this workflow as `cleaning-headlines.ows` for use in Chapter 4.

---

