# Chapter 14: Using a Large Language Model

## Learning Objectives

By the end of this chapter, you will be able to:

- Explain what a large language model (LLM) is and why one model can do many different tasks.
- Install Ollama, download a model, and connect Orange to it.
- Run sentiment analysis, classification, summarization, and free-form generation on the same documents, using the Ollama widgets and the *Text Generator*.
- Read a prompt as the "program" that tells the model what to do, and explain how changing it changes the result.
- Compare an LLM with a classical NLP method on speed, repeatability, and accuracy, and decide when each is the better tool.

---

## 14.1 What Is a Large Language Model?

In Chapter 13 you saw that a language model predicts the next word. A **large language model (LLM)** is the same idea trained at a much larger scale: billions of adjustable numbers (called *parameters*), trained on an enormous amount of text. Two things happen at that scale:

- The model picks up grammar, facts, and styles of writing, along with many patterns of reasoning.
- It can be *instructed*. After extra training on examples of requests and good answers, a model such as `phi4-mini` treats your text as a task: "summarize this", "is this positive or negative?", "reply to this customer".

The result is a **generalist**. Chapters 4 to 10 built one model per task. With an LLM, you keep one model and change the **prompt**.

### Local or hosted?

An LLM can run on your own computer or on someone else's server:

| | Local (Ollama) | Hosted (a company's API) |
|---|---|---|
| **Privacy** | Text never leaves your machine | Text is sent to a third party |
| **Cost** | Free once downloaded | Pay per use |
| **Quality** | Smaller models, weaker on hard tasks | Largest models, strongest |
| **Speed** | Limited by your hardware | Fast, but depends on the network |
| **Works offline** | Yes | No |

This book uses a local model so that the exercises are free, private, and repeatable on a laptop.

---

## 14.2 Running a Model on Your Computer with Ollama

**Ollama** is a free program that downloads language models and serves them to other programs on your computer. Orange's LLM widgets talk to it. It runs as a background server, by default at `localhost:11434`.

**Install Ollama** from [ollama.com/download](https://ollama.com/download):

- **macOS** and **Windows**: download the installer and run it.
- **Linux**: run the install script shown on the download page.

**Download the book's model.** In a terminal:

```
ollama pull phi4-mini
```

This model is about 2.5 GB, so the download takes a few minutes, and it needs at least that much free memory to run. Larger models are better but need much more memory and are slower on a laptop.

**Check that it works:**

```
ollama list
ollama run phi4-mini "Say hello in one sentence."
```

`ollama list` should show `phi4-mini`. If an Orange widget cannot find the model, the usual causes are that Ollama is not running or that the model has not been pulled.

---

## 14.3 The Prompt Is the Program

Each LLM widget is a *prompt template* with your text inserted. The Ollama widgets in this chapter build prompts like these (the wording is in the widgets' source code):

| Widget | Prompt sent for each document |
|--------|-------------------------------|
| Ollama Sentiment Analyzer | `Determine the sentiment of the following text as Positive, Negative, or Neutral. Respond with one word only.` + the text |
| Ollama Text Classification | `Given the following text, classify it as one of the following: <your labels>. Respond with only one word from the list. Do not add anything else.` + the text |
| Ollama Summarizer | `Please provide a very short summary of the following document:` + the text |

A good prompt states the **task**, the **allowed answers**, and the **format** ("respond with one word only"). The sentiment and classification prompts ask for one word because a program has to read the answer. Asking a model to choose among labels it was never trained on, with no examples, is called **zero-shot classification**. It works because the model was instructed, but it still depends on the model following the instruction, and a model sometimes does not (you will see an example in 14A).

---

## 14.4 The Widgets

| Widget | Package | What it does |
|--------|---------|--------------|
| **Ollama Sentiment Analyzer** | orange3-ollama | Adds a `Sentiment` column (Positive, Negative, Neutral). |
| **Ollama Text Classification** | orange3-ollama | Adds a `Prediction` column using the labels you type in, or free-form labels if you give none. |
| **Ollama Summarizer** | orange3-ollama | Adds a `Summary` column. |
| **Text Generator** | orange3-nlp | Runs any prompt template you write, once per document, with temperature, seed, and samples. |
| **Sentiment Analysis** | Orange3-Text | A classical, lexicon-based method (VADER), used in 14C for comparison. |

Things to know before you start:

- The Ollama widgets read only **text columns** (string columns), and they add a column named `Sentiment`, `Prediction`, or `Summary`. If your data already has a column with one of those names, rename it first, or the widget fails.
- They run when you press their button (**Analyze Sentiment**, **Classify Text**, **Summarize Documents**), not automatically, and they have no setting for temperature or seed. The *Text Generator* has both.
- A model that is still loading or a long document can make a run take a while. Wait for the progress bar to finish before you connect the next widget.

![The LLM task workflow for exercises 14A–14C](14-workflow-overview.png)

---

## Lab Exercise 14A: One Dataset, Three Tasks

**Goal**: Apply sentiment analysis, classification, and summarization to the same messages, and check each against the truth.

**Dataset**: `customer-messages.tab` (12 short customer messages). Each message has a true `Topic` (shipping, billing, product, or account) and a true `Tone` (Positive, Negative, or Neutral), so you can score the model. Some messages are tricky on purpose: a sarcastic one, a mixed one, and a neutral question.

**Steps**:

1. Load the dataset with *Corpus*. The text feature is `Message`.
2. Connect *Corpus* to **Ollama Sentiment Analyzer**. Set the model to `phi4-mini:latest` and the text feature to `Message`. Press **Analyze Sentiment** and wait for the progress bar to finish.
3. Connect its output to **Ollama Text Classification**. Add the labels `shipping`, `billing`, `product`, and `account`, then press **Classify Text**.
4. Connect that output to **Ollama Summarizer** and press **Summarize Documents**. This step takes the longest.
5. Connect the summarizer to a *Data Table*. Compare the `Sentiment` and `Prediction` columns with the true `Tone` and `Topic`.

![Data Table with the true Tone and Topic next to the LLM's Sentiment, Prediction and Summary columns](14A-table.png)

**Questions**:

- How many sentiments and topics match the truth? Which messages does the model get wrong? Look closely at the sarcastic message, the mixed one, and the neutral questions.
- Look at the `Prediction` column. Does every answer come from your list of labels? What does that tell you about how reliably a model follows "respond with only one word from the list"?
- Remove the labels and classify again. What kinds of labels does the model invent? Why is that a problem if you want to count messages by topic?
- Run the summarizer a second time. Are the summaries identical? Do they keep the key facts?

---

## Lab Exercise 14B: Writing Your Own Prompt

**Goal**: Do a task that has no ready-made widget, by writing the prompt yourself.

**Steps**:

1. Connect *Corpus* to a *Text Generator*. Choose the **Ollama** backend and the model `phi4-mini`.
2. Use this prompt template, which runs once per message:

   ```
   Write a polite two-sentence reply from customer support to this message:

   {Message}
   ```

3. Set the temperature to `0.7`, **Samples per prompt** to 3, and tick **Fixed seed**. Press **Generate** and read the replies in a *Data Table*.
4. Set the temperature to `0` and generate again. Compare.
5. Change the prompt so the model must return a small structured answer:

   ```
   Extract the main issue from the message as JSON with keys "topic" and "urgent" (true or false). Reply with JSON only.

   Message: {Message}
   ```

![Data Table of three generated replies for each customer message](14B-replies.png)

**Questions**:

- How different are the three replies to the same message at temperature `0.7`? At temperature `0`?
- Read the replies as a customer would. Do they promise anything the company never agreed to (a refund, a deadline, an investigation)? Do any contain a leftover placeholder such as `[Your Name]`?
- In step 5 the prompt says "Reply with JSON only". Is the answer exactly JSON? What would a program that expects JSON have to do first?
- Which of your own ideas could be a prompt? Write one and test it on three messages.

---

## Lab Exercise 14C: LLM or Classical?

**Goal**: Compare the LLM with a classical sentiment method on the same messages.

**Steps**:

1. Connect *Corpus* to **Sentiment Analysis** (Orange3-Text) and choose the **VADER** method. View the result in a *Data Table*.
2. VADER gives a score from -1 (very negative) to +1 (very positive). Turn each score into a label: Positive above `0.05`, Negative below `-0.05`, Neutral otherwise.
3. Compare the VADER labels with the true `Tone` and with the LLM's `Sentiment` column from 14A.

![Data Table of VADER's positive, negative, neutral and compound scores next to the true Tone](14C-vader.png)

**Questions**:

- Which method gets more of the 12 messages right? Where do they disagree?
- Does VADER understand the sarcastic message? Why or why not? (Hint: how does it work?)
- Which method is faster? Which gives the same answer every time you run it?
- You need to score 5 million product reviews tonight, on one laptop. Which method would you use, and what would you check first?

> 📝 **Reflection:** An LLM is more flexible, but it is slower, can vary between runs, and can ignore instructions. A classical method is fast and repeatable, but narrow. For a real project, how would you decide? What would you measure on a small labeled sample before you chose?

---

## Comprehension Questions

1. What advantages do LLMs offer over task-specific models?
2. What is a prompt template, and how does changing the prompt change what the same model does?
3. Why does an LLM sometimes answer "Support" when asked to choose from a list that does not contain it?
4. What privacy and cost reasons favor running a model locally with Ollama?
5. Give two reasons the output of an LLM may differ from run to run, and one way to make it more repeatable.
6. When might you still prefer a traditional NLP pipeline over an LLM?

---

## Key Terms

- Large language model (LLM)
- Parameters
- Instruction-tuned model
- Prompt / prompt template
- Ollama
- Local vs hosted model
- Zero-shot classification
- Temperature / seed
- Hallucination

---

## Notes

- Save your workflow as `llm-tasks.ows`.
- LLMs answer from what they learned in training, which may be out of date or wrong. Chapter 15 adds **retrieval**, so the model answers from your own documents.
