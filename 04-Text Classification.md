# Chapter 4: Text Classification

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the concept of text classification.
- Convert text into numerical features using Bag-of-Words and TF-IDF.
- Train and evaluate machine learning models for classifying text.
- Visualize model performance using accuracy, precision, recall, and confusion matrices.

---

## 4.1 What is Text Classification?

Text classification is the task of assigning predefined categories or labels to text. Common examples include:

- Spam vs. Ham detection
- Sentiment classification (positive, neutral, negative)
- Topic labeling (e.g., Politics, Sports, Business)

Text classification is a **supervised learning** task: you train a model on labeled examples and use it to predict the labels of new, unseen data.

---

## 4.2 Representing Text Numerically

Before we can train a model, we must represent text as numeric features. Common techniques include:

### Bag of Words (BoW)

- Counts how often each word appears in a document.
- Simple but effective for many tasks.

### TF-IDF (Term Frequency–Inverse Document Frequency)

- Weights terms based on how unique they are across documents.
- Helps reduce the influence of common but uninformative words.

> 🧠 Orange provides the *Bag of Words* and *TF-IDF* widgets for easy feature extraction.

---

## 4.3 Building a Classification Workflow

Let’s build a workflow that classifies news headlines by topic.

### Recommended Widgets:

- *File* → Load `news-headlines.csv`
- *Corpus* → Convert text to Orange format
- *Preprocess Text* → Clean the text
- *TF-IDF* or *Bag of Words* → Convert to numeric features
- *Logistic Regression* or *Naive Bayes* → Train classifier
- *Test & Score* → Evaluate performance
- *Confusion Matrix* → Visualize results

---

## 4.4 Evaluating Classifier Performance

### Common Metrics:

- **Accuracy**: % of correct predictions
- **Precision**: Correct positives / Predicted positives
- **Recall**: Correct positives / Actual positives
- **F1 Score**: Harmonic mean of precision and recall

> 📊 Orange’s *Test & Score* widget automatically computes these metrics and more.

### Confusion Matrix

The *Confusion Matrix* widget shows the breakdown of predicted vs actual labels, which is helpful for error analysis.

---

## Lab Exercise 4: Classify News Headlines

**Goal**: Build a workflow that classifies headlines by topic.

**Steps**:

1. Load the `news-headlines.csv` file.
2. Preprocess the text (e.g., lowercase, remove stopwords).
3. Convert the cleaned text to TF-IDF vectors.
4. Train a classifier (try both Naive Bayes and Logistic Regression).
5. Evaluate the model using *Test & Score* and inspect results using *Confusion Matrix*.

> 📝 **Optional Challenge**: Try using *Random Forest* and compare its performance to Naive Bayes.

---

## Comprehension Questions

1. What is the difference between Bag-of-Words and TF-IDF?
2. Why is preprocessing important before training a classifier?
3. What does high accuracy but low precision indicate?
4. How does the *Confusion Matrix* help you understand model behavior?
5. Which classifier performed best on your data? Why might that be?

---

## Key Terms

- Text Classification
- Bag of Words
- TF-IDF
- Supervised Learning
- Precision, Recall, F1 Score
- Confusion Matrix

---

## Notes

- Save your workflow as `headline-classifier.ows` for reuse in future chapters.
- In later chapters, you’ll experiment with cross-validation, parameter tuning, and interpretability.

---

