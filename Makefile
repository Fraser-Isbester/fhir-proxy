
.PHONY: test
test:
	python -m pytest -v

.PHONY: lint
lint:
	ruff .

.PHONY: lint-fix
lint-fix:
	black . -C --line-length 100
	ruff . --fix

.PHONY: clean-cache
clean-cache:  ## Deletes every __pycache__ folder in the project
	find . -type d -name "__pycache__" -exec rm -rf {} +

requirements.txt: poetry.lock  ## Generates a requirements.txt with the latest dependencies
	poetry export -f requirements.txt --output requirements.txt
