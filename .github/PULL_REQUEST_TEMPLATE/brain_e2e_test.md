## Context Brain — E2E test PR (fixture repo)
### 1) Mint a `change_id` (generated automatically by Brain API)
### 1) Mint a `change_id` (run where `brain-api` Docker container exists)
**NOTE:** The Brain API automatically generates a secure, unique `change_id` when it receives the initial `pull_request` webhook event from GitHub. The generated `change_id` is bound to the PR URL, repository, and GitHub installation ID to ensure integrity and prevent collision attacks.
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

You can query the Brain API to retrieve the `change_id` that was automatically generated.
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
