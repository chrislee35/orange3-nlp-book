# Chapter 10: Dependency Parsing and Part-of-Speech Tagging

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand what part-of-speech tagging and dependency parsing are.
- Use Orange widgets to tag and visualize syntactic structures.
- Interpret POS tags and dependency trees for sentence-level analysis.
- Apply these structures in downstream NLP tasks like named entity recognition or question answering.

---

## 10.1 What is Part-of-Speech Tagging?

Part-of-speech (POS) tagging assigns grammatical categories to each word in a sentence.

### Common POS Tags

| Tag | Meaning       | Example        |
|-----|---------------|----------------|
| NN  | Noun          | `cat`, `city`  |
| VB  | Verb          | `run`, `is`    |
| JJ  | Adjective     | `fast`, `red`  |
| RB  | Adverb        | `quickly`      |
| DT  | Determiner    | `the`, `an`    |
| IN  | Preposition   | `on`, `with`   |

> POS tagging is essential for syntactic parsing and downstream NLP tasks.

---

## 10.2 What is Dependency Parsing?

**Dependency parsing** identifies grammatical relationships between words.

- Each word is connected to a "head" in a tree structure.
- Arcs indicate relations like subject, object, or modifier.

> Example:
> `The dog chased the cat.`
> - `chased` is the root
> - `dog` is the subject of `chased`
> - `cat` is the object of `chased`

---

## 10.3 Using Orange for POS and Parsing

Assuming your custom widgets are available in `orange3-nlp`:

### Key Widgets

- **POS Tagger**: Annotates each token with its POS tag.
- **POS Viewer**: Visualizes POS tags and tree structures for selected sentences (similar to `spacy.displacy.render`).

### Typical Workflow

1. *File* + *Corpus* → Load data (e.g., `movie-lines.csv`)
2. *Preprocess Text* (tokenization and normalization)
3. Apply *POS Tagger* and *Dependency Parser*
4. Use *Parse Viewer* to explore sentence structure
5. (Optional) Connect to *Data Table* or *Corpus Viewer* for exploration

> 🧠 Useful for filtering texts by grammatical patterns, or for extracting structured phrases.

![Figure X. Part of Speech Viewer with parsed Slovenian text.](3c%20POS%20Viewer.png)

---

## 10.4 Applications of Parsing and Tagging

- **Named Entity Recognition**: Using noun chunks and modifiers to enhance entity detection.
- **Question Answering**: Identifying subjects, verbs, and objects for context extraction.
- **Search and Retrieval**: Enabling syntactic-aware search (e.g., "verbs of movement").

---

## Lab Exercise 10A: Visualize Sentence Structures

**Goal**: Explore syntactic structures in natural sentences.

**Steps**:

1. Load a conversational or literary dataset (e.g., `movie-lines.csv`).
2. Preprocess and apply *POS Tagger* and *Dependency Parser*.
3. Use *POS/Parse Viewer* to examine sentences:
   - Select multiple examples to view tree structures.
   - Highlight parts of speech for different sentence types.

**Reflection**:
- What is the root of each sentence?
- Are there passive constructions or complex clauses?

---

## Lab Exercise 10B: Extract Subject-Verb-Object Triples

**Goal**: Identify key SVO patterns from parsed text.

**Steps**:

1. Use the same parsed corpus from 10A.
2. In the *POS/Parse Viewer*, identify the dependencies labeled:
   - `nsubj` (nominal subject)
   - `ROOT` or `VERB`
   - `dobj` (direct object)
3. Record several SVO triples by hand and interpret their meaning in context.

**Discussion**:
- How often does the parser produce clean SVO structures?
- What sentence types make parsing more difficult?

---

## Comprehension Questions

1. What is the difference between POS tagging and dependency parsing?
2. What does the "ROOT" label represent in a dependency tree?
3. How can dependency parsing support information extraction?
4. In your own words, describe a case where parsing is better than using a bag-of-words model.
5. What challenges might arise when parsing informal text like tweets or movie dialogue?

---

## Key Terms

- Part-of-Speech (POS) Tagging
- Dependency Parsing
- Parse Tree
- Syntactic Relations
- Tokenization
- Grammatical Subject/Object
- Head/Dependent
- spaCy

---

## Notes

- Save your workflow as `dependency-parsing.ows`.
- These syntactic tools will serve as a foundation for more advanced text extraction and knowledge graph construction in later chapters.

---

