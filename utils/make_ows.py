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
    "Distance Matrix": ("Orange.widgets.unsupervised.owdistancematrix.OWDistanceMatrix", "Orange3"),
}
# (source name, source id) -> (sink name, sink id) keyed by (source widget, sink widget)
LINKS = {
    ("Corpus", "Text Embedder"): (("Corpus", "corpus"), ("Corpus", "data")),
    ("SBERT Embedder", "Text Embedder"): (("Embedder", "embedder"), ("Embedder", "embedder")),
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
WORKFLOWS = {"word-embeddings": (word_embeddings, "word-embeddings.ows")}

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
