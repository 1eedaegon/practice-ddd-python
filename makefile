NAME := ./src/
TEST := ./tests/
INSTALL_STAMP := .install.stamp
POETRY := poetry
DOCKER := docker

.DEFAULT_GOAL := help

# Trick of help using awk
# Using it as a make help statement after parsing '##' 
# help:
#	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "\033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install            install packages and prepare environment"
	@echo "  (deprecated)       add <package>      now use: poetry add <package> "    
	@echo "  (deprecated)       add-dev <package>  now use: poetry add -D <package> "
	@echo "  clean              remove all temporary files"
	@echo "  lint               run the code linters"
	@echo "  format             reformat code"
	@echo "  test               run all the tests"
	@echo "  unit-test 	        run all unit-tests"
	@echo "  export-lib         export poetry.lock -> requirements.txt"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo "$(POETRY) Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi;
	$(POETRY) install
	touch $(INSTALL_STAMP)

.PHONY: clean
clean:
	find -type d -name "__pychache__" | xargs rm -rf {};
	rm -rf $(INSTALL_STAMP) .coverage .mypy_cache

.PHONY: lint
lint:
	$(POETRY) run python -m isort --profile=black --lines-after-imports=2 --check-only $(TEST) $(NAME) 
	$(POETRY) run python -m black --check $(TEST) $(NAME) --diff

.PHONY: format
format: $(INSTALL_STAMP)
	$(POETRY) run python -m isort --profile=black --lines-after-imports=2 $(TEST) $(NAME)
	$(POETRY) run python -m black $(TEST) $(NAME)

.PHONY: unit-test
unit-test: $(INSTALL_STAMP)
	$(POETRY) run python -m pytest --tb=short

.PHONY: test
test: $(INSTALL_STAMP)
	$(POETRY) run python -m pytest $(TEST) --cov-report term-missing --cov-fail-under 100 --cov $(NAME)

.PHONY: export-lib
export-lib: 
	$(POETRY) export -f requirements.txt --output requirements.txt


