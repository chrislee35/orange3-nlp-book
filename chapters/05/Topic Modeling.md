# Chapter 5: Clustering and Topic Modeling

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the difference between clustering and topic modeling in NLP.
- Perform unsupervised grouping of documents using clustering algorithms.
- Use topic modeling to discover latent themes in a text corpus.
- Visualize and interpret cluster/topic results using Orange widgets.

---

## 5.1 Unsupervised Learning for Text

Unlike classification, **unsupervised learning** finds structure in unlabeled data. In NLP, common unsupervised tasks include:

- **Clustering**: Groups similar documents together.
- **Topic Modeling**: Identifies abstract topics based on word distributions.

These techniques are especially useful for **exploration**, **summarization**, or **preprocessing**.

---

## 5.2 Clustering with Orange

### Common Clustering Algorithms

| Algorithm | Description |
|----------|-------------|
| K-Means | Partitions documents into K groups based on feature similarity. |
| Hierarchical Clustering | Builds a tree of document clusters (dendrogram). |
| DBSCAN | Density-based clustering, useful for detecting outliers. |

> Orange includes K-Means and Hierarchical Clustering by default.

### Clustering Workflow

1. *Corpus* → Load dataset (e.g., `book-excerpts`)
2. *Preprocess Text* → Clean the corpus
3. *Bag of Words* → Convert text to features
4. *Distances* → Create a measurement of how similar the instances are.
5. *Hierarchical Clustering* → Group similar documents

![Clustering Workflow Example](./Clustering%20Workflow.png)

![Bag of Words using TF-IDF](./Bag%20of%20Words%20TF-IDF.png)

![Hierarchical Clustering Example](./Hierarchical%20Clustering.png)

> Even though the instances are noted by their class, the class was not used to train or fit the clustering.  It is included to show you how well or poorly the clustering grouped like items.

---

## 5.3 Topic Modeling with LDA

**Latent Dirichlet Allocation (LDA)** is a probabilistic topic model. It assumes:

- Each document is a mixture of topics.
- Each topic is a distribution over words.

### Topic Modeling Workflow

1. Load and preprocess your corpus (e.g., `BBC3`).
2. Use the *Topic Modeling* widget (LDA) to extract topics.
3. Visualize results with *MDS*.

> 📌 Each document receives a topic distribution; the top topic is often used as a soft label.

![Topic Modeling Workflow](./Topic%20Modeling%20Workflow.png)

![Topic Modeling LDA](./Topic%20Modeling-LDA.png)

![Topic Modeling MDS](./Topic%20Modeling%20MDS.png)

![Topic Modeling Workflow with Word Cloud](./Topic%20Modeling%20Workflow%20with%20Word%20Cloud.png)

![Word Cloud for 3rd Topic](./Word%20Cloud.png)

---

## 5.4 Visualizing and Interpreting Results

### For Clustering:

- Use *Scatter Plot* to view document distribution by cluster.
- Use *Distances* + *Hierarchical Clustering* for dendrograms.

### For Topics:

- Use *Word Cloud* to show top words per topic.
- Use *Corpus Viewer* to explore which documents are assigned to which topics.

---

## Lab Exercise 5A: Cluster Book Excerpts

**Goal**: Group book excerpts based on language similarity.

**Steps**:

1. Load `book-excerpts.tab` using the *Corpus* widget.
2. Preprocess the text and extract features using TF-IDF.
3. Apply *K-Means* with 3–5 clusters.
4. Use *Scatter Plot* to view clustering structure.

**Questions to Explore**:
- Do excerpts of the same genre tend to cluster together?
- Which words are most associated with each cluster?

---

## Lab Exercise 5B: Discover Topics in Headlines

**Goal**: Use topic modeling to find major themes in news headlines.

**Steps**:

1. Load `BBC3` dataset, convert to a *Corpus*, and preprocess the text.
2. Convert text to Bag-of-Words vectors.
3. Use *Topic Modeling* (LDA) to extract 5–10 topics.
4. Use *Corpus Viewer* to examine top documents per topic.

**Questions to Explore**:
- What are the most common words in each topic?
- Can you label each topic with a meaningful name?

---

## Comprehension Questions

1. What is the difference between clustering and topic modeling?
2. How does K-Means determine similarity between documents?
3. What does LDA assume about documents and topics?
4. How might you use topic modeling in a real-world application?
5. Why is preprocessing important before unsupervised analysis?

---

## Key Terms

- Clustering
- Topic Modeling
- K-Means
- LDA (Latent Dirichlet Allocation)
- TF-IDF
- Bag of Words
- Unsupervised Learning

---

## Notes

- Save your workflows as `clustering-books.ows` and `topics-headlines.ows`.
- In the next chapter, you’ll learn to fine-tune models and compare different configurations.

---

