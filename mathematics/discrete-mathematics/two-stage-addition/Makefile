.PHONY: paper verify
paper:
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
verify:
	python3 verify.py
	g++ -O3 -std=c++17 verify_full.cpp -o /tmp/addition-state-verify
	/tmp/addition-state-verify > evidence/full-binary-census.json
