# Lifecycle

The supervisor defines a bounded task. A worker appends `started`, executes
only approved scope, and appends one terminal event. The supervisor alone
appends `reviewed`. Worker events never decide.

Use `python tools/agent_ledger.py` for every append. Do not patch or rewrite
JSONL history. On helper, lock, schema, privacy, or write-conflict failure,
stop and preserve evidence.
