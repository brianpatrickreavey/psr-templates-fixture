.PHONY: ci-simulate clean-tags clean-releases clean-tags-and-releases clean test unzip-artifacts

# Run tests
test:
	uv run pytest tests/ -v

# Clean up build artifacts and templates
clean:
	rm -rf templates/ .artifacts/

# Unzip all artifacts for inspection
unzip-artifacts:
	@echo "Extracting artifacts..." && \
	find .artifacts -name "*.zip" -type f | while read zip; do \
	  dir="$${zip%.zip}"; \
	  mkdir -p "$$dir"; \
	  unzip -oq "$$zip" -d "$$dir"; \
	done
	@echo "Artifacts extracted to .artifacts/"

# Simulate CI with act
ci-simulate:
	@timestamp=$$(date +%Y%m%d-%H%M%S); \
	echo "Running CI simulation (artifacts: .artifacts/$$timestamp)"; \
	act repository_dispatch \
	  --artifact-server-path ".artifacts/$$timestamp" \
	  -W .github/workflows/test-harness-act.yml \
	  -e .act/event.json \
	  --container-architecture linux/amd64 \
	  --env GITHUB_RUN_ID="$$timestamp"; \
	echo "Artifacts stored in .artifacts/$$timestamp"

# Clean up all tags in the fixture repo
clean-tags:
	gh api repos/brianpatrickreavey/psr-templates-fixture/git/refs/tags > /dev/null 2>&1 && gh api repos/brianpatrickreavey/psr-templates-fixture/git/refs/tags --jq '.[].ref' | sed 's|refs/tags/||' | xargs -I {} gh api repos/brianpatrickreavey/psr-templates-fixture/git/refs/tags/{} -X DELETE || true

# Clean up all releases in the fixture repo
clean-releases:
	gh api repos/brianpatrickreavey/psr-templates-fixture/releases > /dev/null 2>&1 && gh api repos/brianpatrickreavey/psr-templates-fixture/releases --jq '.[].id' | xargs -I {} gh api repos/brianpatrickreavey/psr-templates-fixture/releases/{} -X DELETE || true

# Clean up all tags and releases in the fixture repo
clean-tags-and-releases: clean-tags clean-releases