# AI Development Rules

## Main workflow

- Never commit directly to `main`
- Never commit directly to `develop`
- Create changes in `agent/*` branches
- Merge `agent/*` into `develop`
- Merge `develop` into `main` by pull request

## Safety

- Do not change deployment without explicit approval
- Do not change infrastructure without explicit approval
- Do not delete files without explanation
- Keep changes small and reviewable
- Prefer one logical change per pull request

## Project structure

- `site/` — website pages
- `assets/` — images and media
- `css/` — styles
- `js/` — scripts
- `docs/` — documentation
- `infra/nginx/` — nginx configuration
- `.github/workflows/` — GitHub automation

## Branch naming

- `agent/*`
- `feature/*`
- `hotfix/*`

## Pull request rules

- Agent PRs go to `develop`
- Production PRs go from `develop` to `main`
- Human approval is required before important production changes
