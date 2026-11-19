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
}
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
             "rag": (rag, "rag.ows")}

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
