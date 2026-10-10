# Service connectivity / mini project

Introduced this fault in `session14-lab` to practice finding and fixing it.

- Problem/root cause: The Service had both a wrong selector and a wrong target port.
- Investigation: Describe and EndpointSlices showed no matching backend; after fixing the selector, HTTP still failed on port 9999.
- Fix: Matched app=web, then changed targetPort to 8080.
- Verification: The client received the Nginx page through the Service.

![Before and after output](../../screenshots/service-mini-project.png)

[Complete commands and output](../../screenshots/service-mini-project.txt)
