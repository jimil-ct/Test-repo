## Context Brain — E2E test PR (fixture repo)

### 1) Mint a `change_id` (run where `brain-api` Docker container exists)

```bash
docker exec brain-api python -c "from ulid import ULID; print(f'chg_{ULID()}')"
```

### 2) Paste this line in the PR description (replace with your minted id)

```html
<!-- change-id: chg_PASTE_YOUR_ULID_HERE -->
```

### 3) Ensure GitHub webhook secret is configured

Before saving the PR description, verify that your GitHub repository webhook is configured with a secret token:

1. Go to GitHub repo Settings → Webhooks → select the CognitiveTrust webhook
2. Verify that the *Secret* field is populated (at least 20 random bytes)
3. If missing, generate a secure webhook secret and configure it both in GitHub and CognitiveTrust webhook receiver

```bash
# Generate a secure webhook secret (example)
openssl rand -base64 32
```

The webhook receiver **must** validate `X-Hub-Signature-256` on every incoming request using HMAC-SHA256 and constant-time comparison. Reject unsigned or incorrectly signed requests with HTTP 401/403.

Reference: https://docs.github.com/webhooks/using-webhooks/validating-webhook-deliveries

### 4) Save the description

**WARNING: Do not edit PR description after saving.** Editing the description after initial webhook delivery creates inconsistent state between GitHub and Brain API. The Brain API currently does not handle `pull_request edited` webhooks.

If you must change the `change_id`, close this PR and create a new one with the correct ID.

GitHub sends webhooks → CognitivTrust → Redpanda `raw.git` (when enabled on platform backend).

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)
### 5) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)
- `GET {brain-api}/v1/changes?limit=30`
***.1) Functional verification**

- `GET {brain-api}/v1/changes?limit=30`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`


***.2) Rate limiting verification**

Verify API Gateway rate limits are enforced before deployment:

**Expected rate limits per endpoint tier** (per JWT `subject`/`org_id`, NOT per IP):
- `GET /v1/changes`: 100 req/min
- `POST /v1/query`: 10 req/min
- `GET /v1/changes/{id}/graph`: 5 req/min

**Test procedure**:
1. Send burst request exceeding endpoint limit (e.g., 15 `POST /v1/query` requests in 60 seconds)
2. Verify endpoint returns `HTTP 429 Too Many Requests`
3. Verify response includes `Retry-After` header with wait time in seconds
4. **Verify rate limit scope and cross-tenant isolation**:
   - Obtain JWT_A (org_id=A, subject=user_A) and JWT_B (org_id=B, subject=user_B)
   - Send burst with JWT_A to exhaust quota for org A (e.g., 15 `POST /v1/query` in 60s)
   - Verify org A receives `HTTP 429`
   - **Immediately** send request with JWT_B to same endpoint
   - **MUST succeed with HTTP 200/201** — org B quota must be isolated from org A consumption
5. Verify rate limit state is shared across API Gateway replicas (Redis/memcached, not in-memory)
6. Cross-reference API Gateway configuration in production IaC/K8s manifests to confirm limits match test expectations

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
