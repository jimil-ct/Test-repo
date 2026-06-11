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

GitHub sends webhooks → CognitivTrust → Redpanda `raw.git` (when `BRAIN_ENABLED=true` on platform backend).

**Security Note**: Redpanda must be configured with:

- **SASL Authentication**: Enable SCRAM-SHA-256 or SCRAM-SHA-512
- **TLS Encryption**: Enable TLS 1.2 or higher for all client connections
- **Topic ACLs**: Restrict `raw.git` topic access:
  - CTBackend: write-only permissions
  - Brain API: read-only permissions
- **Network Segmentation**: Redpanda brokers must only be accessible from authorized services

Unauthorized access to Redpanda can result in data tampering, unauthorized message injection, or consumption of sensitive repository data.

### 4) Verify in Brain (JWT `org_id` = CT org tied to this GitHub installation)

- `GET {brain-api}/v1/changes?limit=30`
- `POST {brain-api}/v1/query` — structured filter `change_id`
- `GET {brain-api}/v1/changes/{id}/graph`
- UI: Brain → Graph, same `chg_…`

---

**This repository** exists only to generate safe PR/push traffic for Brain testing.
