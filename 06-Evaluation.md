# Chapter 6: Model Evaluation and Tuning

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the importance of evaluating machine learning models.
- Use cross-validation and train/test split methods in Orange.
- Compare multiple classifiers using performance metrics.
- Tune hyperparameters to improve model performance.

---

## 6.1 Why Evaluate Models?

Evaluating models helps ensure they generalize well to new, unseen data.

Common goals of evaluation:

- Compare different models fairly.
- Detect overfitting or underfitting.
- Optimize model performance via tuning.

> ⚠️ A model that performs well on training data but poorly on test data is **overfitting**.

---

## 6.2 Train/Test Split vs. Cross-Validation

### Train/Test Split

- Divides the data into two parts: training and testing.
- Simple, but results may vary depending on the split.

### Cross-Validation (CV)

- Splits the data into *k* parts (folds) and rotates which fold is used for testing.
- More stable and reliable for evaluation.

> 🧪 Orange’s *Test & Score* widget supports both methods.

---

## 6.3 Comparing Classifiers in Orange

You can compare several models at once using:

### Workflow Setup

1. *File* + *Corpus* → Load and preprocess text
2. *TF-IDF* → Convert to numeric features
3. Add multiple learners (e.g., Naive Bayes, Logistic Regression, Random Forest)
4. Connect them all to *Test & Score*

### Metrics Provided

| Metric       | Description                               |
|--------------|-------------------------------------------|
| Accuracy     | Overall correctness of the model          |
| Precision    | Proportion of predicted positives that are correct |
| Recall       | Proportion of actual positives that were predicted |
| F1 Score     | Balance between precision and recall      |
| AUC          | Area Under the ROC Curve (for binary)     |

> 📈 Try using *Box Plot* on *Test & Score* output to visually compare models.

---

## 6.4 Tuning Model Parameters

### What is Hyperparameter Tuning?

- Some models have configurable parameters that affect their behavior.
- Tuning helps find the best combination for performance.

### Orange Widgets for Tuning

- *Logistic Regression*, *Random Forest*, and others allow configuration directly.
- Use the *Rank* widget (optional) to find best features.
- For custom tuning, you can use Orange Python scripting or a custom widget.

---

## Lab Exercise 6A: Compare Classifiers on Headlines

**Goal**: Compare the performance of three classifiers on the news headline dataset.

**Steps**:

1. Load and preprocess `news-headlines.csv`.
2. Extract TF-IDF features.
3. Connect Naive Bayes, Logistic Regression, and Random Forest to *Test & Score*.
4. Evaluate using 10-fold Cross-Validation.
5. Use *Confusion Matrix* and *Box Plot* for deeper insights.

---

## Lab Exercise 6B: Tune the Random Forest Classifier

**Goal**: Tune the number of trees and depth of the Random Forest model.

**Steps**:

1. Preprocess your data as in 6A.
2. Click the settings icon on the *Random Forest* widget.
3. Adjust parameters:
   - Number of Trees (e.g., 10, 50, 100)
   - Max Depth (e.g., None vs. 10 vs. 20)
4. Compare performance changes in *Test & Score*.

> 📝 Record which combination gives the best accuracy and F1 score.

---

## Comprehension Questions

1. What is the main advantage of cross-validation over a simple train/test split?
2. Which performance metric is most useful for imbalanced datasets? Why?
3. How does increasing the number of trees in a Random Forest affect performance?
4. What are some signs that a model is overfitting?
5. How can *Box Plot* help you make decisions between classifiers?

---

## Key Terms

- Cross-Validation
- Train/Test Split
- Overfitting
- Hyperparameters
- Model Tuning
- Performance Metrics
- Confusion Matrix
- AUC

---

## Notes

- Save your comparison workflow as `classifier-evaluation.ows`.
- In the next chapter, you will begin working with **custom text widgets** for advanced NLP tasks like named entity recognition and transformer embeddings.

