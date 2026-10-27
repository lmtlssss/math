.PHONY: paper verify figure
paper:
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
	xelatex -interaction=nonstopmode -halt-on-error paper.tex
verify:
	python3 verify.py
figure:
	blender -b --python visual/build_scene.py
