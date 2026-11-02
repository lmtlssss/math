verify:
	python3 verify.py --output evidence/verification.json
	python3 verify_extension.py

paper: verify
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
