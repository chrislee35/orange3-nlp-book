# Chapter 7: Sentiment Analysis

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the difference between rule-based and machine learning approaches to sentiment analysis.
- Use Orange widgets and custom scripts to analyze sentiment in text data.
- Apply sentiment classification to real-world social media data.
- Interpret and visualize sentiment trends across a dataset.

---

## 7.1 Rule-Based vs Machine Learning Approaches

### Rule-Based Sentiment Analysis

- Uses a dictionary or lexicon of words labeled with positive/negative/neutral scores.
- No training data required.
- Fast and interpretable.
- Example tools: VADER, TextBlob, SentiWordNet.

> 📌 Rule-based methods are especially useful for short texts like tweets or reviews.

### Machine Learning Sentiment Models

- Use labeled examples to train a classifier (e.g., positive vs. negative).
- Requires preprocessing, feature extraction, and evaluation.
- Can outperform rule-based methods with enough data.

> 💡 Combine approaches by using lexicon-based scores as features for a classifier.

---

## 7.2 Applying Sentiment Widgets and Custom Scripts

### Using Orange's Built-in Tools

If using a custom widget pack (e.g., `Sentiment Scorer`, `VADER Widget`, or `Sentiment Preprocessor`):

1. Load data using *File* or *Corpus*.
2. Preprocess text (cleaning, tokenization).
3. Apply the *Sentiment Widget* to assign polarity scores.
4. Visualize results with *Box Plot*, *Scatter Plot*, or *Data Table*.

### Using Python Scripts in Orange

For advanced tasks, Orange's *Python Script* widget can import tools like `nltk`, `vaderSentiment`, or `textblob`.

Example script (VADER-based sentiment):

```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
out_data = in_data.copy()
out_data[:, "sentiment"] = [analyzer.polarity_scores(text)["compound"] for text in in_data[:, "text"]]
```

### 7.3 Exercise: Analyzing Twitter Data

Goal: Analyze public sentiment in tweets using both rule-based and ML-based methods.
Dataset

Use a sample dataset like tweets-election.csv or any collection of tweets labeled with text and (optionally) sentiment.

#### Workflow Setup

    1. Load tweets using File and Corpus.
    2. Preprocess with Preprocess Text.
    3. Apply Sentiment Scorer (or use a custom script).
    4. Visualize results:
        * Box Plot: sentiment by topic or hashtag
        * Data Table: explore individual tweet scores
        * Distributions or Histogram: analyze overall sentiment spread

#### Optional ML Extension

    1. If labeled sentiment data is available, train a classifier (e.g., Logistic Regression).
    2. Use Test & Score to compare ML model to rule-based sentiment.
    3. Analyze where the models agree or disagree.

### Comprehension Questions

    1. What are the strengths and limitations of rule-based sentiment analysis?
    2. Why might a machine learning model outperform a lexicon-based one?
    3. What does a compound score of -0.7 in VADER represent?
    4. How can visualization help in understanding sentiment patterns?
    5. When analyzing tweets, what preprocessing steps are particularly important?

## Key Terms

    * Sentiment Analysis
    * Rule-Based vs. Machine Learning
    * VADER (Valence Aware Dictionary)
    * Lexicon
    * Compound Score
    * Polarity
    * Subjectivity

## Notes

    * Save your sentiment workflows as twitter-sentiment.ows.
    * In future chapters, you’ll explore advanced NLP techniques using deep embeddings and transformer models.