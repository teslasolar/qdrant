Deployment Checklist — Chazon Medical Imaging (collab/miracle)
=============================================================

This document walks through full deployment: backend to Railway, Qdrant Cloud configuration, updating the web UI, and running ingestion.

1) Deploy backend to Railway
--------------------------------
- Open a PowerShell terminal and change into the backend folder:

  ```powershell
  cd .\os\backend
  ```

- Login to Railway (follow prompts):

  ```powershell
  railway login
  railway init  # create a new project or link existing
  railway up    # starts a deployment and prints the deployed URL
  ```

- When `railway up` finishes note the public URL (e.g. `https://your-app.railway.app`).

2) Provision Qdrant (Cloud)
-----------------------------
- Sign up / log in: https://cloud.qdrant.io
- Create a new deployment (or use Railway Qdrant add-on). Copy the Qdrant endpoint URL (usually `https://<your-host>.qdrant.cloud`) and API key.

3) Update the frontend (`medical-viewer.html`)
----------------------------------------------
We modified the page to read `API_URL` at runtime. There are three ways to point the UI to your backend:

- Recommended (hosted): configure the host to inject a global variable `window.__API_URL__ = 'https://your-app.railway.app'` into the served HTML (some platforms support environment injection or templates).
- Quick test (URL-param): open the UI with `?api_url=https://your-app.railway.app`, e.g.: `https://<static-host>/medical-viewer.html?api_url=https://your-app.railway.app`
- Quick test (URL-param): open the UI with `?api_url=https://your-app.railway.app`, e.g.: `https://<static-host>/medical-viewer.html?api_url=https://your-app.railway.app`
- Vercel (static host): set the project root to `collab/miracle` when creating a Vercel project, then visit the deployed URL. Use `?api_url=` to point the UI to a backend, for example:

  `https://your-vercel-site.vercel.app/?api_url=https://your-backend.example.com`

  The repo includes a `vercel.json` and a root `index.html` that redirects to `medical-viewer.html` (preserving query parameters).
- Local dev (unchanged): default remains `http://localhost:8000`.

4) Run ingestion against the deployed Qdrant
-------------------------------------------
- On your machine (or a CI job), set `QDRANT_URL` and optionally `QDRANT_API_KEY`, then run the ingestion script. Example PowerShell command:

  ```powershell
  cd .\collab\miracle
  $env:QDRANT_URL = 'https://your-qdrant-cloud-url'
  $env:QDRANT_API_KEY = 'your-api-key-if-any'
  python ingest_medical_data.py
  ```

Notes:
- The ingestion script reads `QDRANT_URL` from the environment and will create the `medical_images` collection and upsert vectors.
- If you want to run ingestion from the Railway-hosted backend, add the Qdrant credentials in Railway project variables and run the ingestion inside the backend deployment or via a job.

5) Verify and open the UI
--------------------------
- Verify ingestion output printed success messages and that `verify_ingestion()` shows points_count > 0.
- Visit your hosted `medical-viewer.html` and configure it to point to your API via `window.__API_URL__` or `?api_url=`.

6) Git push
------------
- Commit and push your changes to GitHub:

  ```powershell
  git add collab/miracle/medical-viewer.html collab/miracle/DEPLOYMENT.md collab/miracle/index.html collab/miracle/vercel.json docker-compose.yml
  git commit -m "chore(medical): runtime API_URL, Vercel config, docker-compose and deployment docs"
  git push origin main
  ```

Helper tips
-----------
- If Railway provides a dashboard to set environment variables, add `QDRANT_URL` and `QDRANT_API_KEY` there so the backend can connect to Qdrant Cloud.
- If you host the UI as static files (GitHub Pages / Railway static), prefer injecting `window.__API_URL__` during build or using the query param for quick testing.

If you want, I can:
- Prepare a small snippet to inject `window.__API_URL__` in a static hosting scenario.
- Create a Railway-friendly `railway-vars.env` example for storing `QDRANT_URL`/`API_KEY`.
 - Prepare a small snippet to inject `window.__API_URL__` in a static hosting scenario.
 - Prepare a `docker-compose.yml` (provided) to run Qdrant + backend as a single stack (useful for VPS/docker hosts).
 - Help deploy the backend container to a VPS or cloud provider (Fly, DigitalOcean App Platform) using this `docker-compose.yml`.

