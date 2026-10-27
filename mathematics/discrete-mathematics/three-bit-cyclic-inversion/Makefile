.PHONY: paper verify clean
paper:
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
verify:
	python3 verify.py
clean:
	rm -f paper.aux paper.log paper.out
