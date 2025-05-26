# Choosing Embedding Models by Use Case

Text embedding models turn words, sentences, or documents into numerical vectors. These vectors are used in many NLP tasks. Below are common use cases and which models are good fits for each.

---

## 🔍 1. Keyword & Semantic Search

Use when: You want to match a user query to the most relevant document or passage.

**Recommended Models:**
- **E5 (e.g., `e5-small-v2`)** – Trained specifically for search tasks using "query:" and "passage:" prompts.
- **OpenAI's `text-embedding-ada-002`** – High-quality embeddings (requires API).
- **SBERT models (e.g., `all-MiniLM-L6-v2`)** – Fast, effective for short queries and passages.
- **nomic-embed-text** – Open-source alternative to commercial APIs with strong semantic search performance.

**Why**: These models capture *meaning* well, not just keywords, so they can match synonyms or related ideas.

---

## 📚 2. Document Clustering & Topic Modeling

Use when: You want to group similar texts together automatically (e.g., news articles, support tickets).

**Recommended Models:**
- **SBERT models** – Offer dense embeddings ideal for clustering.
- **E5** – Produces well-separated embeddings useful for grouping.
- **nomic-embed-text** – High-dimensional embeddings good for unsupervised clustering.
- **Doc2Vec** – Simpler model, can still be used for clustering longer texts.

**Why**: You need embeddings that place related documents close together in vector space.

---

## 🧠 3. Text Classification (e.g., spam detection, sentiment analysis)

Use when: You want to label documents with categories based on their content.

**Recommended Models:**
- **SBERT models** – Good for short to medium text inputs.
- **E5** – Strong zero-shot classification with prompt tuning.
- **Universal Sentence Encoder (USE)** – Easy to use for general tasks.

**Why**: These embeddings can be used directly as features for machine learning classifiers.

---

## 🧾 4. Semantic Similarity (e.g., duplicate detection, paraphrase identification)

Use when: You want to know if two texts mean the same thing.

**Recommended Models:**
- **SBERT models** – Trained specifically for this task.
- **InferSent** – Earlier model, simple and interpretable.
- **E5** – Also works well when texts are framed appropriately.

**Why**: These models are trained to measure *meaning overlap* rather than exact word matching.

---

## 🧰 5. General-Purpose Embeddings (All-rounder models)

Use when: You're not sure what task you're doing yet, or want a flexible model.

**Recommended Models:**
- **SBERT (`all-MiniLM-L6-v2`)** – Balanced performance and speed.
- **nomic-embed-text** – Open and versatile, suitable for search, clustering, and more.
- **USE** – Google’s general-purpose model with multilingual support.
- **OpenAI embeddings** – Strong across most tasks but proprietary.

---

## Summary Table

| Task                      | Best Model Types                            |
|---------------------------|---------------------------------------------|
| Keyword / Semantic Search | E5, OpenAI, SBERT, nomic-embed-text         |
| Document Clustering       | SBERT, E5, nomic-embed-text, Doc2Vec        |
| Text Classification       | SBERT, E5, USE                              |
| Semantic Similarity       | SBERT, InferSent, E5                        |
| General Use               | SBERT, nomic-embed-text, USE, OpenAI        |

---

