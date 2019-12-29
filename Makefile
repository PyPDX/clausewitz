build: ci version
	python setup.py sdist

name := pypdx-clausewitz
v := `python -c "from clausewitz import __version__; print(__version__)"`

version:
	@echo "Current version: $(v). Do you confirm? (y/n)"
	@read y_n && [ "$${y_n}" == "y" ]

lint:
	flake8 .

test:
	pytest --cov --cov-report term-missing:skip-covered

ci: lint test

upload: build
	twine upload "dist/$(name)-$(v).tar.gz"
