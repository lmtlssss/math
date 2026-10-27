.PHONY: verify paper figure preview clean
verify:
	python3 verify.py
paper:
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
figure:
	blender -b --python visual/build_scene.py
preview:
	python3 visual/preview.py
clean:
	rm -f paper.aux paper.log paper.out
