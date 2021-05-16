.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: lint
lint:  ## Linter the code.
	@echo "🚨 Linting code"
	poetry run isort spec_parser tests --check
	poetry run flake8 spec_parser tests
	poetry run mypy spec_parser
	poetry run black spec_parser tests --check --diff


.PHONY: format
format:
	@echo "🎨 Formatting code"
	poetry run isort spec_parser tests
	poetry run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place spec_parser tests --exclude=__init__.py
	poetry run black spec_parser tests


.PHONY: test
test:  ## Test your code.
	@echo "🍜 Running pytest"
	poetry run pytest tests/ --cov=spec_parser --cov-report=term-missing:skip-covered --cov-report=xml --cov-fail-under 100
