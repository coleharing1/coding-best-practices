PYTHON := uv run --python 3.11 python
CTL := uv run --python 3.11 ./bin/crosscheckctl

.PHONY: validate council-doctor council-test council-sync-check council-sync-install council-plugin-validate

validate:
	$(PYTHON) scripts/validate_repo.py

council-doctor:
	$(CTL) doctor

council-test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

council-sync-check:
	$(PYTHON) _scripts/sync-crosscheck.py --check

council-sync-install:
	$(PYTHON) _scripts/install-crosscheck-integrations.py

council-plugin-validate:
	claude plugin validate --strict integrations/claude-plugin
