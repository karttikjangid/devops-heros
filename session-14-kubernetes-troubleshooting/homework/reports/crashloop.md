# CrashLoopBackOff

Introduced this fault in `session14-lab` to practice finding and fixing it.

- Problem/root cause: The startup command printed an error and exited with code 1.
- Investigation: Checked Pod status, previous logs and restart events.
- Fix: Recreated the Pod with the working Nginx image/command.
- Verification: The replacement Pod became Ready.

![Recorded output in Mac zsh: Before and after output](../../screenshots/mac/crashloop.png)

[Complete commands and output](../../screenshots/crashloop.txt)
