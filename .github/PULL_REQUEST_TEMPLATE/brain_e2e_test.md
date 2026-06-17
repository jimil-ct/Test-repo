## Context Brain — E2E test PR (fixture repo)

### 1) Get your `change_id`

**IMPORTANT: The Brain API automatically generates a unique `change_id` server-side when it receives the initial PR webhook event.**

You can retrieve the generated `change_id` after creating the PR by calling the Brain API:

```bash
curl -X GET "https://{brain-api}/v1/changes?pr_url={PRS_GITHUB_URL}" \
  -H "Authorization: Bearer {your_jwt_token}"
```

The response will include the server-generated `change_id` (starts with `chg_`) tied to this PR and repository.

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
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
