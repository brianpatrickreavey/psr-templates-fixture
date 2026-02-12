.PHONY: ci-simulate clean-tags clean-releases clean-tags-and-releases

# Simulate CI with act
ci-simulate:
	act repository_dispatch -W .github/workflows/test-harness-act.yml -e .act/event.json --container-architecture linux/amd64

# Clean up all tags in the fixture repo
clean-tags:
	gh api repos/brianpatrickreavey/psr-templates-fixture/git/refs/tags > /dev/null 2>&1 && gh api repos/brianpatrickreavey/psr-templates-fixture/git/refs/tags --jq '.[].ref' | sed 's|refs/tags/||' | xargs -I {} gh api repos/brianpatrickreavey/psr-templates-fixture/git/refs/tags/{} -X DELETE || true

# Clean up all releases in the fixture repo
clean-releases:
	gh api repos/brianpatrickreavey/psr-templates-fixture/releases > /dev/null 2>&1 && gh api repos/brianpatrickreavey/psr-templates-fixture/releases --jq '.[].id' | xargs -I {} gh api repos/brianpatrickreavey/psr-templates-fixture/releases/{} -X DELETE || true

# Clean up all tags and releases in the fixture repo
clean-tags-and-releases: clean-tags clean-releases