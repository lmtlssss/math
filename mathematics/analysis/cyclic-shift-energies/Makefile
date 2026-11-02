verify:
	python3 verify.py --output evidence/verification.json

paper: verify
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
