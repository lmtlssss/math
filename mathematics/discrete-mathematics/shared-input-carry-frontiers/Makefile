.PHONY: verify paper figure
verify:
	python3 verify.py
paper:
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
figure:
	blender -b --python visual/build_scene.py
