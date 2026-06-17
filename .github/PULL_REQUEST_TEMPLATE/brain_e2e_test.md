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

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`

### 5) Verify Rate Limiting Enforcement

**Expected Rate Limits (per JWT subject/org_id, shared across API Gateway replicas via Redis):**

- `GET /v1/changes`: 100 req/min
- `POST /v1/query`: 10 req/min
- `GET /v1/changes/{id}/graph`: 5 req/min

**Test Procedure:**

1. Send burst exceeding the limit for each endpoint tier:
   ```bash
   # Example: Exceed GET /v1/changes limit
   for i in {1..105}; do curl -H "Authorization: Bearer $JWT" {brain-api}/v1/changes?limit=1; done
   ```
2. Verify HTTP 429 response with `Retry-After` header on requests exceeding limit.
3. Confirm rate limit scope is per JWT subject/org_id (not per IP):
   - Use same JWT from different IPs → same rate limit bucket
   - Use different JWTs (different org_id) → independent rate limit buckets
4. Verify rate limit state is shared across API Gateway replicas (Redis-backed, not in-memory).
5. Cross-reference production API Gateway configuration to confirm documented limits match deployed rules.

- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
