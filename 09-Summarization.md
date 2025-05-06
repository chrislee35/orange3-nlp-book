# Chapter 9: Text Summarization

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the difference between extractive and abstractive summarization.
- Apply automatic summarization to documents using Orange and the `orange3-nlp` extension.
- Explore strategies for scaling summarization workflows to large corpora.
- Evaluate summaries using key heuristics and human judgment.

---

## 9.1 What is Text Summarization?

Text summarization is the task of automatically generating a concise and coherent version of a longer document while preserving its key information.

There are two main types:

- **Extractive summarization**: Selects and joins key sentences or phrases from the original text.
- **Abstractive summarization**: Generates new sentences that paraphrase and condense the original content (more similar to how humans summarize).

Use cases include:

- News aggregation  
- Scientific article previews  
- Legal and compliance documentation  
- Social media monitoring  

---

## 9.2 Using Summarization Widgets in Orange

Several widgets provided by `orange3-nlp` will help you explore summarization:

- **Text Summarizer** (extractive)
- **Abstractive Summarizer** (if transformer support is configured)
- **Summary Viewer**
- **Summary Quality Estimator** (optional)

### Workflow Example

1. Use **File** to load `long-articles.csv`.
2. Preprocess text with **Preprocess Text**.
3. Add **Text Summarizer** to extract sentence-level summaries.
4. Optionally compare with **Abstractive Summarizer** if supported.
5. Output to **Summary Viewer** or save using **Save Data**.

---

## 9.3 Extractive vs Abstractive Approaches

| Feature | Extractive | Abstractive |
|--------|------------|-------------|
| Method | Sentence ranking | Language generation |
| Output | Original text fragments | Paraphrased new text |
| Complexity | Low | High |
| Speed | Fast | Slower |
| Accuracy | High for factual precision | More human-like summaries |

Abstractive models typically require transformer-based architectures and more compute. These may be explored more deeply in Chapter 13 using **Large Language Models** with `orange3-ollama`.

---

## 9.4 Scaling Summarization for Large Texts

When summarizing large documents or corpora, consider:

- **Chunking**: Break texts into paragraphs or sections before summarization.
- **Batch Processing**: Use Orange workflows to process in parallel (with multiple **Text Summarizer** widgets if supported).
- **Caching and Checkpoints**: Save intermediate results to disk for reusability.
- **Hybrid Summaries**: Summarize paragraphs first, then summarize those summaries.

> 💡 In Chapter 13, you will learn how to leverage LLMs via `orange3-ollama` to generate high-quality abstractive summaries even from very large texts.

---

## Lab Exercise 9A: Summarizing News Articles

**Goal**: Generate summaries from long-form news content.

**Steps**:

1. Load `news-articles.csv`
2. Preprocess text → **Text Summarizer**
3. Output to **Data Table** or **Summary Viewer**
4. Compare:
   - How informative is the summary?
   - Are key facts preserved?

Optional:
- Add **Abstractive Summarizer** and compare the results.

---

## Lab Exercise 9B: Compare Summaries of Academic Abstracts

**Goal**: Understand the differences in summarization style and quality.

**Steps**:

1. Load `abstracts.csv`
2. Preprocess and pass through both **Text Summarizer** and **Abstractive Summarizer**
3. Use **Data Table** to view side-by-side results
4. Rate each summary’s quality using:
   - Coverage of main idea
   - Fluency
   - Conciseness

---

## Comprehension Questions

1. What are the core differences between extractive and abstractive summarization?
2. When might extractive summarization be preferable?
3. What challenges arise when summarizing very long documents?
4. How can chunking improve summarization workflows?
5. Why might you choose to integrate LLMs for summarization, as we will see in Chapter 13?

---

## Key Terms

- Extractive Summarization  
- Abstractive Summarization  
- Sentence Ranking  
- Text Compression  
- Chunking  
- `orange3-nlp`  
- `orange3-ollama`  

---

## Notes

- Save your workflows as `summarize-news.ows` and `summarize-abstracts.ows`.  
- You can chain summarization with topic modeling or classification tasks.  
- Look ahead to **Chapter 13**, where we will use Large Language Models for advanced summarization tasks.
