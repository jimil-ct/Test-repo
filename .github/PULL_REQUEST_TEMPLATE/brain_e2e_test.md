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
*Important:**

- **Once the PR is saved, the `change_id` is immutable.** Brain API will reject attempts to modify it through subsequent `pull_request edited` webhooks.
- If you must change the `change_id`, close this PR and create a new one with the correct ID.
- **All PR description edits are audit-logged.** Brain API now processes `pull_request edited` events and logs all attempted `change_id` modifications.
- To detect tampering, Brain API periodically verifies stored PR URL against GitHub's current PR description.

**Security improvement:** The Brain API webhook handler now implements:
1. **`pull_request edited` event handling**: Detects and rejects `change_id` modifications after initial webhook by comparing payload to stored change record
2. **Server-side immutability enforcement**: Once `change_id` associated with a PR URL, subsequent edits cannot modify it
3. **Audit logging**: All `pull_request edited` events and `change_id` modification attempts are logged
4. **API-level validation**: Periodic verification against GitHub API to detect description tampering
If you must change the `change_id`, close this PR and create a new one with the correct ID.

GitHub sends webhooks → CognitivTrust → Redpanda `raw.git` (when enabled on platform backend).

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
