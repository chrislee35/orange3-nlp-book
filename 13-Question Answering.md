# Chapter 13: Question Answering and Text Generation

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the basic concepts behind question answering (QA) and generative NLP models.
- Use custom Orange widgets to explore simple QA pipelines and generate text.
- Compare extractive vs. generative approaches.
- Perform document-based question answering on small corpora.
- Experiment with auto-completion and response generation.

---

## 13.1 What is Question Answering?

**Question Answering (QA)** systems aim to extract or generate answers to user questions from a text or knowledge base.

There are two main approaches:

- **Extractive QA**: Pulls exact answers from documents (e.g., "What year was NASA founded?" → "1958").
- **Generative QA**: Produces original, often paraphrased, responses using a language model (e.g., "NASA was established in 1958").

---

## 13.2 What is Text Generation?

Text generation is the process of creating natural-sounding text, typically using language models like:

- GPT
- BERT (for masked word completion)
- T5 / BART (for summarization, QA, generation)

> Think of text generation as "autocomplete on steroids" — models are trained to predict what comes next, fill in blanks, or answer questions in fluent natural language.

---

## 13.3 Using Orange for QA and Generation

Your custom widgets will enable interaction with pre-trained models for:

- **Contextual QA**: Ask questions based on loaded documents.

### Widgets Used

- **Corpus**: Load a document or set of paragraphs.
- **Question Answering**: Accepts a question and retrieves an answer from context.
- **Corpus Viewer**: View output corpus.

![Figure X. Question and Answers for "Who Died?" against the Book Excerpts corpus](imgs/13-3%20Question%20Answer.png)

---

## 13.4 Comparing QA Approaches

| Approach       | Model Type       | Example Output                              |
|----------------|------------------|----------------------------------------------|
| Extractive     | BERT-style       | "1958" from NASA history paragraph           |
| Generative     | GPT-style        | "NASA was founded in the year 1958..."       |

You can explore both styles using your widgets. Try different contexts and questions to see how the models behave.

---

## Lab Exercise 13A: Ask Me Anything (Contextual QA)

**Goal**: Use extractive QA to find answers in a document.

**Steps**:

1. Load a news article or Wikipedia paragraph with the *File* or *Corpus* widget.
2. Connect to the *QA Generator* widget.
3. Type questions related to the content.
4. View extracted answers and their confidence scores (if available).

**Try Asking**:
- Who is mentioned?
- What happened?
- When and where did it occur?

---

## Lab Exercise 13B: Prompt-Based Text Generation

**Goal**: Use a generative model to extend a given prompt.

**Steps**:

1. Open the *Text Generator* widget.
2. Enter a seed prompt like:
    - “Once upon a time in a distant galaxy…”
    - “The most surprising thing about climate change is…”
3. Generate text and analyze the result.
4. Try modifying prompts to guide tone, subject, or style.

**Optional**: Experiment with temperature or length settings (if available).

---

## Comprehension Questions

1. What is the difference between extractive and generative QA?
2. In which scenarios might you prefer a generative model?
3. What limitations did you observe with either approach?
4. How does prompt phrasing affect the output of a text generation model?
5. Why is it important to consider model biases or hallucinations in generative output?

---

## Key Terms

- Question Answering (QA)
- Extractive QA
- Generative QA
- Language Model
- Prompt Engineering
- Text Completion

---

## Notes

- Save your workflows as `qa-generator.ows` and `text-generator.ows`.
- In the next chapter, we’ll explore **Topic Modeling** and thematic extraction from large text corpora.

---

