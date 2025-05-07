# Chapter 11: Word Embeddings and Vector Representations

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand why word embeddings are used instead of one-hot or count-based vectors.
- Explore how word embeddings group similar words together in space.
- Use Orange to visualize pre-trained word vectors.
- Apply embeddings to cluster or compare words and documents based on meaning.
- Interpret vector relationships through interactive plots and similarity tools.

---

## 11.1 Why Word Embeddings?

Traditional models like bag-of-words or one-hot encodings treat each word as a unique, unrelated symbol. This has several drawbacks:

- **No sense of similarity** between words (e.g., "cat" and "kitten" are unrelated in a one-hot encoding).
- **Sparse and high-dimensional** data that’s inefficient for modeling.

**Word embeddings** solve this by placing words in a continuous vector space where:

- Similar words are **closer together**.
- Directions in space encode **semantic relationships**.

> Think of embeddings like a map of words: words that mean similar things are near each other on the map.

---

## 11.2 Common Embedding Models

Some common pre-trained word embedding models include:

- **Word2Vec**: Learns word associations using context windows.
- **GloVe**: Learns word co-occurrence patterns from a global corpus.
- **fastText**: Improves on Word2Vec by incorporating subword information.

For this lab, we’ll use **preloaded embeddings** via a custom widget or bundled dataset.

---

## 11.3 Using Word Embeddings in Orange

With your custom Orange widgets, the following tools will be available:

### Widgets Used

- **Word Embeddings**: Loads pre-trained embeddings (Word2Vec, GloVe, etc.)
- **Word Similarity Explorer**: Allows users to type in a word and find similar words by cosine similarity.
- **Word Embedding Plot**: Visualizes word vectors in 2D or 3D using t-SNE or PCA.
- **Distance Map / Clustering**: Groups words or documents based on semantic proximity.

### Example Workflow

1. Load a list of selected words or short documents (e.g., news headlines).
2. Use *Word Embeddings* to represent each word or document vector.
3. Visualize the embeddings in a *Word Embedding Plot*.
4. Explore relationships using *Distance Map*, *Clustering*, or *Similarity Explorer*.

---

## 11.4 Interpreting Word Relationships

### Examples to Try

- Search for: `"king"`, `"queen"`, `"man"`, `"woman"`
- What patterns do you notice in the 2D plot?

Try entering more groups like:

- `"apple"`, `"orange"`, `"banana"` (fruits)
- `"cat"`, `"dog"`, `"puppy"`, `"kitten"` (animals)
- `"paris"`, `"france"`, `"berlin"`, `"germany"` (cities and countries)

> 💡 Words with similar meanings tend to cluster together. Even word with opposite meanings can appear close because they occur in similar contexts (e.g., "good" and "bad").

---

## Lab Exercise 11A: Explore Embedding Space

**Goal**: Visualize word clusters and similarities.

**Steps**:

1. Load a word list (you can use a `File` widget with a `.txt` or `.csv` file).
2. Connect to the *Word Embeddings* widget to generate vector representations.
3. Connect to the *Word Embedding Plot* to visualize the space.
4. Use *Word Similarity Explorer* to find related terms.

**Questions**:

- Do semantically related words form tight clusters?
- Are there words that appear far from where you expect? Why?

---

## Lab Exercise 11B: Group Words by Category

**Goal**: Use embeddings to group words into categories without labeling them.

**Steps**:

1. Load a word list with mixed categories (e.g., animals, professions, emotions).
2. Pass it through *Word Embeddings* and then to a *Hierarchical Clustering* widget.
3. Visualize the dendrogram and interpret which clusters were formed.

**Optional**: Use *Distance Map* or *Silhouette Score* to evaluate cluster tightness.

---

## Comprehension Questions

1. What does it mean when two words are "close" in embedding space?
2. How is a word embedding different from a one-hot vector?
3. Why might "good" and "bad" appear near each other in a plot?
4. What are some practical tasks where embeddings are helpful?
5. In what ways can visualizing word vectors help guide your analysis?

---

## Key Terms

- Word Embedding
- Semantic Similarity
- Vector Representation
- Word2Vec
- GloVe
- Embedding Space
- t-SNE / PCA
- Clustering

---

## Notes

- Save your workflow as `word-embeddings.ows`.
- The next chapter will introduce document embeddings and sentence-level semantic search.

---

