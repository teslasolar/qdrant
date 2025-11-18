Deployment CI guide for collab/miracle

This file explains how the repository CI will deploy the frontend and backend using GitHub Actions.

What I added
- `.github/workflows/deploy-frontend-pages.yml`: uploads `collab/miracle` folder as a Pages artifact and deploys it to GitHub Pages on push to `main` (or manual dispatch).
- `.github/workflows/build-and-push-backend.yml`: builds the backend Docker image (context `os/backend`) and pushes it to GitHub Container Registry as `ghcr.io/<owner>/qdrant-backend:<sha>`. It includes an optional SSH deploy step that runs if the SSH secrets are set.

How to trigger
- Push your changes to the `main` branch or the `feature/medical-vercel-docker` branch (both are enabled), or run the workflows manually from the Actions tab.

Required repository secrets (optional/for full automation)
- `SSH_HOST` - optional: remote host address for SSH deploy (e.g., `1.2.3.4`).
- `SSH_USER` - optional: SSH username.
- `SSH_PRIVATE_KEY` - optional: private key (PEM) for SSH; no passphrase recommended for automation.

Notes and recommended next steps
- The frontend will be served by GitHub Pages. After the first successful run, the Pages URL is available in the repository Settings -> Pages.
- The backend image is pushed to GHCR. To run it publicly you have several options:
  1. Provide SSH deploy secrets above and the workflow will pull and run the image on your VPS.
  2. Use a managed service (Render, Fly, DigitalOcean App Platform). I can add a workflow for one of those if you provide an API key or choose a provider.
  3. Run the image manually on any host that can access GHCR (login required with a PAT or using `docker login ghcr.io -u USER -p TOKEN`).

If you want me to complete the full deployment now, tell me which of these you prefer:
- Provide VPS SSH details (host, user, and private key) so I can finish automatic deploy to that host. The backend workflow is already configured to perform an SSH pull/start when `SSH_HOST`, `SSH_USER`, and `SSH_PRIVATE_KEY` are set in repo Secrets.
- Provide a managed platform choice (Render/Fly/DO) and a corresponding API key and I will add the provider-specific workflow and finish deployment.
- Or I can run the final steps locally and give you the public endpoints (requires a machine with public IP and open ports).

If you prefer, I can also add a status workflow to report the deployed frontend URL and the GHCR image tag when the workflows succeed.

Repository Pages configuration note
- The `deploy-frontend-pages.yml` workflow uses the Pages deployment action and will publish the contents of `collab/miracle`. Ensure the repository's Pages settings (Settings -> Pages) are set to use "GitHub Actions" as the source (the workflow will take care of publishing; GitHub will show the site URL once the first workflow succeeds).

Frontend runtime API configuration
- The frontend (`collab/miracle/medical-viewer.html`) supports runtime API configuration via `?api_url=` query string and `window.__API_URL__`. After the Pages deployment, visit the published URL with `?api_url=https://<your-backend>` to point the UI to the deployed backend.
