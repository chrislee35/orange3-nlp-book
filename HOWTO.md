# How to build the NLP Book

I made the build system for Linux.

So, to build the book, you'll need the following:

* Python
* pillow python package
* pandoc
* weasyprint
* make

If you need to build on Windows or Mac, just let me know and we'll figure it out together.

## If you want to change the chapters around or add/remove chapters.

I tried to make this easy, but it's hard to make it flexible.  In chapters.conf, I enumerate all the input files in the order that they should appear in the output.  So, you can easily add or remove chapters there.  

If you include directories that are outside of the chapters folder, then you'll need to add copy commands to move any images into the nlp-book/imgs folder.  Add those copy command after these lines:
```make
	# custom resources would go here
	# e.g., cp mychapters/phishing_detection/*.jpeg $(OUTDIR)/imgs
```

## Image sizes

If you include images wider than 600px, please consider resizing them to a width of 600px, which makes them about 6 1/4" (158.75mm) wide, which fits well on letter-size paper.  If your main target is web browsers, then 1200px wide is a good, modern target size.