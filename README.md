# Balitrip Site

Production repository for the Balitrip website.

## Branches

- `main` — production
- `develop` — integration / staging
- `agent/*` — AI changes
- `feature/*` — manual changes
- `hotfix/*` — urgent fixes

## Workflow

- Never commit directly to `main`
- AI changes go to `agent/*`
- `agent/*` branches merge into `develop`
- `develop` merges into `main` by pull request
- `main` is the production source of truth

## Structure

- `site/` — website pages
- `assets/` — images and media
- `css/` — styles
- `js/` — scripts
- `docs/` — documentation
- `infra/nginx/` — nginx configuration
- `.github/workflows/` — GitHub automation
