# Pending

Introduced this fault in `session14-lab` to practice finding and fixing it.

- Problem/root cause: A 1000-CPU request exceeded node capacity.
- Investigation: Describe showed FailedScheduling / insufficient CPU.
- Fix: Reduced requests to the small demo requirements.
- Verification: The replacement Pod was scheduled and became Ready.

![Recorded output in Mac zsh: Before and after output](../../screenshots/mac/pending.png)

[Complete commands and output](../../screenshots/pending.txt)
