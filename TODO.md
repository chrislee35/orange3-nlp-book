# TODO List

While there are obvious todo items such as finishing the writing, exercise designs, and editing.  There are some less obvious, easy to forget TODO items that I need to track.  That's what I'll focus on here.

## Obvious

* Finish writing the book
* Design the exercises
* Playtest the exercises
* Edit for grammar
* Translate into target languages (TBD)

## Less obvious

* Include a chapter or addendum on installing Ollama (cover Linux, Windows, and Mac)
  * I'll need someone from the community to help with Mac.
* Figure out the processor and disk size requirements to do everything in this book.
  * I think I can approximate this quite well, but I'll do it at the end since I'd have to reset everything.
* Figure out the licensing of the News Headlines dataset used in Chapter 3.
  * Kaggle says Unknown.  That's not sufficient.
  * http://groups.di.unipi.it/~gulli/AG_corpus_of_news_articles.html says:
```
You are encouraged to download this corpus for any non-commercial use. If you download the dataset, please drop me a mail to describe the academic research you are doing: gulli AT di.unipi.it.
If you use the corpus, you are requested to cite this web page in your academic publication
You are not authorized to change the corpus or to re-distribute (part of) it with a different name. 
```
  * I will email the author and ask for guidance.
* Create an interesting corpus for the question and answer exercise and the RAG exercise.
* Scour Biolab's Introduction to Data Science book (orange-lecture-notes) for additional NLP tasks that I should include in the book.
  * Remember that this book is more on practical application than theory. 
  * While exercises are great way to reenforce theory taught in class, the scope quickly becomes outside my ability to write.
  * I will probably add a lot more to text classification, chapter 4, as I have found that to be powerful in a lot of the work I've done, especially with cheap techniques like word2vec and multinomial native bayes or random forest for high-speed processing of messages.
* Make a CSS for the PDF version of the book.  
  * I tried using nlp-book.css, but it looked quite ugly.  I'd like to tweak the format of the PDF a little, but not as much as the web version of the CSS does.

