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

**Secure Webhook Configuration (Local Development)**

Webhooks must hit your public CT API endpoint. **For local development only:**

1. **Recommended**: Use GitHub CLI webhook forwarding (secure, no public exposure):
   ```bash
   gh webhook forward --events=pull_request,pull_request_review --url=http://localhost:3000/webhooks/github
   ```

2. **If using ngrok**: You MUST configure security controls:
   - Use a **reserved domain** with basic authentication:
     ```bash
   - **Mandatory**: Configure `WEBHOOK_SECRET` env variable in your CognitivTrust application.
   - **Mandatory**: Validate GitHub webhook signatures (`x-hub-signature-256`) in your handler:
      - Validation MUST occur **BEFORE** any payload parsing or processing.
      - Use constant-time comparison `crypto.timingSafeEqual()` (Node.js) or `hmac.compare_digest()` (Python).
      - Reject requests with 401 if signature is missing, malformed, or invalid.
      - See implementation example: `docs/features/integrations/github.md`
      - **TEST REQUIRED**: Add integration test that sends forged webhook and verifies 401 response.
     ```
   - **Mandatory**: Configure `WEBHOOK_SECRET` env and validate GitHub webhook signatures (`x-hub-signature-256`) in your handler.
   - Restrict IP access to GitHub webhook ranges: `https://api.github.com/meta` (`hooks` field).

**NOTE: GitHub CLI `gh webhook forward` bypasses signature validation since the CLI authenticates to GitHub but localhost endpoint receives unsigned requests. Test with real GitHub webhooks (using ngrok + signature validation) before deploying.**

See your internal doc: `docs/features/integrations/github.md` for webhook signature validation implementation.

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
