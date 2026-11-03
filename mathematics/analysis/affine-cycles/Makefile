PYTHON ?= python3
XELATEX ?= xelatex
BLENDER ?= blender
THREADS ?= 4

.PHONY: all verify pdf figure package
all: verify pdf

verify:
	$(PYTHON) verify.py

pdf:
	$(XELATEX) -interaction=nonstopmode -halt-on-error paper.tex
	$(XELATEX) -interaction=nonstopmode -halt-on-error paper.tex

figure:
	@test -n "$(STYLE_BLEND)" || (echo "Set STYLE_BLEND to the canonical tensor-note-v1.0.0 scene"; exit 1)
	$(BLENDER) --background "$(STYLE_BLEND)" --threads $(THREADS) --python-exit-code 1 --python visual/build_scene.py

package:
	$(PYTHON) package_release.py
