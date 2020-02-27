debug:
	$(MAKE) remove
	pip install . --force --no-deps

publish:
	python setup.py dist
	twine upload dist/*

remove:
	jupyter kernelspec uninstall michelson -f

docs:
	python -m scripts.gen_docs_py
