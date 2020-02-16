publish:
	python setup.py dist
	twine upload dist/*

install:
	pip install . --force

remove:
	jupyter kernelspec uninstall michelson

docs:
	python -m scripts.gen_docs_py