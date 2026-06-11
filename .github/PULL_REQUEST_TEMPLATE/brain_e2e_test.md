## Context Brain — E2E test PR (fixture repo)

### 1) Mint a `change_id` (run where `brain-api` Docker container exists)

```bash
docker exec brain-api python -c "from ulid import ULID; print(f'chg_{ULID()}')"
```

### 2) Paste this line in the PR description (replace with your minted id)

```html
<!-- change-id: chg_PASTE_YOUR_ULID_HERE -->
```

> **WARNING:** Do not edit this PR description after saving, as it may create inconsistent state
> between GitHub and Brain API. If you must edit, consider:
> 1. Delete the existing `change-id` from the description
> 2. Mint a new `change_id` following step 1 above
> 3. Add the new `change-id` to the description
> 4. Verify the new state in Brain (step 4)

### 3) Save the description

GitHub sends webhooks → CognitivTrust → Redpanda `raw.git` (when `BRAIN_ENABLED=true` on platform backend).

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
