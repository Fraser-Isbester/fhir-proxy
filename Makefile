
.PHONY: test
test:
	python -m pytest -v

.PHONY: lint lint-fix
lint:
	ruff .

lint-fix:
	black . -C --line-length 100
	ruff . --fix
