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

GitHub sends webhooks ₒ CognitivTrust ₒ Redpanda `raw.git` (when enabled on platform backend).

**SECURITY: Webhook Signature Validation Required**

The CognitivTrust webhook receiver **must validate** the `X-Hub-Signature-256` header on all incoming GitHub webhooks to prevent forged event injection.

Validation process:
1. Extract the `X-Hub-Signature-256` header from the incoming request
2. Compute HMAC-SHA256 of the raw request body using the configured webhook secret
3. Compare the computed signature with the header value using constant-time comparison
4. Reject requests with missing, invalid, or mismatched signatures (HTTP 401/403) before parsing the payload

Reference: https://docs.github.com/webhooks/using-webhooks/validating-webhook-deliveries

The webhook secret must be stored securely (environment variable or secrets manager) and rotated periodically.

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.

### 5) Test Webhook Signature Validation

To verify that signature validation is working correctly:

**Test 1. Rejection of unsigned requests:**
Send a POST request to the webhook endpoint without the `X-Hub-Signature-256` header. The server must respond with HTTP 401 or 403.

**Test 2. Rejection of invalidly signed requests:**
Send a POST request with an incorrect `X-Hub-Signature-256` header (e.g., `sha256=invalidhash`). The server must respond with HTTP 401 or 403.

**Test 3. Acceptance of correctly signed requests:**
Send a POST request with a valid `X-Hub-Signature-256` header (use the same secret configured in GitHub webhook settings). The server must respond with HTTP 200 and process the payload.
