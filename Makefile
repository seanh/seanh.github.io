.PHONY: help
help:
	@echo "make dev"
	@echo "    Run the dev server at http://localhost:8000/."
	@echo "make requirements"
	@echo "    Re-compile the requirements files."
	@echo "make upgrade"
	@echo "    Upgrade all requirements to the latest versions."
	@echo "make upgrade-package package=foo"
	@echo "    Upgrade foo to the latest version."
	@echo "make upgrade-package package=foo==1.2.3"
	@echo "    Upgrade or downgrade foo to 1.2.3."
	@echo "make deploy"
	@echo "    Deploy the latest version of the site to GitHub Pages."

.PHONY: dev
dev: python
dev:
	tox

.PHONY: requirements
requirements: python
requirements:
	tox -e pipcompile

.PHONY: upgrade
upgrade: python
upgrade:
	tox -e pipcompile -- --upgrade

.PHONY: upgrade-package
upgrade-package: python
upgrade-package:
	tox -e pipcompile -- --upgrade-package $(package)

.PHONY: deploy
deploy:
	@gh workflow run --ref main deploy.yml > /dev/null && GITHUB_TOKEN=$$(gh auth token) watch_gha_runs --wait-for-start

.PHONY: python
python:
	pyenv install --skip-existing
