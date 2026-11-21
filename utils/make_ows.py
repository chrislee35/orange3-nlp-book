#!/usr/bin/env python
"""Generate an Orange .ows workflow from a small Python description.

Usage:  python utils/make_ows.py   (writes workflows/word-embeddings.ows)

Run with the conda env that has Orange installed.  Node settings are written
as pickled dicts (format="pickle"), the same way Orange saves them.  Anything
not set here (e.g. which column is the text feature, t-SNE color/label) falls
back to widget defaults and must be set in the GUI.
"""
import base64
import pickle
from pathlib import Path
from xml.sax.saxutils import quoteattr

BOOK = Path(__file__).resolve().parent.parent

# qualified names + (output channel name, id) / (input channel name, id)
WIDGETS = {
    "Corpus": ("orangecontrib.text.widgets.owcorpus.OWCorpus", "Orange3-Text"),
    "SBERT Embedder": ("orangecontrib.nlp.widgets.owmodel_sbert.OWSBERTEmbedder", "orange3-nlp"),
    "Text Embedder": ("orangecontrib.nlp.widgets.owtext_embedder.OWTextEmbedder", "orange3-nlp"),
    "t-SNE": ("Orange.widgets.unsupervised.owtsne.OWtSNE", "Orange3"),
    "Distances": ("Orange.widgets.unsupervised.owdistances.OWDistances", "Orange3"),
    "Hierarchical Clustering": ("Orange.widgets.unsupervised.owhierarchicalclustering.OWHierarchicalClustering", "Orange3"),
    "Datasets": ("Orange.widgets.data.owdatasets.OWDataSets", "Orange3"),
    "Data Table": ("Orange.widgets.data.owtable.OWTable", "Orange3"),
    "Neighbors": ("Orange.widgets.data.owneighbors.OWNeighbors", "Orange3"),
    "Corpus Viewer": ("orangecontrib.text.widgets.owcorpusviewer.OWCorpusViewer", "Orange3-Text"),
    "Question Answering": ("orangecontrib.nlp.widgets.owquestion_answer.OWQuestionAnswer", "orange3-nlp"),
    "Text Generator": ("orangecontrib.nlp.widgets.owtext_generator.OWTextGenerator", "orange3-nlp"),
    "Ollama Sentiment Analyzer": ("orangecontrib.ollama.widgets.owollama_sentiment_analyzer.OWOllamaSentimentAnalyzer", "orange3-ollama"),
    "Ollama Text Classification": ("orangecontrib.ollama.widgets.owollama_text_classifier.OWOllamaTextClassifier", "orange3-ollama"),
    "Ollama Summarizer": ("orangecontrib.ollama.widgets.owollama_summarizer.OWOllamaSummarizer", "orange3-ollama"),
    "Sentiment Analysis": ("orangecontrib.text.widgets.owsentimentanalysis.OWSentimentAnalysis", "Orange3-Text"),
    "Text Chunker": ("orangecontrib.nlp.widgets.owtext_chunker.OWTextChunker", "orange3-nlp"),
    "Reference Library": ("orangecontrib.nlp.widgets.owreference_library.OWReferenceLibrary", "orange3-nlp"),
    "Ollama RAG": ("orangecontrib.nlp.widgets.owollama_rag.OWOllamaRAG", "orange3-nlp"),
    "Preprocess Text": ("orangecontrib.text.widgets.owpreprocess.OWPreprocess", "Orange3-Text"),
    "Word Cloud": ("orangecontrib.text.widgets.owwordcloud.OWWordCloud", "Orange3-Text"),
    "Select Rows": ("Orange.widgets.data.owselectrows.OWSelectRows", "Orange3"),
    "Feature Statistics": ("Orange.widgets.data.owfeaturestatistics.OWFeatureStatistics", "Orange3"),
    "Bag of Words": ("orangecontrib.text.widgets.owbagofwords.OWTBagOfWords", "Orange3-Text"),
    "Constant": ("Orange.widgets.model.owconstant.OWConstant", "Orange3"),
    "Naive Bayes": ("Orange.widgets.model.ownaivebayes.OWNaiveBayes", "Orange3"),
    "Logistic Regression": ("Orange.widgets.model.owlogisticregression.OWLogisticRegression", "Orange3"),
    "Random Forest": ("Orange.widgets.model.owrandomforest.OWRandomForest", "Orange3"),
    "Test and Score": ("Orange.widgets.evaluate.owtestandscore.OWTestAndScore", "Orange3"),
    "Confusion Matrix": ("Orange.widgets.evaluate.owconfusionmatrix.OWConfusionMatrix", "Orange3"),
    "k-Means": ("Orange.widgets.unsupervised.owkmeans.OWKMeans", "Orange3"),
    "MDS": ("Orange.widgets.unsupervised.owmds.OWMDS", "Orange3"),
    "Topic Modelling": ("orangecontrib.text.widgets.owtopicmodeling.OWTopicModeling", "Orange3-Text"),
    "Box Plot": ("Orange.widgets.visualize.owboxplot.OWBoxPlot", "Orange3"),
    "Data Sampler": ("Orange.widgets.data.owdatasampler.OWDataSampler", "Orange3"),
    "ROC Analysis": ("Orange.widgets.evaluate.owrocanalysis.OWROCAnalysis", "Orange3"),
    "Parameter Fitter": ("Orange.widgets.evaluate.owparameterfitter.OWParameterFitter", "Orange3"),
    "Named Entity Recognition": ("orangecontrib.nlp.widgets.owner.OWNERWidget", "orange3-nlp"),
    "Extractive Summary": ("orangecontrib.nlp.widgets.owextractive_summary.OWExtractiveSummary", "orange3-nlp"),
    "Abstractive Summary": ("orangecontrib.nlp.widgets.owabstractive_summary.OWAbstractiveSummary", "orange3-nlp"),
    "Group by": ("Orange.widgets.data.owgroupby.OWGroupBy", "Orange3"),
    "POS Tagger": ("orangecontrib.nlp.widgets.owpos_tagger.OWPOSTagger", "orange3-nlp"),
    "POS Viewer": ("orangecontrib.nlp.widgets.owpos_viewer.OWPOSViewer", "orange3-nlp"),
    "Rule-based Entity-Relationship Extraction": ("orangecontrib.nlp.widgets.owrule_based_entity_relationship_extraction.OWRuleBasedEntityRelationshipExtraction", "orange3-nlp"),
    "Python Script": ("Orange.widgets.data.owpythonscript.OWPythonScript", "Orange3"),
    "Distance Matrix": ("Orange.widgets.unsupervised.owdistancematrix.OWDistanceMatrix", "Orange3"),
}
# (source name, source id) -> (sink name, sink id) keyed by (source widget, sink widget)
LINKS = {
    ("Corpus", "Text Embedder"): (("Corpus", "corpus"), ("Corpus", "data")),
    ("SBERT Embedder", "Text Embedder"): (("Embedder", "embedder"), ("Embedder", "embedder")),
    ("Datasets", "Corpus"): (("Data", "data"), ("Data", "data")),
    ("Text Embedder", "Neighbors"): (("Embedded Corpus", "data"), ("Data", "data")),
    ("Text Embedder", "Data Table"): (("Embedded Corpus", "data"), ("Data", "data")),
    ("Data Table", "Neighbors"): (("Selected Data", "selected_data"), ("Reference", "reference")),
    ("Neighbors", "Corpus Viewer"): (("Neighbors", "data"), ("Corpus", "corpus")),
    ("Corpus", "Question Answering"): (("Corpus", "corpus"), ("Corpus", "data")),
    ("Corpus", "Text Generator"): (("Corpus", "corpus"), ("Corpus", "data")),
    ("Question Answering", "Corpus Viewer"): (("Corpus", "data"), ("Corpus", "corpus")),
    ("Text Generator", "Corpus Viewer"): (("Corpus", "data"), ("Corpus", "corpus")),
    ("Text Generator", "Data Table"): (("Corpus", "data"), ("Data", "data")),
    ("Question Answering", "Data Table"): (("Corpus", "data"), ("Data", "data")),
    ("Corpus", "Ollama Sentiment Analyzer"): (("Corpus", "corpus"), ("Corpus", "in_corpus")),
    ("Ollama Sentiment Analyzer", "Ollama Text Classification"): (("Sentiment Corpus", "out_table"), ("Corpus", "in_corpus")),
    ("Ollama Text Classification", "Ollama Summarizer"): (("Labeled Corpus", "out_table"), ("Corpus", "in_corpus")),
    ("Ollama Summarizer", "Data Table"): (("Summarized Corpus", "out_table"), ("Data", "data")),
    ("Corpus", "Sentiment Analysis"): (("Corpus", "corpus"), ("Corpus", "corpus")),
    ("Sentiment Analysis", "Data Table"): (("Corpus", "corpus"), ("Data", "data")),
    ("Corpus", "Text Chunker"): (("Corpus", "corpus"), ("Corpus", "data")),
    ("Text Chunker", "Text Embedder"): (("Chunked Corpus", "data"), ("Corpus", "data")),
    ("Text Embedder", "Reference Library"): (("Embedded Corpus", "data"), ("Corpus", "data")),
    ("SBERT Embedder", "Reference Library"): (("Embedder", "embedder"), ("Embedder", "embedder")),
    ("Reference Library", "Ollama RAG"): (("Excerpts", "data"), ("Corpus", "data")),
    ("Reference Library", "Data Table"): (("Excerpts", "data"), ("Data", "data")),
    ("Ollama RAG", "Data Table"): (("Corpus", "data"), ("Data", "data")),
    ("Text Embedder", "t-SNE"): (("Embedded Corpus", "data"), ("Data", "data")),
    ("Text Embedder", "Distances"): (("Embedded Corpus", "data"), ("Data", "data")),
    ("Distances", "Hierarchical Clustering"): (("Distances", "distances"), ("Distances", "distances")),
    ("Distances", "Distance Matrix"): (("Distances", "distances"), ("Distances", "distances")),
    ("Corpus", "Corpus Viewer"): (("Corpus", "corpus"), ("Corpus", "corpus")),
    ("Corpus", "Word Cloud"): (("Corpus", "corpus"), ("Corpus", "corpus")),
    ("Corpus", "Data Table"): (("Corpus", "corpus"), ("Data", "data")),
    ("Corpus", "Preprocess Text"): (("Corpus", "corpus"), ("Corpus", "corpus")),
    ("Corpus", "Feature Statistics"): (("Corpus", "corpus"), ("Data", "data")),
    ("Preprocess Text", "Word Cloud"): (("Corpus", "corpus"), ("Corpus", "corpus")),
    ("Preprocess Text", "Corpus Viewer"): (("Corpus", "corpus"), ("Corpus", "corpus")),
    ("Preprocess Text", "Select Rows"): (("Corpus", "corpus"), ("Data", "data")),
    ("Select Rows", "Word Cloud"): (("Matching Data", "matching_data"), ("Corpus", "corpus")),
    ("Word Cloud", "Data Table"): (("Word Counts", "word_counts"), ("Data", "data")),
}
LEARNER = (("Learner", "learner"), ("Learner", "learner"))
LINKS.update({
    ("Preprocess Text", "Bag of Words"): (("Corpus", "corpus"), ("Corpus", "corpus")),
    ("Bag of Words", "Test and Score"): (("Corpus", "corpus"), ("Data", "train_data")),
    ("Constant", "Test and Score"): LEARNER,
    ("Naive Bayes", "Test and Score"): LEARNER,
    ("Logistic Regression", "Test and Score"): LEARNER,
    ("Random Forest", "Test and Score"): LEARNER,
    ("Test and Score", "Confusion Matrix"): (("Evaluation Results", "evaluation_results"),
                                             ("Evaluation Results", "evaluation_results")),
    ("Confusion Matrix", "Corpus Viewer"): (("Selected Data", "selected_data"), ("Corpus", "corpus")),
})
LINKS.update({
    ("Bag of Words", "Distances"): (("Corpus", "corpus"), ("Data", "data")),
    ("Bag of Words", "k-Means"): (("Corpus", "corpus"), ("Data", "data")),
    ("k-Means", "MDS"): (("Data", "annotated_data"), ("Data", "data")),
    ("k-Means", "Data Table"): (("Data", "annotated_data"), ("Data", "data")),
    ("Preprocess Text", "Topic Modelling"): (("Corpus", "corpus"), ("Corpus", "corpus")),
    ("Topic Modelling", "Box Plot"): (("Corpus", "corpus"), ("Data", "data")),
    ("Topic Modelling", "Word Cloud"): (("Selected Topic", "selected_topic"), ("Topic", "topic")),
    ("Topic Modelling", "Data Table"): (("Corpus", "corpus"), ("Data", "data")),
})
LINKS.update({
    ("Test and Score", "ROC Analysis"): (("Evaluation Results", "evaluation_results"),
                                         ("Evaluation Results", "evaluation_results")),
    ("Bag of Words", "Parameter Fitter"): (("Corpus", "corpus"), ("Data", "data")),
    ("Random Forest", "Parameter Fitter"): (("Learner", "learner"), ("Learner", "learner")),
    ("Bag of Words", "Data Sampler"): (("Corpus", "corpus"), ("Data", "data")),
    ("Sentiment Analysis", "Box Plot"): (("Corpus", "corpus"), ("Data", "data")),
    ("Sentiment Analysis", "Test and Score"): (("Corpus", "corpus"), ("Data", "train_data")),
    ("Data Sampler", "Test and Score"): (("Data Sample", "data_sample"), ("Data", "train_data")),
})
LINKS.update({
    ("Corpus", "Named Entity Recognition"): (("Corpus", "corpus"), ("Corpus", "data")),
    ("Preprocess Text", "Named Entity Recognition"): (("Corpus", "corpus"), ("Corpus", "data")),
    ("Named Entity Recognition", "Data Table"): (("Corpus with Entities", "data"), ("Data", "data")),
    ("Named Entity Recognition", "Select Rows"): (("Corpus with Entities", "data"), ("Data", "data")),
    ("Named Entity Recognition", "Corpus"): (("Corpus with Entities", "data"), ("Data", "data")),
    ("Select Rows", "Data Table"): (("Matching Data", "matching_data"), ("Data", "data")),
})
LINKS.update({
    ("Corpus", "Data Sampler"): (("Corpus", "corpus"), ("Data", "data")),
    ("Corpus", "Select Rows"): (("Corpus", "corpus"), ("Data", "data")),
    ("Corpus", "Extractive Summary"): (("Corpus", "corpus"), ("Corpus", "data")),
    ("Corpus", "Abstractive Summary"): (("Corpus", "corpus"), ("Corpus", "data")),
    ("Data Sampler", "Extractive Summary"): (("Data Sample", "data_sample"), ("Corpus", "data")),
    ("Data Sampler", "Abstractive Summary"): (("Data Sample", "data_sample"), ("Corpus", "data")),
    ("Select Rows", "Extractive Summary"): (("Matching Data", "matching_data"), ("Corpus", "data")),
    ("Select Rows", "Abstractive Summary"): (("Matching Data", "matching_data"), ("Corpus", "data")),
    ("Select Rows", "Group by"): (("Matching Data", "matching_data"), ("Data", "data")),
    ("Extractive Summary", "Group by"): (("Corpus with Summaries", "data"), ("Data", "data")),
    ("Extractive Summary", "Corpus"): (("Corpus with Summaries", "data"), ("Data", "data")),
    ("Extractive Summary", "Corpus Viewer"): (("Corpus with Summaries", "data"), ("Corpus", "corpus")),
    ("Abstractive Summary", "Corpus Viewer"): (("Corpus with Summaries", "data"), ("Corpus", "corpus")),
    ("Group by", "Corpus"): (("Data", "data"), ("Data", "data")),
})
LINKS.update({
    ("Corpus", "POS Tagger"): (("Corpus", "corpus"), ("Corpus", "data")),
    ("POS Tagger", "POS Viewer"): (("Tagged Corpus", "data"), ("Tagged Corpus", "data")),
    ("POS Tagger", "Python Script"): (("Tagged Corpus", "data"), ("Data", "data")),
    ("Python Script", "Data Table"): (("Data", "data"), ("Data", "data")),
    ("Corpus", "Rule-based Entity-Relationship Extraction"): (("Corpus", "corpus"), ("Corpus", "corpus")),
    ("Rule-based Entity-Relationship Extraction", "Data Table"): (("Relations", "relations"), ("Data", "data")),
})
COSINE, ROWS = 4, 0  # Orange.widgets.unsupervised.owdistances


def build(nodes, links, annotations=()):
    """nodes: [(key, widget, title, (x, y), settings dict)], links: [(key, key)]."""
    ids = {k: i for i, (k, *_) in enumerate(nodes)}
    kind = {k: w for k, w, *_ in nodes}
    out = ["<?xml version='1.0' encoding='utf-8'?>",
           '<scheme version="2.0" title="" description="">', "\t<nodes>"]
    for k, w, title, (x, y), _ in nodes:
        q, proj = WIDGETS[w]
        out.append(f'\t\t<node id="{ids[k]}" name="{w}" qualified_name="{q}" project_name="{proj}" '
                   f'version="" title={quoteattr(title)} position="({x}, {y})" />')
    out += ["\t</nodes>", "\t<links>"]
    for i, (a, b) in enumerate(links):
        (sn, sid), (kn, kid) = LINKS[(kind[a], kind[b])]
        out.append(f'\t\t<link id="{i}" source_node_id="{ids[a]}" sink_node_id="{ids[b]}" '
                   f'source_channel="{sn}" sink_channel="{kn}" enabled="true" '
                   f'source_channel_id="{sid}" sink_channel_id="{kid}" />')
    out += ["\t</links>", "\t<annotations>"]
    for i, (text, rect) in enumerate(annotations):
        out.append(f'\t\t<text id="{i}" type="text/markdown" rect="{rect}" '
                   f'font-family="Sans Serif" font-size="16">{text}</text>')
    out += ["\t</annotations>", "\t<thumbnail />", "\t<node_properties>"]
    for k, _, _, _, settings in nodes:
        if settings:
            blob = base64.b64encode(pickle.dumps(settings, protocol=4)).decode()
            out.append(f'\t\t<properties node_id="{ids[k]}" format="pickle">{blob}</properties>')
    out += ["\t</node_properties>", "</scheme>", ""]
    return "\n".join(out)


def corpus(key, fname, title, y):
    path = str(BOOK / "datasets" / fname)
    return (key, "Corpus", title, (100, y),
            {"controlAreaVisible": True, "recent_files": [path], "__version__": 2})


def distances(key, y):
    return (key, "Distances", "Distances " + key[-1].upper() + " (cosine)", (550, y),
            {"axis": ROWS, "metric_id": COSINE, "autocommit": True,
             "controlAreaVisible": True, "__version__": 4})


def word_embeddings():
    nodes = [("sbert", "SBERT Embedder", "SBERT Embedder", (100, 300), {})]
    links = []
    rows = [("a", "food-and-country.tab", "11A food-and-country", 0),
            ("b", "word-categories.tab", "11B word-categories", 150),
            ("c", "similar-and-opposite.tab", "11C similar-and-opposite", 450),
            ("d", "bank-senses.tab", "11D bank-senses", 600)]
    # layout: 11A, 11B above the shared SBERT node, 11C, 11D below it
    for key, fname, title, y in rows:
        nodes.append(corpus("corpus" + key, fname, title, y))
        nodes.append(("emb" + key, "Text Embedder", "Text Embedder " + key.upper(), (325, y), {}))
        links += [("corpus" + key, "emb" + key), ("sbert", "emb" + key)]
        if key in "ad":
            nodes.append(("tsne" + key, "t-SNE", "t-SNE " + key.upper(), (550, y), {}))
            links.append(("emb" + key, "tsne" + key))
    # 11B: t-SNE + Distances -> Hierarchical Clustering
    nodes.append(("tsneb", "t-SNE", "t-SNE B", (550, 100), {}))
    links.append(("embb", "tsneb"))
    nodes.append(distances("distb", 200))
    nodes.append(("hcb", "Hierarchical Clustering", "Hierarchical Clustering B", (775, 200), {}))
    links += [("embb", "distb"), ("distb", "hcb")]
    # 11C: Distances -> Distance Matrix
    nodes.append(distances("distc", 450))
    nodes.append(("dmc", "Distance Matrix", "Distance Matrix C", (775, 450), {}))
    links += [("embc", "distc"), ("distc", "dmc")]
    note = ("*Chapter 11. One shared **SBERT Embedder** feeds all four exercises. "
            "In each Corpus, check that the text feature is `Word` (11D: `Sentence`).*")
    return build(nodes, links, [(note, "(700.0, -10.0, 300.0, 110.0)")])


def document_embeddings():
    """Chapter 12: 12A/12B/12C on BBC3, 12D on movie reviews."""
    D = {"axis": ROWS, "metric_id": COSINE, "autocommit": True, "__version__": 4}
    nodes = [
        ("ds", "Datasets", "Datasets: BBC3", (100, 150),
         {"selected_id": "core/BBC3.tab", "controlAreaVisible": True}),
        ("sbert", "SBERT Embedder", "SBERT Embedder", (250, 300), {}),
        # 12A / 12C: Content
        ("corpus", "Corpus", "BBC3 Corpus (Content)", (250, 0), {}),
        ("emb", "Text Embedder", "Text Embedder (Content)", (400, 0), {}),
        ("tsne", "t-SNE", "t-SNE Content", (575, -75), {}),
        ("dist", "Distances", "Distances (cosine)", (575, 0), D),
        ("hc", "Hierarchical Clustering", "Hierarchical Clustering", (750, 0), {}),
        ("table", "Data Table", "Data Table (pick reference)", (575, 75), {}),
        ("nb", "Neighbors", "Neighbors (cosine, 5)", (750, 75),
         {"n_neighbors": 5, "limit_neighbors": True, "metric_id": COSINE,
          "include_reference": False, "auto_apply": True, "controlAreaVisible": True}),
        ("cv", "Corpus Viewer", "Corpus Viewer", (925, 75), {}),
        # 12B: Title
        ("corpust", "Corpus", "BBC3 Corpus (Title)", (250, 225), {}),
        ("embt", "Text Embedder", "Text Embedder (Title)", (400, 225), {}),
        ("tsnet", "t-SNE", "t-SNE Title", (575, 225), {}),
        # 12D: movie reviews
        corpus("mr", "movie-reviews.tab", "movie-reviews (Review)", 450),
        ("embm", "Text Embedder", "Text Embedder (Reviews)", (400, 450), {}),
        ("tsnem", "t-SNE", "t-SNE Reviews", (575, 450), {}),
        ("distm", "Distances", "Distances Reviews (cosine)", (575, 525), D),
        ("hcm", "Hierarchical Clustering", "Hierarchical Clustering Reviews", (750, 525), {}),
    ]
    links = [("ds", "corpus"), ("ds", "corpust"),
             ("corpus", "emb"), ("sbert", "emb"), ("emb", "tsne"),
             ("emb", "dist"), ("dist", "hc"),
             ("emb", "table"), ("emb", "nb"), ("table", "nb"), ("nb", "cv"),
             ("corpust", "embt"), ("sbert", "embt"), ("embt", "tsnet"),
             ("mr", "embm"), ("sbert", "embm"), ("embm", "tsnem"),
             ("embm", "distm"), ("distm", "hcm")]
    note = ("*Chapter 12. In each Corpus, set the text feature: `Content` (12A, 12C), `Title` (12B), "
            "`Review` (12D). Color t-SNE by `category` or `Sentiment`. 12C: select a row in the Data Table.*")
    return build(nodes, links, [(note, "(700.0, 300.0, 330.0, 120.0)")])


GROUNDED = (
    "Answer the question using only the passage. If the passage does not contain the answer, say so.\n\n"
    "Passage: {Passage}\n\nQuestion: Who discovered penicillin?\nAnswer:"
)


def question_answering():
    """Chapter 13: 13A extractive QA, 13B autocomplete with gpt2, 13C generative QA with phi4-mini."""
    nodes = [
        corpus("qa", "qa-passages.tab", "qa-passages (Passage)", 0),
        ("qa13a", "Question Answering", "Question Answering (13A)", (325, 0), {}),
        ("dt13a", "Data Table", "Data Table: answers (13A)", (550, 0), {}),
        ("gpt2", "Text Generator", "Text Generator: gpt2 (13B)", (325, 200),
         {"backend": "Hugging Face", "hf_model": "gpt2", "prompt": "NASA was established in", "temperature": 0.7,
          "max_new_tokens": 30, "samples": 3, "use_seed": True, "seed": 42, "controlAreaVisible": True}),
        ("dt13b", "Data Table", "Data Table: completions (13B)", (550, 200), {}),
        ("phi", "Text Generator", "Text Generator: phi4-mini (13C)", (325, 400),
         {"backend": "Ollama", "ollama_model": "phi4-mini:latest", "prompt": GROUNDED, "temperature": 0.0,
          "max_new_tokens": 60, "samples": 1, "use_seed": False, "controlAreaVisible": True}),
        ("dt13c", "Data Table", "Data Table: generated answers (13C)", (550, 400), {}),
    ]
    links = [("qa", "qa13a"), ("qa13a", "dt13a"), ("gpt2", "dt13b"), ("qa", "phi"), ("phi", "dt13c")]
    note = ("*Chapter 13. 13A: select a passage in Question Answering and ask a question (tick **All documents** to ask "
            "every passage). 13B: no input; change the prompt, temperature and samples. 13C: the question is written "
            "in the prompt template; edit it and press Generate.*")
    return build(nodes, links, [(note, "(700.0, 180.0, 330.0, 140.0)")])


REPLY = "Write a polite two-sentence reply from customer support to this message:\n\n{Message}"


def llm_tasks():
    """Chapter 14: 14A orange3-ollama widgets in series, 14B Text Generator, 14C classical sentiment for comparison."""
    ollama = {"selected_model": "phi4-mini:latest", "selected_column": "Message", "prompt_context": "", "controlAreaVisible": True}
    nodes = [
        corpus("msgs", "customer-messages.tab", "customer-messages (Message)", 200),
        ("sent", "Ollama Sentiment Analyzer", "Ollama Sentiment Analyzer (14A)", (325, 0), dict(ollama)),
        ("cls", "Ollama Text Classification", "Ollama Text Classification (14A)", (550, 0),
         {**ollama, "classification_labels": ["shipping", "billing", "product", "account"]}),
        ("summ", "Ollama Summarizer", "Ollama Summarizer (14A)", (775, 0), dict(ollama)),
        ("dta", "Data Table", "Data Table: LLM tasks (14A)", (1000, 0), {}),
        ("gen", "Text Generator", "Text Generator: reply drafts (14B)", (325, 200),
         {"backend": "Ollama", "ollama_model": "phi4-mini:latest", "prompt": REPLY, "temperature": 0.7, "max_new_tokens": 80,
          "samples": 3, "use_seed": True, "seed": 42, "controlAreaVisible": True}),
        ("dtb", "Data Table", "Data Table: replies (14B)", (550, 200), {}),
        ("vader", "Sentiment Analysis", "Sentiment Analysis: VADER (14C)", (325, 400), {}),
        ("dtc", "Data Table", "Data Table: VADER scores (14C)", (550, 400), {}),
    ]
    links = [("msgs", "sent"), ("sent", "cls"), ("cls", "summ"), ("summ", "dta"),
             ("msgs", "gen"), ("gen", "dtb"), ("msgs", "vader"), ("vader", "dtc")]
    note = ("*Chapter 14. Ollama must be running with phi4-mini pulled. 14A: the three Ollama widgets are chained, so "
            "each adds a column (Sentiment, Prediction, Summary); press Analyze Sentiment, then Classify Text, then Summarize Documents, waiting for each to finish. 14B: edit the "
            "prompt template and press Generate. 14C: choose the VADER method and compare with the true Tone column.*")
    return build(nodes, links, [(note, "(700.0, 300.0, 380.0, 150.0)")])


RAG_QUESTION = "How long do I have to return an item?"
RAG_PROMPT = "Using only the references, answer the question: " + RAG_QUESTION


def rag():
    """Chapter 15: 15A retrieval-augmented pipeline, 15B closed-book comparison, 15C inspect retrieval."""
    nodes = [
        corpus("kb", "harbor-policies.tab", "harbor-policies (Text)", 150),
        ("chunk", "Text Chunker", "Text Chunker (256, recursive)", (325, 150),
         {"chunk_size": 256, "chunk_strategy": "recursive", "controlAreaVisible": True}),
        ("sbert", "SBERT Embedder", "SBERT Embedder", (550, 300), {}),
        ("emb", "Text Embedder", "Text Embedder (chunks)", (550, 150), {}),
        ("lib", "Reference Library", "Reference Library (top 3)", (775, 150),
         {"max_excerpts": 3, "threshold": 0.0, "query": RAG_QUESTION, "controlAreaVisible": True}),
        ("dtx", "Data Table", "Data Table: retrieved excerpts (15C)", (1000, 50), {}),
        ("rag", "Ollama RAG", "Ollama RAG: phi4-mini (15A)", (1000, 250),
         {"host": "localhost", "port": 11434, "model": "phi4-mini:latest", "prompt": RAG_PROMPT,
          "controlAreaVisible": True}),
        ("dta", "Data Table", "Data Table: RAG answer (15A)", (1225, 250), {}),
        ("closed", "Text Generator", "Text Generator: no references (15B)", (775, 450),
         {"backend": "Ollama", "ollama_model": "phi4-mini:latest", "prompt": RAG_QUESTION, "temperature": 0.0,
          "max_new_tokens": 100, "samples": 1, "use_seed": False, "controlAreaVisible": True}),
        ("dtb", "Data Table", "Data Table: closed-book answer (15B)", (1000, 450), {}),
    ]
    links = [("kb", "chunk"), ("chunk", "emb"), ("sbert", "emb"), ("emb", "lib"), ("sbert", "lib"),
             ("lib", "dtx"), ("lib", "rag"), ("rag", "dta"), ("closed", "dtb")]
    note = ("*Chapter 15. In Corpus, make sure only `Text` is the text feature. The Reference Library has its own "
            "query box and the Ollama RAG has its own prompt: keep them about the same question. The same SBERT "
            "Embedder must feed both Text Embedder and Reference Library.*")
    return build(nodes, links, [(note, "(100.0, 330.0, 380.0, 130.0)")])


def cleaning_headlines():
    """Chapter 3: 3A load and inspect BBC3, 3B preprocess one stage at a time, 3C compare categories."""
    nodes = [
        ("ds", "Datasets", "Datasets: BBC3", (80, 200), {"selected_id": "BBC3.tab"}),
        ("c", "Corpus", "Corpus: Title only (3A)", (250, 200), {"controlAreaVisible": True}),
        ("cv", "Corpus Viewer", "Corpus Viewer (3A)", (450, 80), {}),
        ("fs", "Feature Statistics", "Feature Statistics (3A)", (450, 330), {}),
        ("pp", "Preprocess Text", "Preprocess Text (3B)", (450, 200), {}),
        ("cvt", "Corpus Viewer", "Corpus Viewer: tokens (3B)", (680, 80), {}),
        ("wc", "Word Cloud", "Word Cloud (3B)", (680, 200), {}),
        ("dt", "Data Table", "Data Table: word counts (3B)", (900, 200), {}),
        ("sb", "Select Rows", "Select Rows: business (3C)", (680, 340), {}),
        ("se", "Select Rows", "Select Rows: entertainment (3C)", (680, 440), {}),
        ("ss", "Select Rows", "Select Rows: sport (3C)", (680, 540), {}),
        ("wb", "Word Cloud", "Word Cloud: business (3C)", (900, 340), {}),
        ("we", "Word Cloud", "Word Cloud: entertainment (3C)", (900, 440), {}),
        ("wsp", "Word Cloud", "Word Cloud: sport (3C)", (900, 540), {}),
    ]
    links = [("ds", "c"), ("c", "cv"), ("c", "fs"), ("c", "pp"), ("pp", "cvt"), ("pp", "wc"), ("wc", "dt"),
             ("pp", "sb"), ("pp", "se"), ("pp", "ss"), ("sb", "wb"), ("se", "we"), ("ss", "wsp")]
    note = ("*Chapter 3. Corpus: move Content to Ignored so only Title is used. Preprocess Text starts with Lowercase "
            "and Stopwords on; change one stage at a time. Select Rows: set category to business, entertainment, "
            "sport. Datasets needs an internet connection.*")
    return build(nodes, links, [(note, "(80.0, 620.0, 760.0, 80.0)")])


def headline_classifier():
    """Chapter 4: classify BBC3 headlines; 4A compare learners, 4B change Bag of Words, 4C confusion matrix."""
    nodes = [
        ("ds", "Datasets", "Datasets: BBC3", (80, 220), {"selected_id": "BBC3.tab"}),
        ("c", "Corpus", "Corpus: Title only", (240, 220), {"controlAreaVisible": True}),
        ("pp", "Preprocess Text", "Preprocess Text", (400, 220), {}),
        ("bow", "Bag of Words", "Bag of Words (4B)", (560, 220), {}),
        ("ts", "Test and Score", "Test and Score (4A)", (780, 220), {}),
        ("const", "Constant", "Constant (baseline)", (560, 360), {}),
        ("nb", "Naive Bayes", "Naive Bayes", (560, 440), {}),
        ("lr", "Logistic Regression", "Logistic Regression", (560, 520), {}),
        ("rf", "Random Forest", "Random Forest", (560, 600), {}),
        ("cm", "Confusion Matrix", "Confusion Matrix (4C)", (960, 220), {}),
        ("cv", "Corpus Viewer", "Corpus Viewer: wrong headlines (4C)", (1150, 220), {}),
    ]
    links = [("ds", "c"), ("c", "pp"), ("pp", "bow"), ("bow", "ts"), ("const", "ts"), ("nb", "ts"),
             ("lr", "ts"), ("rf", "ts"), ("ts", "cm"), ("cm", "cv")]
    note = ("*Chapter 4. Corpus: move Content to Ignored so only Title is used. Test and Score: the data goes in "
            "the Data input, each learner in the Learner input; target class = category. Bag of Words starts with "
            "Count / (None) / (None); change it for 4B. Naive Bayes and Logistic Regression take about half a "
            "minute each. Confusion Matrix: select the Naive Bayes learner, then click a cell.*")
    return build(nodes, links, [(note, "(80.0, 330.0, 440.0, 190.0)")])


def clustering_books():
    """Chapter 5, 5A: cluster the book excerpts (hierarchical and k-Means)."""
    nodes = [
        ("c", "Corpus", "Corpus: book-excerpts", (80, 200),
         {"controlAreaVisible": True, "recent_files": ["book-excerpts.tab"], "__version__": 2}),
        ("pp", "Preprocess Text", "Preprocess Text", (250, 200), {}),
        ("bow", "Bag of Words", "Bag of Words (TF-IDF)", (420, 200),
         {"wlocal": "Count", "wglobal": "IDF", "normalization": "L2 (Euclidean)", "autocommit": True}),
        ("dist", "Distances", "Distances (cosine)", (620, 100),
         {"axis": ROWS, "metric_id": COSINE, "autocommit": True, "controlAreaVisible": True, "__version__": 4}),
        ("hc", "Hierarchical Clustering", "Hierarchical Clustering", (820, 100), {}),
        ("km", "k-Means", "k-Means", (620, 300), {}),
        ("mds", "MDS", "MDS", (820, 300), {}),
        ("dt", "Data Table", "Data Table: clusters", (820, 430), {}),
    ]
    links = [("c", "pp"), ("pp", "bow"), ("bow", "dist"), ("dist", "hc"), ("bow", "km"), ("km", "mds"), ("km", "dt")]
    note = ("*Chapter 5, 5A. Bag of Words: Count / IDF / L2 (TF-IDF). Hierarchical Clustering: set Color by to "
            "Category and drag the cut line. k-Means: try k = 2..5; color MDS by Cluster, then by Category.*")
    return build(nodes, links, [(note, "(80.0, 330.0, 460.0, 110.0)")])


def topics_news():
    """Chapter 5, 5B: LDA topics on BBC3 article content."""
    nodes = [
        ("ds", "Datasets", "Datasets: BBC3", (80, 200), {"selected_id": "BBC3.tab"}),
        ("c", "Corpus", "Corpus: Content only", (250, 200), {"controlAreaVisible": True}),
        ("pp", "Preprocess Text", "Preprocess Text", (420, 200), {}),
        ("lda", "Topic Modelling", "Topic Modelling (LDA)", (620, 200), {}),
        ("wc", "Word Cloud", "Word Cloud: selected topic", (840, 100), {}),
        ("bp", "Box Plot", "Box Plot: topic weight by category", (840, 200), {}),
        ("dt", "Data Table", "Data Table: topic weights", (840, 300), {}),
    ]
    links = [("ds", "c"), ("c", "pp"), ("pp", "lda"), ("lda", "wc"), ("lda", "bp"), ("lda", "dt")]
    note = ("*Chapter 5, 5B. Corpus: move Title to Ignored so only Content is used. Preprocess Text: Lowercase, "
            "Regexp, English stopwords, then add Numbers and Document frequency (relative 0.01 to 0.3). Topic "
            "Modelling: choose Latent Dirichlet Allocation and 3 topics.*")
    return build(nodes, links, [(note, "(80.0, 330.0, 460.0, 110.0)")])


def classifier_evaluation():
    """Chapter 6: 6A compare fairly, 6B tune (Parameter Fitter), 6C held-out test (Data Sampler)."""
    nodes = [
        ("ds", "Datasets", "Datasets: BBC3", (80, 240), {"selected_id": "BBC3.tab"}),
        ("c", "Corpus", "Corpus: Title only", (240, 240), {"controlAreaVisible": True}),
        ("pp", "Preprocess Text", "Preprocess Text", (400, 240), {}),
        ("bow", "Bag of Words", "Bag of Words", (560, 240), {}),
        ("ts", "Test and Score", "Test and Score (6A)", (860, 120), {}),
        ("const", "Constant", "Constant (baseline)", (700, 360), {}),
        ("nb", "Naive Bayes", "Naive Bayes", (700, 440), {}),
        ("lr", "Logistic Regression", "Logistic Regression (6B: C)", (700, 520), {}),
        ("rf", "Random Forest", "Random Forest (6B: trees, depth)", (700, 600), {}),
        ("roc", "ROC Analysis", "ROC Analysis (6A)", (1060, 60), {}),
        ("cm", "Confusion Matrix", "Confusion Matrix", (1060, 180), {}),
        ("pf", "Parameter Fitter", "Parameter Fitter: trees (6B)", (1000, 600), {}),
        ("sam", "Data Sampler", "Data Sampler: 80/20 (6C)", (700, 60), {}),
        ("ts2", "Test and Score", "Test and Score: held-out test (6C)", (1000, 340), {}),
    ]
    links = [("ds", "c"), ("c", "pp"), ("pp", "bow"), ("bow", "ts"), ("const", "ts"), ("nb", "ts"), ("lr", "ts"),
             ("rf", "ts"), ("ts", "roc"), ("ts", "cm"), ("bow", "pf"), ("rf", "pf"), ("bow", "sam"),
             ("sam", "ts2"), ("const", "ts2"), ("nb", "ts2"), ("lr", "ts2"), ("rf", "ts2")]
    note = ("*Chapter 6. Same headlines and Bag of Words as Chapter 4. 6A: change the method in Test and Score. "
            "6B: Parameter Fitter (number of trees); learner settings in Random Forest and Logistic Regression. "
            "6C: Data Sampler 80/20 (tick stratify). In the second Test and Score, Data Sampler's Data Sample is the "
            "training data; connect its Remaining Data to the Test Data input yourself, then choose Test on test data.*")
    return build(nodes, links, [(note, "(80.0, 330.0, 540.0, 190.0)")])


def sentiment_reviews():
    """Chapter 7: 7A lexicon scores on short sentences, 7B on movie reviews, 7C a trained model."""
    nodes = [
        corpus("sen", "sentiment-sentences.tab", "Corpus: sentiment-sentences (7A)", 80),
        ("va", "Sentiment Analysis", "Sentiment Analysis: VADER (7A)", (330, 20), {"method_idx": 1}),
        ("lha", "Sentiment Analysis", "Sentiment Analysis: Liu Hu (7A)", (330, 140), {"method_idx": 0}),
        ("dta", "Data Table", "Data Table: VADER (7A)", (560, 20), {}),
        ("dtl", "Data Table", "Data Table: Liu Hu (7A)", (560, 140), {}),
        corpus("rev", "movie-reviews.tab", "Corpus: movie-reviews (7B)", 400),
        ("vb", "Sentiment Analysis", "Sentiment Analysis: VADER (7B)", (330, 300), {"method_idx": 1}),
        ("lhb", "Sentiment Analysis", "Sentiment Analysis: Liu Hu (7B)", (330, 420), {"method_idx": 0}),
        ("bpv", "Box Plot", "Box Plot: compound by Sentiment (7B)", (560, 300), {}),
        ("bpl", "Box Plot", "Box Plot: Liu Hu score by Sentiment (7B)", (560, 420), {}),
        ("pp", "Preprocess Text", "Preprocess Text (7C)", (330, 560), {}),
        ("bow", "Bag of Words", "Bag of Words (7C)", (520, 560), {}),
        ("tsb", "Test and Score", "Test and Score: words (7C)", (760, 560), {}),
        ("tsv", "Test and Score", "Test and Score: VADER scores (7C)", (760, 360), {}),
        ("lr", "Logistic Regression", "Logistic Regression", (560, 660), {}),
        ("nb", "Naive Bayes", "Naive Bayes", (560, 740), {}),
    ]
    links = [("sen", "va"), ("sen", "lha"), ("va", "dta"), ("lha", "dtl"), ("rev", "vb"), ("rev", "lhb"),
             ("vb", "bpv"), ("lhb", "bpl"), ("rev", "pp"), ("pp", "bow"), ("bow", "tsb"), ("vb", "tsv"),
             ("lr", "tsb"), ("nb", "tsb"), ("lr", "tsv"), ("nb", "tsv")]
    note = ("*Chapter 7. 7A: compare the two Sentiment Analysis methods with the Label column. 7B: Box Plot, "
            "choose compound (or sentiment) as the variable and Sentiment for Group by. 7C: Preprocess Text with "
            "Lowercase, Regexp, English stopwords and a Document frequency filter (relative 0.01 to 1.0); Bag of "
            "Words with Count. Test and Score: Naive Bayes on the words takes a couple of minutes. Corpus: the text feature is Review (7B) "
            "and Sentence (7A). Sentiment Analysis does not use Preprocess Text: VADER reads the raw text.*")
    return build(nodes, links, [(note, "(820.0, 20.0, 400.0, 230.0)")])


def named_entities():
    """Chapter 8: 8A entities in BBC3 headlines, 8B compare backends, 8C effect of Preprocess Text."""
    ner = lambda fw: {"selected_framework": fw, "controlAreaVisible": True}
    nodes = [
        ("ds", "Datasets", "Datasets: BBC3", (80, 100), {"selected_id": "BBC3.tab"}),
        ("c", "Corpus", "Corpus: Title only", (240, 100), {"controlAreaVisible": True}),
        ("n1", "Named Entity Recognition", "Named Entity Recognition: spaCy (8A)", (440, 100), ner("spaCy")),
        ("d1", "Data Table", "Data Table: entities (8A)", (680, 20), {}),
        ("sel1", "Select Rows", "Select Rows: contains (GPE) (8A)", (680, 100), {}),
        ("d1s", "Data Table", "Data Table: headlines with a place (8A)", (900, 100), {}),
        ("c2", "Corpus", "Corpus: Named Entities (8A)", (680, 200), {"controlAreaVisible": True}),
        ("pp2", "Preprocess Text", "Preprocess Text: entities (8A)", (880, 200), {}),
        ("wc", "Word Cloud", "Word Cloud: most frequent entities (8A)", (1080, 200), {}),
        ("pp3", "Preprocess Text", "Preprocess Text: Lowercase (8C)", (440, 330), {}),
        ("n3", "Named Entity Recognition", "Named Entity Recognition: spaCy (8C)", (680, 330), ner("spaCy")),
        ("sel3", "Select Rows", "Select Rows: contains (GPE) (8C)", (900, 330), {}),
        ("d3", "Data Table", "Data Table: places after Lowercase (8C)", (1100, 330), {}),
        corpus("cs", "ner-sentences.tab", "Corpus: ner-sentences (8B)", 520),
        ("nsp", "Named Entity Recognition", "Named Entity Recognition: spaCy (8B)", (440, 450), ner("spaCy")),
        ("nnl", "Named Entity Recognition", "Named Entity Recognition: NLTK (8B)", (440, 540), ner("NLTK")),
        ("nfl", "Named Entity Recognition", "Named Entity Recognition: Flair (8B)", (440, 630), ner("Flair")),
        ("nol", "Named Entity Recognition", "Named Entity Recognition: Ollama (8B, not connected)", (440, 720),
         {**ner("Ollama"), "selected_model": "llama3.1:8b"}),
        ("dsp", "Data Table", "Data Table: spaCy (8B)", (680, 450), {}),
        ("dnl", "Data Table", "Data Table: NLTK (8B)", (680, 540), {}),
        ("dfl", "Data Table", "Data Table: Flair (8B)", (680, 630), {}),
        ("dol", "Data Table", "Data Table: Ollama (8B)", (680, 720), {}),
    ]
    links = [("ds", "c"), ("c", "n1"), ("n1", "d1"), ("n1", "sel1"), ("sel1", "d1s"), ("n1", "c2"), ("c2", "pp2"), ("pp2", "wc"),
             ("c", "pp3"), ("pp3", "n3"), ("n3", "sel3"), ("sel3", "d3"),
             ("cs", "nsp"), ("cs", "nnl"), ("cs", "nfl"), ("nsp", "dsp"), ("nnl", "dnl"), ("nfl", "dfl"), ("nol", "dol")]
    note = ("*Chapter 8. 8A: Corpus: move Content to Ignored so only Title is used. Select Rows: Named Entities contains "
            "(GPE). In the second Corpus, make Named Entities the only text feature; in Preprocess Text use only the Regexp "
            "tokenizer with the pattern [^,\\s][^,]\\* and untick Lowercase and Stopwords. 8B: Ollama needs a running server "
            "with llama3.1:8b pulled; connect ner-sentences to its NER widget yourself (it takes minutes). 8C: Preprocess Text "
            "with Lowercase ticked, compare with 8A, then untick Lowercase.*")
    return build(nodes, links, [(note, "(820.0, 450.0, 380.0, 260.0)")])


def summarization():
    """Chapter 9: 9A extractive, 9B abstractive, 9C a long text (Dracula chapter 1) in one pass and in stages."""
    ex = lambda fw: {"selected_framework": fw, "controlAreaVisible": True}
    nodes = [
        ("ds", "Datasets", "Datasets: BBC3", (80, 100), {"selected_id": "BBC3.tab"}),
        ("c", "Corpus", "Corpus: Content only", (240, 100), {"controlAreaVisible": True}),
        ("sam", "Data Sampler", "Data Sampler: 5 articles", (420, 100),
         {"sampling_type": 1, "sampleSizeNumber": 5, "use_seed": True, "replacement": False}),
        ("sumy", "Extractive Summary", "Extractive Summary: Sumy (9A)", (640, 0), ex("Sumy")),
        ("summa", "Extractive Summary", "Extractive Summary: Summa (9A)", (640, 80), ex("Summa")),
        ("bart", "Abstractive Summary", "Abstractive Summary: BART (9B)", (640, 160), ex("BART")),
        ("t5", "Abstractive Summary", "Abstractive Summary: T5 (9B)", (640, 240), ex("T5")),
        ("flan", "Abstractive Summary", "Abstractive Summary: FLAN-T5 (9B)", (640, 320), ex("FLAN-T5")),
        ("oll", "Abstractive Summary", "Abstractive Summary: Ollama (9B, not connected)", (640, 400),
         {**ex("Ollama"), "selected_model": "llama3.1:8b"}),
        ("v1", "Corpus Viewer", "Corpus Viewer: Sumy", (900, 0), {}),
        ("v2", "Corpus Viewer", "Corpus Viewer: Summa", (900, 80), {}),
        ("v3", "Corpus Viewer", "Corpus Viewer: BART", (900, 160), {}),
        ("v4", "Corpus Viewer", "Corpus Viewer: T5", (900, 240), {}),
        ("v5", "Corpus Viewer", "Corpus Viewer: FLAN-T5", (900, 320), {}),
        ("v6", "Corpus Viewer", "Corpus Viewer: Ollama", (900, 400), {}),
        corpus("dr", "dracula.tab", "Corpus: Dracula (9C)", 640),
        ("sel", "Select Rows", "Select Rows: Chapter is 1 (9C)", (300, 640), {}),
        ("g1", "Group by", "Group by Chapter: join paragraphs (9C)", (500, 580), {}),
        ("c1", "Corpus", "Corpus: whole chapter (9C)", (700, 580), {"controlAreaVisible": True}),
        ("a1", "Abstractive Summary", "Abstractive Summary: BART, one pass (9C)", (900, 580), ex("BART")),
        ("v7", "Corpus Viewer", "Corpus Viewer: one pass (9C)", (1120, 580), {}),
        ("e1", "Extractive Summary", "Extractive Summary: Summa per paragraph (9C)", (500, 700), ex("Summa")),
        ("g2", "Group by", "Group by Chapter: join summaries (9C)", (700, 700), {}),
        ("c2", "Corpus", "Corpus: joined summaries (9C)", (900, 700), {"controlAreaVisible": True}),
        ("e2", "Extractive Summary", "Extractive Summary: Summa on the chapter (9C)", (1100, 700), ex("Summa")),
        ("c3", "Corpus", "Corpus: second summary (9C)", (1300, 700), {"controlAreaVisible": True}),
        ("a2", "Abstractive Summary", "Abstractive Summary: BART, in stages (9C)", (1500, 700), ex("BART")),
        ("v8", "Corpus Viewer", "Corpus Viewer: in stages (9C)", (1700, 700), {}),
    ]
    links = [("ds", "c"), ("c", "sam"), ("sam", "sumy"), ("sam", "summa"), ("sam", "bart"), ("sam", "t5"), ("sam", "flan"),
             ("sumy", "v1"), ("summa", "v2"), ("bart", "v3"), ("t5", "v4"), ("flan", "v5"), ("oll", "v6"),
             ("dr", "sel"), ("sel", "g1"), ("g1", "c1"), ("c1", "a1"), ("a1", "v7"),
             ("sel", "e1"), ("e1", "g2"), ("g2", "c2"), ("c2", "e2"), ("e2", "c3"), ("c3", "a2"), ("a2", "v8")]
    note = ("*Chapter 9. Corpus (BBC3): move Title to Ignored so only Content is used. Each summarizer runs as soon as data "
            "arrives, and the first run of each model downloads it. Corpus Viewer: tick the summary column under Display Features. "
            "Ollama needs a running server with llama3.1:8b; connect Data Sampler to it yourself (about 3 minutes). 9C: Select Rows "
            "Chapter is 1. Group by Chapter: aggregate Paragraph (or the summary column) with Concatenate. In each Corpus widget make the joined "
            "column the text feature.*")
    return build(nodes, links, [(note, "(80.0, 200.0, 420.0, 260.0)")])


SVO_SCRIPT = """import json
from Orange.data import Domain, StringVariable, Table

tags = in_data.domain["POS Tags"]
sentence = in_data.domain.metas[0]
rows = []
for doc in in_data:
    tokens = json.loads(str(doc[tags]))
    for i, t in enumerate(tokens):
        if t["dep"].lower() != "root":
            continue
        children = lambda labels: [tokens[j]["text"] for j, u in enumerate(tokens)
                                   if j + u["head"] == i and j != i and u["dep"] in labels]
        subject = children(("nsubj", "nsubj:pass", "nsubjpass"))
        obj = children(("dobj", "obj"))
        if subject and obj:
            rows.append([str(doc[sentence]), subject[0], t["text"], obj[0]])

domain = Domain([], metas=[StringVariable(n) for n in ("Sentence", "Subject", "Verb", "Object")])
out_data = Table.from_list(domain, rows)
"""


def dependency_parsing():
    """Chapter 10: 10A read trees from three taggers, 10B extract subject-verb-object triples, 10C POS filter."""
    fw = lambda name: {"selected_framework": name, "controlAreaVisible": True}
    script = {"__version__": 2, "scriptLibrary": [{"name": "SVO triples", "script": SVO_SCRIPT, "filename": None}],
              "currentScriptIndex": 0, "scriptText": SVO_SCRIPT}
    nodes = [
        corpus("ps", "parse-sentences.tab", "Corpus: parse-sentences (10A)", 100),
        ("tsp", "POS Tagger", "POS Tagger: spaCy (10A)", (330, 20), fw("spaCy")),
        ("tud", "POS Tagger", "POS Tagger: UDPipe (10A)", (330, 120), fw("UDPipe")),
        ("tst", "POS Tagger", "POS Tagger: Stanza (10A)", (330, 220), fw("Stanza")),
        ("vsp", "POS Viewer", "POS Viewer: spaCy (10A)", (560, 20), {}),
        ("vud", "POS Viewer", "POS Viewer: UDPipe (10A)", (560, 120), {}),
        ("vst", "POS Viewer", "POS Viewer: Stanza (10A)", (560, 220), {}),
        corpus("hk", "huck.tab", "Corpus: huck (10B, 10C)", 480),
        ("th", "POS Tagger", "POS Tagger: spaCy (10B)", (330, 380), fw("spaCy")),
        ("py", "Python Script", "Python Script: SVO triples (10B)", (560, 380), script),
        ("dt", "Data Table", "Data Table: triples (10B)", (780, 380), {}),
        ("rs", "Rule-based Entity-Relationship Extraction", "Relations: parse-sentences (10B)", (330, 300), {}),
        ("ds_", "Data Table", "Data Table: relations, sentences (10B)", (560, 300), {}),
        ("rh", "Rule-based Entity-Relationship Extraction", "Relations: huck (10B)", (330, 460), {}),
        ("dh", "Data Table", "Data Table: relations, huck (10B)", (560, 460), {}),
        ("pp", "Preprocess Text", "Preprocess Text: POS filter (10C)", (330, 580), {}),
        ("wc", "Word Cloud", "Word Cloud (10C)", (560, 580), {}),
        ("dw", "Data Table", "Data Table: word counts (10C)", (780, 580), {}),
    ]
    links = [("ps", "tsp"), ("ps", "tud"), ("ps", "tst"), ("tsp", "vsp"), ("tud", "vud"), ("tst", "vst"),
             ("ps", "rs"), ("rs", "ds_"), ("hk", "rh"), ("rh", "dh"), ("hk", "th"), ("th", "py"), ("py", "dt"), ("hk", "pp"), ("pp", "wc"), ("wc", "dw")]
    note = ("*Chapter 10. 10A: each tagger takes a few seconds, Stanza about a minute the first time. 10B: the Python Script "
            "keeps sentences whose root verb has a subject and an object; change the framework in the POS Tagger and compare. "
            "10C: in Preprocess Text use the Regexp tokenizer (pattern [\\w\u2019]+, no Lowercase), then the POS Tagger stage "
            "(Averaged Perceptron), then the POS tags filter, and type the tags to keep (NN,NNS,NNP,NNPS).*")
    return build(nodes, links, [(note, "(80.0, 680.0, 760.0, 110.0)")])


def check(path):
    """Load the .ows with Orange's own reader; print node/link counts and errors."""
    import os
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orangecanvas.registry import WidgetRegistry
    from orangecanvas.scheme import Scheme
    from orangecanvas.scheme.readwrite import scheme_load
    from orangewidget.workflow.discovery import WidgetDiscovery
    from Orange.canvas import config
    reg = WidgetRegistry()
    WidgetDiscovery(reg).run(config.widgets_entry_points())
    scheme, errors = Scheme(), []
    with open(path, "rb") as f:
        scheme_load(scheme, f, registry=reg, error_handler=errors.append)
    print(f"{path}: {len(scheme.nodes)} nodes, {len(scheme.links)} links, errors={errors}")
    return not errors


# name -> (builder, output file under workflows/).  Add new workflows here.
WORKFLOWS = {"word-embeddings": (word_embeddings, "word-embeddings.ows"),
             "document-embeddings": (document_embeddings, "document-embeddings.ows"),
             "question-answering": (question_answering, "question-answering.ows"),
             "llm-tasks": (llm_tasks, "llm-tasks.ows"),
             "rag": (rag, "rag.ows"),
             "cleaning-headlines": (cleaning_headlines, "cleaning-headlines.ows"),
             "headline-classifier": (headline_classifier, "headline-classifier.ows"),
             "clustering-books": (clustering_books, "clustering-books.ows"),
             "topics-news": (topics_news, "topics-news.ows"),
             "classifier-evaluation": (classifier_evaluation, "classifier-evaluation.ows"),
             "sentiment-reviews": (sentiment_reviews, "sentiment-reviews.ows"),
             "named-entities": (named_entities, "named-entities.ows"),
             "summarization": (summarization, "summarization.ows"),
             "dependency-parsing": (dependency_parsing, "dependency-parsing.ows")}

if __name__ == "__main__":
    import sys
    names = [a for a in sys.argv[1:] if not a.startswith("-")] or list(WORKFLOWS)
    for name in names:
        fn, fname = WORKFLOWS[name]
        dest = BOOK / "workflows" / fname
        dest.write_text(fn())
        print("wrote", dest)
        if "--check" in sys.argv:
            check(dest)
