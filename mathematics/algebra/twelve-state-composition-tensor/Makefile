.PHONY: verify paper clean

verify:
	python3 verify.py

paper: verify
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
	xelatex -interaction=nonstopmode -halt-on-error paper.tex

clean:
	rm -f paper.aux paper.log paper.out paper.toc
