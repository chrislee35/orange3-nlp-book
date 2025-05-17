# Chapter 8: Named Entity Recognition (NER)

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand what Named Entity Recognition (NER) is and why it's important.
- Identify common entity types such as people, organizations, and locations.
- Apply NER using the Orange environment with the `orange3-nlp` extension.
- Visualize and interpret named entities extracted from real-world datasets.

---

## 8.1 What is Named Entity Recognition?

**Named Entity Recognition (NER)** is a task in NLP that locates and classifies named entities in text into predefined categories such as:

- **PERSON** – names of people  
- **ORG** – organizations  
- **GPE** – countries, cities, or locations  
- **DATE**, **TIME**, **MONEY**, etc.

NER is used in:

- News and media analytics  
- Chatbot understanding  
- Document summarization  
- Knowledge graph construction

> 🧠 NER is often performed using rule-based systems, statistical models, or deep learning approaches (e.g., transformer-based).

---

## 8.2 Installing `orange3-nlp`

To use NER in Orange for this lab, you must install the `orange3-nlp` package. This package provides specialized widgets for advanced NLP functionality.

### Installation:

![Installing Add-ons](Add-on%20menu.png)

![Add-ons Widget](Text%20Add-on.png)

![Installing NLP Add-on](NLP%20Add-on.png)

💡 Restart Orange after installation to see the new widgets.

## 8.3 Using the Named Entity Recognizer Widget

### Example Workflow

1. Load a dataset using **File** (e.g., `news-headlines.tab`, `tweets.csv`)
2. Preprocess text with **Preprocess Text**
3. Add the widget: **Named Entity Recognition**
4. Connect to a **Data Table** or **Corpus Viewer** to inspect results

### Options (example)

- **Model selection**: spaCy small/NLTK/Flair/Ollama  
- **Filter by type**: PERSON, ORG, GPE, etc.  
- **Output columns**:
  - `entities`: list of extracted entities  
  - `entity_types`: parallel list of corresponding types  
  - (optional) `highlighted_text`: for visualization

### Model Selection Options
- **spaCy** is fast and moderately accurate.  
- **NLTK** is almost as fast as spaCy, not very accurate, but easiest to install.  
- **Flair** is almost cutting edge, requires lots of complex dependencies, and is moderately fast.  
- **Ollama** is very slow and inaccurate, however, it can be used for a lot of different tasks. We will use Ollama in Chapters 14 and 15.  

---

## 8.4 Visualizing and Filtering Entities

Use these widgets (assumed available via `orange3-nlp`):

- **Entity Viewer**: See highlighted entities in context  
- **Entity Frequency Plot**: Visualize most common names, organizations, or places  
- **Entity Type Filter**: Filter dataset to rows containing specific entity types  

> 🧪 Try filtering rows to only those mentioning a named location (e.g., `GPE`) for geospatial analysis.

---

## Lab Exercise 8A: Exploring Named Entities in News Headlines

**Goal**: Extract and visualize named entities from a collection of headlines.

**Steps**:

1. Load `news-headlines.csv`
2. Use **Preprocess Text** → **Named Entity Recognizer**
3. Connect to:
   - **Data Table** to review the extracted entities  
   - **Entity Frequency Plot** to see most mentioned people or organizations  
4. Answer:
   - Which entities appear most often?
   - What entity types dominate the headlines?

---

## Lab Exercise 8B: Filter for Locations in Tweet

**Goal**: Identify and analyze geographic mentions in tweets.

**Steps**:

1. Load `tweets-election.csv`
2. Run text through **Named Entity Recognizer**
3. Use **Entity Type Filter** set to `GPE`
4. Visualize filtered data with **Word Cloud** or **Data Table**

**Optional**:

- Combine with **Sentiment Scorer** to study how sentiment differs by location  
- Export results using the **Save Data** widget for external mapping

---

## Comprehension Questions

1. What is the difference between a named entity and a keyword?
2. Which entity types did you find most common in your dataset?
3. Why is filtering by entity type useful in analysis?
4. How would you use NER to enhance a chatbot or question-answering system?
5. What are some limitations of NER models?

---

## Key Terms

- Named Entity Recognition (NER)  
- Entity Type  
- PERSON, ORG, GPE, DATE, etc.  
- spaCy  
- Transformer Model  
- Entity Frequency  
- `orange3-nlp`

---

## Notes

- Save your NER workflows as `ner-news-headlines.ows` and `ner-tweets.ows`  
- You can use the extracted entity types in downstream tasks such as clustering or relation extraction  
- In the next chapter, you'll explore **Text Summation** to reduce larger texts to more managable summaries.

---

