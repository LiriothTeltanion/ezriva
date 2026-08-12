.PHONY: setup lint typecheck test build secret-scan verify test-ai-fixtures

setup:
	python scripts/verify.py setup

lint:
	python scripts/verify.py lint

typecheck:
	python scripts/verify.py typecheck

test:
	python scripts/verify.py test

build:
	python scripts/verify.py build

secret-scan:
	python scripts/verify.py secret-scan

verify:
	python scripts/verify.py verify

test-ai-fixtures:
	python scripts/verify.py ai-fixtures

.PHONY: test-ai-fixtures-live
test-ai-fixtures-live:
	uv run python scripts/run_ai_fixture_eval.py --live --acknowledge-metered-bedrock
