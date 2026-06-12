## Context Brain — E2E test PR (fixture repo)

**WARNING: `change_id` MUST be unique across all PRs.** Clone or duplicate ids cause data corruption and state inconsistencies in the Brain API.

**When re-using this template:**
 1. Generate a fresh `change_id` each time
 2. Never re-use an id from a previous PR
 3. If you notice a duplicate `change_id` after creating a PR, close the PR and create a new one

---

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

GitHub sends webhooks → CognitivTrust → Redpanda `raw.git` (when `BRAIN_ENABLED=true` on platform backend).

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
