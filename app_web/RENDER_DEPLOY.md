# Deploying IOTinel to Render (Free Plan)

## What gets deployed

| Render Service | Type | Source |
|---|---|---|
| `iotinel-db` | PostgreSQL (free) | managed |
| `iotinel-auth` | Web Service (Docker) | `backend/Dockerfile.auth` |
| `iotinel-detection` | Web Service (Docker) | `backend/Dockerfile.detection` |
| `iotinel-training` | Web Service (Docker) | `backend/Dockerfile.training` |
| `iotinel-monitoring` | Web Service (Docker) | `backend/Dockerfile.monitoring` |
| `iotinel-dashboard` | Web Service (Docker) | `backend/Dockerfile.dashboard` |
| `iotinel-admin` | Web Service (Docker) | `backend/Dockerfile.admin` |
| `iotinel-gateway` | Web Service (Docker) | `backend/Dockerfile.gateway` |
| `iotinel-analyst-ui` | Static Site | `frontend/analyst` |
| `iotinel-scientist-ui` | Static Site | `frontend/scientist` |
| `iotinel-admin-ui` | Static Site | `frontend/admin` |

---

## Free Plan Limitations to Know

- **Services spin down after 15 minutes of inactivity** — first request after sleep takes ~30s.
- **PostgreSQL free tier expires after 90 days** — you'll need to recreate it.
- **Ephemeral filesystem** — MLflow runs and trained models stored in `/tmp` are lost on restart. Training works but history won't persist across deploys.
- **No persistent disk on free plan** — the MLOPS models/datasets from your local volume mounts are not available. Detection and training will return errors until you either bundle models into the image or upgrade to a paid plan with a Disk.

---

## Step-by-Step Deployment

### 1. Push your code to GitHub

Make sure `app_web/render.yaml` and all the new `Dockerfile.*` files are committed and pushed.

```bash
git add app_web/render.yaml app_web/backend/Dockerfile.* app_web/backend/shared/config.py
git commit -m "chore: add Render deployment config"
git push
```

### 2. Create a new Blueprint on Render

1. Go to [https://dashboard.render.com/blueprints](https://dashboard.render.com/blueprints)
2. Click **New Blueprint Instance**
3. Connect your GitHub repo
4. Set the **Root Directory** to `app_web`
5. Render will detect `render.yaml` automatically
6. Click **Apply** — this creates all 11 services at once

### 3. Wait for the first deploy

The first build takes 5–10 minutes per service (Docker builds are slow on free tier).
Watch the logs for each service. The order that matters:
- `iotinel-db` must be ready first (auto-handled)
- `iotinel-auth` must be up before other backend services can authenticate

### 4. Set the remaining environment variables

After all services are deployed, go to each service in the Render dashboard and fill in the blank `value: ""` env vars.

#### On `iotinel-gateway`:
| Key | Value |
|---|---|
| `ANALYST_UI_URL` | `https://iotinel-analyst-ui.onrender.com` |
| `SCIENTIST_UI_URL` | `https://iotinel-scientist-ui.onrender.com` |
| `ADMIN_UI_URL` | `https://iotinel-admin-ui.onrender.com` |
| `ALLOWED_ORIGINS` | `https://iotinel-analyst-ui.onrender.com,https://iotinel-scientist-ui.onrender.com,https://iotinel-admin-ui.onrender.com` |

#### On ALL backend services (auth, detection, training, monitoring, dashboard, admin, gateway):
| Key | Value |
|---|---|
| `ALLOWED_ORIGINS` | `https://iotinel-analyst-ui.onrender.com,https://iotinel-scientist-ui.onrender.com,https://iotinel-admin-ui.onrender.com` |

#### On ALL three frontend static sites (analyst-ui, scientist-ui, admin-ui):
| Key | Value |
|---|---|
| `VITE_API_URL` | `https://iotinel-gateway.onrender.com` |

> **Note:** After setting env vars on static sites, trigger a manual redeploy so Vite picks them up at build time.

### 5. Verify the deployment

Hit these URLs to confirm services are up:

```
https://iotinel-gateway.onrender.com/health
https://iotinel-auth.onrender.com/health
https://iotinel-detection.onrender.com/health
https://iotinel-training.onrender.com/health
https://iotinel-monitoring.onrender.com/health
https://iotinel-dashboard.onrender.com/health
https://iotinel-admin.onrender.com/health
```

Then open the frontends:
```
https://iotinel-analyst-ui.onrender.com
https://iotinel-scientist-ui.onrender.com
https://iotinel-admin-ui.onrender.com
```

Default login credentials (seeded on first startup):
| Email | Password | Role |
|---|---|---|
| `analyst@hexamind.local` | `analyst123` | security_analyst |
| `scientist@hexamind.local` | `scientist123` | data_scientist |
| `admin@hexamind.local` | `admin123` | administrator |

---

## Known Limitations on Free Plan

### ML Detection & Training won't work out of the box

The detection and training services depend on the MLOPS pipeline (`model_pipeline.py`) and dataset files that live outside `app_web/` in your local repo. These are not included in the Docker build context.

**Options:**
1. **Demo mode only** — auth, dashboard, admin, and monitoring work fine. Detection returns errors for predict/batch calls.
2. **Bundle models** — copy pre-trained `.joblib` model files into `app_web/backend/` and adjust `MLOPS_DIR` in `config.py` to point to them.
3. **Upgrade to paid** — add a Render Disk and mount your MLOPS directory.

### Elasticsearch / Kibana

The ELK stack is in a separate repo and not deployed here. The `elk_client.py` will silently fail (logs the error, doesn't crash the service) when `ELASTICSEARCH_URL` is empty, so all services still work — you just won't have log aggregation.

### Redis

Not used for critical functionality (only referenced in config). Safe to leave empty on free plan.

---

## Updating After Deploy

To redeploy after code changes:
1. Push to GitHub — Render auto-deploys on push if auto-deploy is enabled
2. Or go to the service in Render dashboard → **Manual Deploy** → **Deploy latest commit**
