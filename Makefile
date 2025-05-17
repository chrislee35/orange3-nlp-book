# Book Metadata
TITLE="Natural Language Processing (NLP) with Orange: A Lab-Based Approach"
AUTHOR="Course Team"
OUTDIR=nlp-book
FILEBASE=orange3-nlp-book
OUTPUT=$(OUTDIR)/$(FILEBASE)
INPUT=README.md \
       chapters/01/Introduction.md \
       chapters/02/Orange.md \
       chapters/03/Text\ Data.md \
       chapters/04/Text\ Classification.md \
       chapters/05/Topic\ Modeling.md \
       chapters/06/Evaluation.md \
       chapters/07/Sentiment.md \
       chapters/08/Recognition.md \
       chapters/09/Summarization.md \
       chapters/10/Parts\ of\ Speech.md \
       chapters/11/Embeddings.md \
       chapters/12/Document\ Embeddings.md \
       chapters/13/Question\ Answering.md \
       chapters/14/LLMs.md \
       chapters/15/RAGs.md \
       chapters/16/Capstone.md

# Default rule
all: $(OUTDIR) html pdf epub

# Ensure output directory exists
$(OUTDIR):
	mkdir $(OUTDIR)

# Combine all markdown files into a single one
$(OUTPUT).md: $(INPUT) | $(OUTDIR)
	mkdir -p $(OUTDIR)/imgs
	rm -rf $(OUTPUT).md
	for file in $(INPUT); do \
		cat "$$file" >> $(OUTPUT).md; \
		echo '<div style="page-break-before: always;"></div>' >> $(OUTPUT).md; \
	done
	cat $(OUTPUT).md | utils/fix_links.py > $(OUTPUT).md2
	mv $(OUTPUT).md2 $(OUTPUT).md
	find chapters/ -name '*.png' -exec cp "{}" $(OUTDIR)/imgs \;
	cp imgs/* $(OUTDIR)/imgs

# Generate HTML
html: $(OUTPUT).md
	pandoc $(OUTPUT).md -o $(OUTPUT).html \
		--metadata title=$(TITLE) \
		--css css/nlp-book.css \
		--toc \
		--standalone

# Generate PDF
pdf: $(OUTPUT).md
	cd $(OUTDIR) && \
	pandoc $(FILEBASE).md -o $(FILEBASE).pdf \
		--metadata title=$(TITLE) \
		--pdf-engine=weasyprint \
		--toc \
		--standalone

# Generate EPUB
epub: $(OUTPUT).md
	cd $(OUTDIR) && \
	pandoc $(FILEBASE).md -o $(FILEBASE).epub \
		--metadata title=$(TITLE) \
		--toc \
		--standalone

# Clean up
clean:
	rm -rf $(OUTDIR)
