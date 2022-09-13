SHELL := bash

DUTY = $(shell [ -n "${VIRTUAL_ENV}" ] || echo pdm run) duty

BASIC_DUTIES = \
	clean \
	coverage \
	format

QUALITY_DUTIES = \
	check-quality \
	check-types \
	test

.PHONY: help
help:
	@$(DUTY) --list

.PHONY: setup
setup:
	@bash scripts/setup.sh

.PHONY: $(BASIC_DUTIES)
$(BASIC_DUTIES):
	@$(DUTY) $@ $(call args, $@)

.PHONY: $(QUALITY_DUTIES)
$(QUALITY_DUTIES):
	@$(DUTY) $@ $(call args, $@)
