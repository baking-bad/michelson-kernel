debug:
	pip install . --force --no-deps --user

publish:
	python setup.py sdist
	twine upload dist/*
	rm -rf dist/

remove:
	jupyter kernelspec uninstall michelson -f

docs:
	python -m scripts.gen_docs_py

kernel:
	python -m michelson_kernel
