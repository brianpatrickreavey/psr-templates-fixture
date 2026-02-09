.PHONY: ci-simulate

# Simulate CI with act
ci-simulate:
	act repository_dispatch -e .act/event.json --container-architecture linux/amd64