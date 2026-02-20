# TODO List

- Bypass kodi-check. We're only doing Kodi right now. (Removed kodi-check jobs from workflow, hardcoded Kodi values)
- Serialize the workflow. (Changed to single job with phases in series)
- Restore uploading the CHANGELOG.md and addon.xml files directly to the build. (Added upload steps to consolidated-kodi-zip action)