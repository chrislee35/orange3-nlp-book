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

> 📌 Rule-based methods are especially useful for short texts like tweets or reviews.

### Machine Learning Sentiment Models

- Use labeled examples to train a classifier (e.g., positive vs. negative).
- Requires preprocessing, feature extraction, and evaluation.
- Can outperform rule-based methods with enough data.

> 💡 Combine approaches by using lexicon-based scores as features for a classifier.

---

### 7.2 Exercise: Analyzing Twitter Data

Goal: Analyze public sentiment in movie reviews using both rule-based and ML-based methods.

#### Dataset

Use a sample dataset like movie-reviews.csv or any collection of tweets labeled with text and (optionally) sentiment.

#### Workflow Setup

    1. Load `movie-reviews.tab` using *Corpus*.
    2. Preprocess with *Preprocess Text*.
    3. Apply *Sentiment Analysis*.
    4. Visualize results:
        * Box Plot: sentiment by topic or hashtag
        * Data Table: explore individual tweet scores
        * Distributions or Histogram: analyze overall sentiment spread

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

    * Save your sentiment workflows as movie-reviews-sentiment.ows.
    * In future chapters, you’ll explore advanced NLP techniques using deep embeddings and transformer models.

---

