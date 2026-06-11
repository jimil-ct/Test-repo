## Context Brain — E2E test PR (fixture repo)

### 1) Add change tracking to PR description

Note: `change_id` is automatically generated server-side when the webhook is processed.
```html
<!-- change-id: auto -->
```

### 2) Save the description

GitHub sends webhooks → CognitivTrust → Redpanda `raw.git` (when `BRAIN_ENABLED=true` on platform backend).

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id` (use server-generated ID from step 1 response)
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, look for the auto-generated `chg_…` ID

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
