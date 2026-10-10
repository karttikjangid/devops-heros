# Configuration error

This was an intentionally introduced classroom fault in `session14-lab`.

- Problem/root cause: An environment variable referenced a missing MODE key.
- Investigation: Pod status showed CreateContainerConfigError; describe identified the missing key.
- Fix: Added MODE=homework to the ConfigMap.
- Verification: The container started and printenv returned homework.

![Real before-and-after output](../../screenshots/configuration.png)

[Complete commands and output](../../screenshots/configuration.txt)
