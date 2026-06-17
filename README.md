# brain-github-e2e-repo

**Tiny GitHub-only fixture** for testing **CognitivTrust → webhooks → `raw.git` → Brain extractors → Neo4j → graph** end-to-end.

This is **not** the CognitivTrust platform repo. Use it as a **separate** GitHub repository so you can install the CT GitHub App on **only** this repo and open PRs without touching production code.

---

## 1. Create the GitHub repo (empty)

1. GitHub → **New repository** (e.g. under `jimil-ct`): name **`brain-github-e2e`** (or any name).
2. **Do not** add README/license on GitHub (keeps `main` empty for first push), **or** if GitHub created `README.md`, use the “push existing repo” flow below with `--force` only if you intend to replace (usually avoid force on shared repos).

---

## 2. Push this folder as the only history

From your machine (path = this folder’s parent + folder name):

```bash
cd brain-github-e2e-repo
git init -b main
git add .
git commit -m "chore: Brain E2E fixture repo (PR template + noop files)"
git remote add origin https://github.com/<YOUR_USER_OR_ORG>/<YOUR_REPO_NAME>.git
git push -u origin main
```

Use **SSH** if you prefer: `git@github.com:<USER>/<REPO>.git`

---

## 3. Connect CognitivTrust GitHub App to **this** repo only

In the CognitivTrust app: **Settings → Integrations → GitHub** → ensure this new repository is **selected** for the installation (or add it in GitHub App **repository access**).

### Webhook Configuration (Development)

**⚠️ SECURITY NOTICE:** Webhooks carry sensitive GitHub data and must be protected even in development.

**Recommended (secure):** Use GitHub CLI webhook forwarding with automatic signature validation:
```bash
gh webhook forward --events=pull_request,pull_request_review --url=http://localhost:3000/api/webhooks/github
```

**Alternative (ngrok):** If using ngrok, **MUST** use reserved domain with authentication and IP allowlisting:
```bash
# 1. Reserve domain: https://dashboard.ngrok.com/cloud-edge/domains
# 2. Configure webhook signature validation (WEBHOOK_SECRET env var required)
# 3. Start tunnel with access control:
ngrok http 3000 --domain=your-reserved.ngrok.app --basic-auth="user:$(openssl rand -base64 32)"
# 4. Configure GitHub webhook with signature secret and IP allowlist (https://api.github.com/meta hooks field)
```

**🚫 NEVER use ngrok for production/staging environments.** See internal doc: `docs/features/integrations/github.md`.

---

## 4. Open a PR using the Brain E2E template

1. Create branch: `git checkout -b test/brain-e2e-1` → edit `VERSION.txt` (bump patch) → commit → push.
2. On GitHub: **Compare & pull request**.
3. Add **`?template=brain_e2e_test.md`** to the PR URL **or** copy text from `.github/PULL_REQUEST_TEMPLATE/brain_e2e_test.md`.
4. **Mint** a change id:

   ```bash
    # Generate a unique change ID using your preferred method (e.g., ULID generator, UUID, or API endpoint)
    # Example: chg_01HJ9A5ZF6856W3GK4PDVVDJS3
   ```

5. Paste into the PR description:

   `<!-- change-id: chg_YOUR_ULID_HERE -->`

6. Save → confirm GitHub **webhook 200** → wait ~30s → Brain:

   - `GET /v1/changes?limit=20`
   - `POST /v1/query` with `change_id` filter
   - `GET /v1/changes/{id}/graph`
   - UI: `/brain/graph` with same id

---

## What’s in this repo

| Path | Purpose |
|------|--------|
| `VERSION.txt` | Trivial bump for each test PR. |
| `src/hello.txt` | Second trivial file (optional edits in PRs). |
| `.github/PULL_REQUEST_TEMPLATE/brain_e2e_test.md` | Instructions + `change-id` marker steps. |

For a longer API checklist, copy from the platform repo if you have it: `brain/docs/E2E_BRAIN_API_AND_GRAPH.md` (optional; not required for this fixture to work).
