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

**Security Note**: The Redpanda message queue flow requires:
- SASL authentication enabled
- TLS encryption for all broker connections
- Topic ACLs configured:
  - `raw.git` topic: CTBackend (write-only), Brain API (read-only)
- Network segmentation to prevent unauthorized broker access
- Regular audit of topic permissions and access logs

Verify these security controls are properly configured before testing.

GitHub sends webhooks → CognitivTrust → Redpanda `raw.git` (when `BRAIN_ENABLED=true` on platform backend).

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
