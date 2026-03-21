# AI Development Rules

## Branch workflow
- Never commit directly to main
- Work from develop or agent/* branches
- All changes go through pull requests

## Safety
- Do not change deployment without approval
- Do not change infrastructure without approval
- Do not delete files without explanation
- Keep changes small and reviewable

## Project structure
- site/ — website pages
- assets/ — images and media
- css/ — styles
- js/ — scripts
- docs/ — documentation
- infra/nginx/ — nginx configuration

## Branch naming
- develop
- agent/*
- feature/*
- hotfix/*
