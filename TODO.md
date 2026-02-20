# TODO List

- Bypass kodi-check. We're only doing Kodi right now. (Removed kodi-check jobs from workflow, hardcoded Kodi values)
- Serialize the workflow. (Changed to single job with phases in series)
- Restore uploading the CHANGELOG.md and addon.xml files directly to the build. (Added upload steps to consolidated-kodi-zip action)

## ACT Test Harness Oddities (Benign - Investigate Later)

- Fix "Non-terminating error while running 'git clone'" warnings during action checkout (ACT framework issue, doesn't affect workflow)
- Fix branch deletion errors in setup job (errors when trying to delete files as branches, expected but could be cleaner)
- Fix "cannot delete branch" warning for current branch (expected behavior, but cleanup script could be smarter)
