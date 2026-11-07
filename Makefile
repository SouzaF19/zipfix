.PHONY: install test run build clean check

install:
	python -m pip install -e .

test:
	python -m unittest discover -s tests -v

run:
	python -m zipflix fix $(INPUT) --out $(OUT)

build:
	python -m build

clean:
	rm -rf dist build *.egg-info __pycache__ zipflix/__pycache__ tests/__pycache__
