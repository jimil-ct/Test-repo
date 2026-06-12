## Context Brain — E2E test PR (fixture repo)

**SECURITY NOTICE**: This Brain API processes code changes for AI/ML analysis. Ensure all inputs are properly sanitized and validated before processing. Monitor for adversarial inputs and potential model poisoning attacks. Human validation should be required for suspicious patterns or anomalous code submissions.

### Security Requirements
- Input sanitization must be enabled on Brain API endpoints
- Adversarial input detection should be active
- Model drift monitoring should be in place
- Suspicious code patterns require human review before processing

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
