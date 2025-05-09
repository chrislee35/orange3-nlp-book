# Book Metadata
TITLE="Natural Language Processing with Orange"
AUTHOR="Course Team"
OUTDIR=nlp-book
OUTPUT=$(OUTDIR)/orange3-nlp-book
INPUT=README.md \
       01-Introduction.md \
       02-Orange.md \
       03-Text\ Data.md \
       04-Text\ Classification.md \
       05-Topic\ Modeling.md \
       06-Evaluation.md \
       07-Sentiment.md \
       08-Recognition.md \
       09-Summarization.md \
       10-Parts\ of\ Speech.md \
       11-Embeddings.md \
       12-Document\ Embeddings.md \
       13-Question\ Answering.md \
       14-LLMs.md \
       15-RAGs.md \
       16-Capstone.md

# Default rule
all: $(OUTDIR) html pdf epub

# Ensure output directory exists
$(OUTDIR):
	mkdir -p $(OUTDIR)

# Combine all markdown files into a single one
$(OUTPUT).md: $(INPUT) | $(OUTDIR)
	mkdir -p $(OUTDIR)
	rm -rf $(OUTPUT).md
	for file in $(INPUT); do \
		cat "$$file" >> $(OUTPUT).md; \
		echo '<div style="page-break-before: always;"></div>' >> $(OUTPUT).md; \
	done

# Generate HTML
html: $(OUTPUT).md
	pandoc $(OUTPUT).md -o $(OUTPUT).html \
		--metadata title=$(TITLE) --toc --standalone

# Generate PDF
pdf: $(OUTPUT).md
	pandoc $(OUTPUT).md -o $(OUTPUT).pdf \
		--pdf-engine=weasyprint \
		--metadata title=$(TITLE) \
		--toc \
		--standalone

# Generate EPUB
epub: $(OUTPUT).md
	pandoc $(OUTPUT).md -o $(OUTPUT).epub \
		--metadata title=$(TITLE) \
		--toc \
		--standalone

# Clean up
clean:
	rm -rf $(OUTDIR)
