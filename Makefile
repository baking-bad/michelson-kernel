publish:
	python setup.py dist
	twine upload dist/*