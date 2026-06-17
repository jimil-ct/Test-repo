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

### Webhook Security Requirements

GitHub sends webhooks → CognitivTrust → Redpanda `raw.git` (when enabled on platform backend).

**CRITICAL:** The webhook receiver MUST validate GitHub's signature before processing any payload:

- **Required Header:** `X-Hub-Signature-256` must be present and valid
- **Validation:** HMAC-SHA256 signature computed using the shared webhook secret
- **Reject unsigned/invalid requests:** HTTP 401 or 403
- **Accept valid signatures:** HTTP 200

**Security Reference:** [GitHub Webhook Signature Validation](https://docs.github.com/webhooks/using-webhooks/validating-webhook-deliveries)

Without signature validation, attackers can forge webhook payloads to trigger unauthorized Brain API operations.

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
