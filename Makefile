install:
	poetry install

post-install:
	poetry run python post-install.py

debug:
	pip install . --force --no-deps

isort:
	poetry run isort src

pylint:
	poetry run pylint src || poetry run pylint-exit $$?

mypy:
	poetry run mypy src

lint: isort pylint mypy

build:
	poetry build

image:
	docker build . -t michelson-kernel

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
