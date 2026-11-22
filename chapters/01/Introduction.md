# Chapter 1: Introduction to NLP and Data Mining

## Learning Objectives

By the end of this chapter, you will be able to:

- Define Natural Language Processing (NLP) and give examples of where you already use it.
- Explain why human language is hard for a computer, and what it means to turn unstructured text into structured data.
- Describe the stages of an NLP pipeline and find where each stage appears in this book.
- Explain what data mining adds to NLP, and how Orange's visual workflows make the steps easy to see and repeat.
- Read a simple table of features and a scatter plot, which is the same habit you will use on text from Chapter 3 onward.

---

## 1.1 What Is Natural Language Processing?

**Natural Language Processing (NLP)** is the field of getting computers to work with human language: to read it, sort it, search it, summarize it, translate it, and write it. It sits between computer science, linguistics, and data science.

You already use NLP every day:

- Auto-complete and spelling correction when you type
- Spam filters that decide which email you see
- Search engines that find a page that does not contain your exact words
- Voice assistants and chatbots
- Translation, captions, and summaries of long documents

### Why language is hard

A table of numbers is easy for a computer. A sentence is not, for several reasons:

- **Ambiguity.** "I saw her duck" has at least two meanings. "Bank" is a river edge or a place for money. "Can you pass the salt?" is a request, not a question about your ability.
- **Context.** "It was cold" means something different in a weather report, a restaurant review, and a story about a rude host.
- **Variety.** People write the same idea many ways ("great", "excellent", "loved it", "not bad at all") and the same word many ways ("run", "runs", "ran", "running").
- **Noise.** Real text has typos, slang, emoji, sarcasm, and several languages in one message.
- **Scale.** More text is written in a day than anyone could read in a lifetime.

Much of this book is about handling these problems in sensible ways, and about knowing where the methods still fail.

---

## 1.2 From Unstructured Text to Structured Data

A **structured** dataset is a table. Each row is one thing, and each column is one measured property of it. Orange, like most data mining tools, works on tables.

| Flower | Sepal length | Sepal width | Petal length | Petal width | Species |
|--------|-------------:|------------:|-------------:|------------:|---------|
| 1 | 5.1 | 3.5 | 1.4 | 0.2 | setosa |
| 2 | 7.0 | 3.2 | 4.7 | 1.4 | versicolor |

A text is **unstructured**: it is a sequence of words with no fixed columns. The central move in NLP is to **turn each text into a row of numbers** so that the same tools can be applied to it. There are many ways to do this, and the book covers three families:

| Way of making a row | Example idea | Chapters |
|---------------------|--------------|----------|
| **Count words** | One column per word, and the value is how often it appears (*Bag of Words*, *TF-IDF*) | 3 to 6 |
| **Look up meaning in a list** | A sentiment score from a dictionary of words | 7 |
| **Let a model describe it** | A vector of a few hundred numbers from a neural network (*embeddings*) | 11 to 15 |

Once texts are rows, you can ask the familiar questions: which rows are similar, which belong to the same group, which can be predicted from the others.

---

## 1.3 What Is Data Mining?

**Data mining** is finding patterns in data using statistics and machine learning. Its basic tasks are:

- **Classification.** Predict a known category (spam or not spam) from examples that were labeled by hand. This is *supervised* learning.
- **Clustering and topic modeling.** Find groups in data with no labels. This is *unsupervised* learning.
- **Extraction.** Pull out specific pieces, such as names, dates, or key phrases.
- **Evaluation.** Measure how well the pattern holds on data the model has not seen.

NLP supplies the step that makes text usable (turning it into data), and data mining supplies the methods that find patterns once it is. In practice the two are used together.

---

## 1.4 The NLP Pipeline

Most NLP projects follow the same stages. The wording differs, but the order is nearly always this:

1. **Collect** the text.
2. **Clean** it: remove duplicates, empty rows, markup, and other noise.
3. **Preprocess** it: split into words (*tokens*), make words uniform (for example lowercase, or reduce to a base form), and remove very common words.
4. **Represent** it as numbers: word counts, TF-IDF, or embeddings.
5. **Model** it: classify, cluster, find topics, extract entities, summarize, answer questions, or generate text.
6. **Evaluate** the result and read the outputs yourself.

The book follows this pipeline, and then shows where modern models change it:

| Chapter | Topic | Pipeline stage |
|---------|-------|----------------|
| 2 | Getting started with Orange | Tools |
| 3 | Working with text data | Collect, clean, preprocess, represent |
| 4 | Text classification | Model (supervised) |
| 5 | Clustering and topic modeling | Model (unsupervised) |
| 6 | Model evaluation and tuning | Evaluate |
| 7 | Sentiment analysis | Model (classification by dictionary and by learning) |
| 8 | Named entity recognition | Model (extraction) |
| 9 | Text summarization | Model (summarization) |
| 10 | Parts of speech and dependency parsing | Preprocess (structure of sentences) |
| 11, 12 | Word and document embeddings | Represent (modern) |
| 13 | Question answering and text generation | Model (generative) |
| 14 | Using a large language model | Model (one model, many tasks) |
| 15 | Retrieval-augmented generation | Model, with your own documents |
| 16 | Capstone project | The whole pipeline, with a fair comparison |

---

## 1.5 Why Orange?

**Orange** is a free, open-source tool for data mining. You build an analysis by placing **widgets** on a canvas and connecting them with lines, so the whole pipeline is visible at a glance. This suits a lab book:

- You see every step, and what flows between steps.
- You change one setting and watch the result change.
- A saved workflow (an `.ows` file) can be shared and rerun, so another person can repeat your result.
- Add-ons supply text widgets (*Orange3-Text*) and the newer embedding, question answering, and LLM widgets (*orange3-nlp*). You install them in Chapter 2 and later.

Orange is not a toy. It can also be scripted in Python when you need more control.

> 💡 A workflow you build by dragging is also a record of what you did. Always save it, and name it in a way you will recognize later.

---

## 1.6 How to Use This Book

- **Read, then do.** Each chapter explains the idea, lists the widgets, and then gives lab exercises (A, B, C) that you do in Orange.
- **Predict first.** Before you run a step, guess what you will see. A wrong guess teaches more than a right one.
- **Look at the data.** After every step, open a *Data Table* and look at actual rows. Many mistakes show up there.
- **Expect some differences.** Orange and its add-ons change between versions, and language models give different wording each time. Your screen may not match the figures exactly. The questions are written so that you can still answer them.
- **Datasets and workflows.** The datasets used are in the `datasets` folder of the book's repository, and example workflows are in `workflows`. Try your own build first.
- **Be skeptical.** A model's output is a result to check, not a fact to accept. The last four chapters return to this.

---

## 1.7 Case Study Preview

A company has thousands of customer reviews and wants to know which are positive and which are negative. Reading them all is not possible. The pipeline looks like this:

- Collect and clean the reviews (Chapter 3).
- Convert each review into numbers (Chapters 3 and 11).
- Train a classifier on reviews that were labeled by hand (Chapter 4), and measure how well it does on reviews it has not seen (Chapter 6).
- Compare it with a dictionary method and with an LLM (Chapters 7 and 14).

Chapter 7 carries out this plan on 2,000 movie reviews.

---

## Lab Exercise 1A: Your First Look at Orange

**Goal**: Practice the loop of loading a table, looking at it, and plotting it. The data here is numeric, so you can see how a structured dataset looks before text enters.

**Steps**:

1. Install Orange from [orangedatamining.com](https://orangedatamining.com/download/) and open it. (Chapter 2 covers installing the text add-ons.)
2. Create a new workflow. Add a *Datasets* widget (Data toolbox) and choose the **iris** dataset. *Datasets* downloads its list from the internet, so you need a connection.
3. Add a *Data Table* and connect *Datasets* to it. Open it and look at the rows and columns.
4. Add a *Scatter Plot* (Visualize toolbox) and connect *Datasets* to it.
5. In the scatter plot, color the points by **iris**. Try different pairs of features on the x and y axes and watch how the colors mix.
6. Find the pair of features that separates the three species best. The **Find Informative Projections** button in the plot's left panel ranks the pairs if you want a hint.
7. Save the plot as `ex1.png` (the save button at the bottom left of the plot window) and save your workflow as `ex1.ows`.

![Figure 1. A first workflow: Datasets sends iris to a Data Table and a Scatter Plot](Ex1%20First%20Look.png)

![Figure 2. Sepal width against sepal length, with a confidence ellipse for each species: the ellipses overlap, so these two features do not separate the species cleanly](Ex1%20Scatter%20Plot.png)

The dataset is Edgar Anderson's 1936 measurements of three iris species: *setosa*, *versicolor*, and *virginica*. Figure 2 is a *poor* choice of axes, because the *versicolor* and *virginica* ellipses overlap heavily.

**Questions**:

- How many rows and columns does the table have? Which column is the label, and which are the features?
- Which two features separated the species best? Which species was always easy to pick out, and which two were hard to tell apart?
- If a new flower has sepal width 3.0 and sepal length 5.0, which species would you guess from Figure 2? How sure are you?
- What does a scatter plot tell you that the table does not? What does the table tell you that the plot does not?

---

## Lab Exercise 1B: Language Is Hard (No Computer)

**Goal**: See why turning text into numbers is a design choice, and that each choice loses something.

**Steps**:

1. For each pair of sentences, write down what is different in meaning:
   - "The doctor asked the nurse to leave her notes."
   - "The doctor asked the nurse to leave their notes."
   - "I saw the man with the telescope."
   - "I didn't say she stole it."  (Say it aloud and stress a different word each time.)
2. Take these three reviews:
   - `The food was great but the service was terrible.`
   - `The service was great but the food was terrible.`
   - `Great food, great service!`
3. Make a table with one row per review and one column per distinct word. Fill each cell with how many times the word appears in the review.

**Questions**:

- Which reviews does your table make look most alike? Do they mean the same thing?
- What did you lose when you replaced a sentence with word counts? What would you need to keep it?
- Name one thing a computer could do easily with your table, and one thing that would still be hard.

> 📝 **Reflection:** You will meet this problem again in Chapter 3 (counting words) and in Chapter 11 (embeddings, which try to keep more of the meaning). As you read, ask each time: what does this method keep, and what does it throw away?

---

## Comprehension Questions

1. Define Natural Language Processing in your own words, and give three applications you used this week.
2. Give two reasons human language is harder for a computer than a table of measurements.
3. What does it mean to turn unstructured text into structured data? Why is that useful?
4. What is the difference between supervised and unsupervised learning? Give an example of each from the chapter.
5. List the stages of an NLP pipeline and say what happens in each.
6. What are two advantages of building an analysis as a visual workflow?

---

## Key Terms

- Natural Language Processing (NLP)
- Structured and unstructured data
- Data mining
- Supervised and unsupervised learning
- Token
- Feature
- Pipeline
- Workflow and widget (Orange)

---

## Notes

- Save your workflow as `ex1.ows`.
- Chapter 2 installs the text add-ons and tours the Orange interface. Chapter 3 turns real text into a table.
