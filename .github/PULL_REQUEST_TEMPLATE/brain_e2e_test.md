## Context Brain — E2E test PR (fixture repo)

### 1) Mint a `change_id` (run where `brain-api` Docker container exists)

```bash
**IMPORTANT:** Each `change_id` must be unique. If multiple PRs use the same ID, it causes state corruption.

 **Step 1.1:** First check for existing IDs:
```bash
curl -H "Authorization: Bearer $JWT_TOKEN" ${BRAIN_API_URL}/v1/changes?limit=100
```

 **Step 1.2:** Generate a new unique ID:
docker exec brain-api python -c "from ulid import ULID; print(f'chg_{ULID()}')"
```

### 2) Paste this line in the PR description (replace with your minted id)

```html
<!-- change-id: chg_PASTE_YOUR_ULID_HERE -->
```

**Note:** If you get a conflict error, generate a new `change_id` and try again.


### 3) Save the description

GitHub sends webhooks → CognitivTrust → Redpanda `raw.git` (when `BRAIN_ENABLED=true` on platform backend).

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
