#!/usr/bin/env bash
set -euo pipefail
URL="${URL:-http://homework.local/api/tasks}"
WORKERS="${WORKERS:-8}"
REQUESTS="${REQUESTS:-200}"
pids=()
for ((worker=0; worker<WORKERS; worker++)); do
  (
    for ((request=0; request<REQUESTS; request++)); do
      curl --fail --silent --show-error --max-time 10 "$URL" > /dev/null
    done
  ) &
  pids+=("$!")
done
for pid in "${pids[@]}"; do wait "$pid"; done
echo "Completed $((WORKERS * REQUESTS)) successful requests to $URL"
