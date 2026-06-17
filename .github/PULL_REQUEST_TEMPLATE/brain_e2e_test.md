## Context Brain — E2E test PR (fixture repo)

### 1) Mint a `change_id` (run where `brain-api` Docker container exists)

```bash
docker exec brain-api python -c "from ulid import ULID; print(f'chg_{ULID()}')"
```

### 2) Paste this line in the PR description (replace with your minted id)

```html
<!-- change-id: chg_PASTE_YOUR_ULID_HERE -->
```

### 3) Save the description

**WARNING: Do not edit PR description after saving.** Editing the description after initial webhook delivery creates inconsistent state between GitHub and Brain API. The Brain API currently does not handle `pull_request edited` webhooks.

If you must change the `change_id`, close this PR and create a new one with the correct ID.

GitHub sends webhooks → CognitivTrust → Redpanda `raw.git` (when enabled on platform backend).

**Security Note:** The CognitivTrust webhook receiver **must** validate GitHub webhook signatures using HMAC-SHA256 verification of the `X-Hub-Signature-256` header against the configured webhook secret. Failure to validate signatures allows attackers to forge malicious webhook payloads, inject arbitrary `change_id` values, or manipulate Brain API state.

**Implementation Requirements:**
```
Receiver must: extract X-Hub-Signature-256 from request header, compute HMAC-SHA256 of raw request body using webhook secret, compare using constant-time comparison, reject invalid/missing signatures before parsing. Store secret securely (env/secrets manager) and log validation failures.
```

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
