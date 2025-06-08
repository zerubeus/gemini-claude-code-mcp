.DEFAULT_GOAL := all

.PHONY: .uv
.uv: ## Check that uv is installed
	@uv --version || echo 'Please install uv: https://docs.astral.sh/uv/getting-started/installation/'

.PHONY: .pre-commit
.pre-commit: ## Check that pre-commit is installed
	@pre-commit -V || echo 'Please install pre-commit: https://pre-commit.com/'

.PHONY: install
install: .uv .pre-commit ## Install the package, dependencies, and pre-commit for local development
	uv sync
	pre-commit install --install-hooks

.PHONY: format
format: ## Format the code
	uv run ruff format
	uv run ruff check --fix --fix-only

.PHONY: lint
lint: ## Lint the code
	uv run ruff format --check
	uv run ruff check

.PHONY: typecheck
typecheck:
	@# PYRIGHT_PYTHON_IGNORE_WARNINGS avoids the overhead of making a request to github on every invocation
	PYRIGHT_PYTHON_IGNORE_WARNINGS=1 uv run pyright

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf dist/
	rm -rf *.egg-info/

.PHONY: build
build: clean ## Build the package distribution
	uv build

.PHONY: get-latest-version
get-latest-version: ## Get the latest version from git tags
	@LATEST_TAG=$$(git tag -l "v[0-9]*.[0-9]*.[0-9]*" | sort -V | tail -n1); \
	if [ -z "$$LATEST_TAG" ]; then \
		echo "0.0.0"; \
	else \
		echo "$${LATEST_TAG#v}"; \
	fi

.PHONY: release
release: all build ## Create a new release on GitHub (requires VERSION env var or auto-increments patch)
	@if [ -z "$$VERSION" ]; then \
		CURRENT_VERSION=$$(make -s get-latest-version); \
		MAJOR=$$(echo $$CURRENT_VERSION | cut -d. -f1); \
		MINOR=$$(echo $$CURRENT_VERSION | cut -d. -f2); \
		PATCH=$$(echo $$CURRENT_VERSION | cut -d. -f3); \
		NEW_PATCH=$$((PATCH + 1)); \
		VERSION="$$MAJOR.$$MINOR.$$NEW_PATCH"; \
		echo "No VERSION specified, auto-incrementing to $$VERSION"; \
	fi; \
	echo "Creating release v$$VERSION..."; \
	if ! echo "$$VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$$'; then \
		echo "ERROR: Version $$VERSION must be in format X.Y.Z (e.g. 1.0.0)"; \
		exit 1; \
	fi; \
	if git rev-parse "v$$VERSION" >/dev/null 2>&1; then \
		echo "ERROR: Tag v$$VERSION already exists"; \
		exit 1; \
	fi; \
	git tag -a "v$$VERSION" -m "Release v$$VERSION"; \
	git push origin "v$$VERSION"; \
	echo "Successfully created and pushed tag v$$VERSION"

.PHONY: publish
publish: all build ## Publish the package to PyPI
	@if [ ! -f .env ]; then \
		echo "ERROR: Missing .env file with PYPI_TOKEN"; \
		exit 1; \
	fi
	@echo "Publishing to PyPI..."
	. .env && uv publish --token $$PYPI_TOKEN
	@echo "Successfully published to PyPI"

.PHONY: all
all: format lint typecheck ## Run code formatting, linting, static type checks
