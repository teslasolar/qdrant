# Deploying the Backend to Render (quick guide)

This document explains how to create a Render web service for the backend and how to configure GitHub to trigger Render deploys automatically.

Steps on Render (GUI)
1. Sign in to https://render.com and connect your GitHub account.
2. Click **New** → **Web Service**.
3. Select the `teslasolar/qdrant` repository and the branch `feature/medical-vercel-docker` (or `main`).
4. For **Environment**, choose **Docker** (Render will use the repository Dockerfile at `os/backend/Dockerfile`).
5. Set the **Name** (e.g. `qdrant-backend`) and **Instance Type** (free/standard).
6. Set **Health Check Path** to `/health` and **Internal Port** to `8000`.
7. Add required Environment variables (see below).
8. Create the service and wait for the first deploy to complete. The service URL will be shown in Render dashboard (e.g. `https://qdrant-backend.onrender.com`).

Environment variables to add on Render
- `QDRANT_URL` — URL of your Qdrant instance (must be reachable from Render). For Qdrant Cloud, use the cloud URL.
- `QDRANT_API_KEY` — if required by your Qdrant instance.
- `COHERE_API_KEY`, `OPENAI_API_KEY` — optional, only if you use those embedding providers.
- Any other env variable referenced by `os/backend` code.

Triggering deploys from GitHub Actions
- Create two repository secrets in GitHub: `RENDER_SERVICE_ID` and `RENDER_API_KEY`.
  - `RENDER_SERVICE_ID`: the Render service id for your web service (visible in the service settings or URL; looks like `srv-xxxxx`).
  - `RENDER_API_KEY`: a Render API key with permissions to create deploys (create at https://dashboard.render.com/account/api-keys).
- Once those secrets are set, the workflow `.github/workflows/deploy-to-render.yml` will call the Render API to trigger a deploy after pushes to `feature/medical-vercel-docker` or when manually dispatched.

How to find `RENDER_SERVICE_ID`
- In the Render dashboard open the service and look at the URL or the service settings. The service id (e.g. `srv-abc123`) is visible in the URL or via Render's API list services endpoint.

How to create a Render API key
1. Go to https://dashboard.render.com/account/api-keys
2. Click **Generate Key** (note the key now — you can't view it again).
3. Save the key as the GitHub repository secret `RENDER_API_KEY`.

Manual test of Render deploy (optional)
1. From a shell with the Render API key available:

```bash
curl -X POST \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -H "Content-Type: application/json" \
  "https://api.render.com/v1/services/${RENDER_SERVICE_ID}/deploys" \
  -d '{}'
```

Notes
- The GitHub workflow will not try to deploy if `RENDER_SERVICE_ID` or `RENDER_API_KEY` are missing. Add them as repository secrets to enable automatic deploys.
- Ensure your backend can reach the Qdrant instance (use Qdrant Cloud or a publicly reachable endpoint).
