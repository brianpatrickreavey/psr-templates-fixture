.PHONY: ci-simulate ci-simulate-consolidated ci-simulate-consolidated-gitea start-gitea stop-gitea clean-tags clean-releases clean-tags-and-releases clean test unzip-artifacts

# Gitea configuration
GITEA_CONTAINER = act-gitea-local
GITEA_IMAGE = gitea/gitea:latest
GITEA_PORT = 3000

# Run tests
test:
	uv run pytest tests/ -v

# Clean up build artifacts and templates
clean:
	rm -rf templates/ .artifacts/ .pytest_cache/ build/ dist/ *.egg-info src/*.egg-info

# Unzip all artifacts for inspection (including nested addon zips)
unzip-artifacts:
	@echo "Extracting artifacts..." && \
	max_iterations=10; \
	iteration=0; \
	while [ $$iteration -lt $$max_iterations ]; do \
	  zip_count=$$(find .artifacts -name "*.zip" -type f | wc -l); \
	  [ $$zip_count -eq 0 ] && break; \
	  find .artifacts -name "*.zip" -type f | while read zip; do \
	    dir="$${zip%.zip}"; \
	    mkdir -p "$$dir"; \
	    unzip -oq "$$zip" -d "$$dir"; \
	  done; \
	  iteration=$$((iteration + 1)); \
	done
	@echo "Artifacts extracted to .artifacts/"

# Simulate CI with act
ci-simulate:
	@timestamp=$$(date +%Y%m%d-%H%M%S); \
	mkdir -p .artifacts/$$timestamp; \
	echo "Running CI simulation (artifacts: .artifacts/$$timestamp)"; \
	act repository_dispatch \
	  --artifact-server-path ".artifacts/$$timestamp" \
	  -W .github/workflows/test-harness-act.yml \
	  -e .act/event.json \
	  --container-architecture linux/amd64 \
	  --env GITHUB_RUN_ID="$$timestamp" \
	  | tee .artifacts/$$timestamp/ci-simulate.log; \
	echo "Artifacts stored in .artifacts/$$timestamp"; \
	echo "Log file: .artifacts/$$timestamp/ci-simulate.log"

# Simulate CI with consolidated workflow
ci-simulate-consolidated:
	@timestamp=$$(date +%Y%m%d-%H%M%S); \
	mkdir -p .artifacts/$$timestamp; \
	echo "Running consolidated CI simulation (artifacts: .artifacts/$$timestamp)"; \
	act repository_dispatch \
	  --artifact-server-path ".artifacts/$$timestamp" \
	  -W .github/workflows/test-harness-consolidated.yml \
	  -e .act/event.json \
	  --container-architecture linux/amd64 \
	  --env ACT_RUN_ID="act-test-run-$$timestamp" \
	  | tee .artifacts/$$timestamp/ci-simulate-consolidated.log; \
	echo "Artifacts stored in .artifacts/$$timestamp"; \
	echo "Log file: .artifacts/$$timestamp/ci-simulate-consolidated.log"

# Start local Gitea server
start-gitea:
	@echo "Cleaning up any existing Gitea container..." && \
	docker rm -f $(GITEA_CONTAINER) 2>/dev/null || true; \
	echo "Preparing Gitea data directory..." && \
	mkdir -p /tmp/gitea-data/conf && \
	bash ./tools/gitea-config-gen.sh /tmp/gitea-data/conf/app.ini && \
	echo "Starting Gitea on port $(GITEA_PORT)..." && \
	docker run -d \
		--name $(GITEA_CONTAINER) \
		-p $(GITEA_PORT):3000 \
		-p 2222:22 \
		-v /tmp/gitea-data:/data \
		$(GITEA_IMAGE) && \
	echo "Waiting for Gitea to be healthy..." && \
	max_attempts=30; \
	attempt=0; \
	while [ $$attempt -lt $$max_attempts ]; do \
		if curl -s http://localhost:$(GITEA_PORT) > /dev/null 2>&1; then \
			echo "✓ Gitea is ready"; \
			break; \
		fi; \
		if [ $$attempt -eq $$((max_attempts - 1)) ]; then \
			echo "✗ Gitea failed to start"; \
			docker rm -f $(GITEA_CONTAINER) 2>/dev/null || true; \
			exit 1; \
		fi; \
		sleep 1; \
		attempt=$$((attempt + 1)); \
	done && \
	echo "Creating install.lock to skip wizard..." && \
	docker exec $(GITEA_CONTAINER) touch /data/gitea/conf/install.lock && \
	echo "✓ Gitea installation locked"

# Stop local Gitea server
stop-gitea:
	@echo "Stopping Gitea..." && \
	docker rm -f $(GITEA_CONTAINER) 2>/dev/null || echo "Gitea container not running"

# Simulate CI with consolidated-with-gitea workflow (local Gitea server)
ci-simulate-consolidated-gitea: start-gitea
	@timestamp=$$(date +%Y%m%d-%H%M%S); \
	mkdir -p .artifacts/$$timestamp; \
	echo "Running consolidated-with-gitea CI simulation (artifacts: .artifacts/$$timestamp)"; \
	act repository_dispatch \
	  --artifact-server-path ".artifacts/$$timestamp" \
	  -W .github/workflows/test-harness-consolidated-with-gitea.yml \
	  -e .act/event.json \
	  --container-architecture linux/amd64 \
	  --env ACT_RUN_ID="act-test-run-$$timestamp" \
	  | tee .artifacts/$$timestamp/ci-simulate-consolidated-gitea.log; \
	exit_code=$$?; \
	make stop-gitea; \
	exit $$exit_code

# Clean up all tags in the fixture repo
clean-tags:
	gh api repos/brianpatrickreavey/psr-templates-fixture/git/refs/tags > /dev/null 2>&1 && gh api repos/brianpatrickreavey/psr-templates-fixture/git/refs/tags --jq '.[].ref' | sed 's|refs/tags/||' | xargs -I {} gh api repos/brianpatrickreavey/psr-templates-fixture/git/refs/tags/{} -X DELETE || true

# Clean up all releases in the fixture repo
clean-releases:
	gh api repos/brianpatrickreavey/psr-templates-fixture/releases > /dev/null 2>&1 && gh api repos/brianpatrickreavey/psr-templates-fixture/releases --jq '.[].id' | xargs -I {} gh api repos/brianpatrickreavey/psr-templates-fixture/releases/{} -X DELETE || true

# Clean up all tags and releases in the fixture repo
clean-tags-and-releases: clean-tags clean-releases