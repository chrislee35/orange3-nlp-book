# Chapter 12: Document Embeddings and Similarity

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand how document embeddings represent whole texts in vector space.
- Use Orange to compute and visualize similarity between documents.
- Apply embeddings to cluster, search, and explore texts based on meaning.
- Compare different methods for representing documents using embeddings.

---

## 12.1 From Word to Document Embeddings

While word embeddings help us understand individual word meanings, we often need to analyze entire **documents**, such as:

- Reviews
- Tweets
- News articles
- Transcripts

Document embeddings combine information from all words in a text into a single vector.

> Think of it like making a smoothie: each word contributes flavor (meaning), and the resulting vector captures the “overall taste” (topic/meaning) of the document.

---

## 12.2 How Are Document Embeddings Created?

Some simple and practical methods:

- **Averaging Word Embeddings**: Take all word vectors in a document and average them.
- **TF-IDF Weighted Averages**: Weight more important words higher in the average.
- **Pre-trained Sentence Embedding Models**: Use models like **Sentence-BERT**, **USE**, or **FastText sentence vectors**.

> In this chapter, we'll use averaged word embeddings, with support from custom widgets for simplicity and transparency.

---

## 12.3 Using Orange to Work with Document Embeddings

### Widgets Used

- **Corpus** or **File**: Load a dataset of texts (e.g., news headlines, movie lines, product reviews).
- **Preprocess Text**: Tokenization, normalization, filtering.
- **Word Embeddings**: Load pre-trained word vectors.
- **Document Embeddings**: Compute average (or weighted) vector per document.
- **Similarity Viewer**: View document-to-document cosine similarities.
- **t-SNE / PCA / MDS**: Visualize document clusters.
- **Distance Map** and **Hierarchical Clustering**: Explore relationships between documents.

### Example Workflow

File → Preprocess Text → Word Embeddings → Document Embeddings → (Visualization / Clustering / Similarity)

---

## 12.4 Exploring Document Similarity

Once each document is represented as a vector, we can:

- **Cluster similar documents** (e.g., product reviews by tone or topic)
- **Search for related documents** (e.g., "find all tweets similar to this one")
- **Visualize topic space** (e.g., plotting political speeches or movie plots)

> Cosine similarity helps us measure how “directionally” similar two document vectors are.

---

## Lab Exercise 12A: Visualizing Document Clusters

**Goal**: Identify meaningful clusters of similar texts.

**Steps**:

1. Load a dataset like `movie_lines.csv` or `news_headlines.csv`.
2. Preprocess the text and generate *Word Embeddings*.
3. Feed into *Document Embeddings* to create vectorized texts.
4. Visualize using *t-SNE*, *PCA*, or *MDS*.
5. Use *Data Table* or *Corpus Viewer* to examine clusters.

**Discussion**:
- What do documents in the same cluster have in common?
- Are clusters thematic (topic-based) or stylistic?

---

## Lab Exercise 12B: Document Similarity Search

**Goal**: Find documents most similar to a query.

**Steps**:

1. Use the same workflow from 12A.
2. Add a *Similarity Viewer* or a *Select Example* → *Distance Map* chain.
3. Select one document (e.g., a quote or headline).
4. View its top 5 most similar entries based on cosine distance.

**Discussion**:
- What kinds of documents are considered “close”?
- Would humans agree with the similarity ranking?

---

## Comprehension Questions

1. What is a document embedding, and how is it different from a word embedding?
2. Why do we use cosine similarity instead of Euclidean distance?
3. What is the purpose of dimensionality reduction (e.g., t-SNE) in visualizing embeddings?
4. What kind of clustering did you observe in your document embedding plots?
5. How could document embeddings be used in real-world applications?

---

## Key Terms

- Document Embedding
- Sentence Vector
- Averaged Word Embeddings
- Cosine Similarity
- t-SNE / PCA / MDS
- Semantic Search
- Clustering

---

## Notes

- Save your workflow as `document-embeddings.ows`.
- In the next chapter, we will explore **Topic Modeling** and how to uncover themes hidden in text corpora.

---

