## Context Brain — E2E test PR (fixture repo)

### 1) Mint a `change_id` (run where `brain-api` Docker container exists)

```bash
docker exec brain-api python -c "from ulid import ULID; print(f'chg_{ULID()}')"
```

### 2) Paste this line in the PR description (replace with your minted id)

**SECURITY:** Only use valid ULID format (chg_ + 26 chars: 0-9, A-Z excluding I,L,O,U). Never paste untrusted data.

```html
<!-- change-id: chg_01ARZ3NDEKTSV4RRFFQ69G5FAV -->
```

Replace the example `chg_01ARZ3NDEKTSV4RRFFQ69G5FAV` with your minted ULID from step 1.

### 3) Save the description

GitHub sends webhooks → CognitivTrust → Redpanda `raw.git` (when `BRAIN_ENABLED=true` on platform backend).

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
