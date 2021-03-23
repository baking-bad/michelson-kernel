install:
	bash -c "python -m venv .venv; source .venv/bin/activate; pip install wheel jupyter; pip install .; pip install -U pytezos-3.0.4-py3-none-any.whl"

debug:
	pip install . --force --no-deps --user

isort:
	bash -c "python -m venv .venv; source .venv/bin/activate; pip install isort; isort michelson_kernel/kernel.py"

black:
	bash -c "python -m venv .venv; source .venv/bin/activate; pip install black; black -S -l 140 michelson_kernel/kernel.py"

mypy:
	bash -c "python -m venv .venv; source .venv/bin/activate; pip install mypy; mypy michelson_kernel/kernel.py"

lint: isort black mypy

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
