# Project Context

## Project

Balitrip website.

## Infrastructure

Production environment runs on Proxmox VE.

## Server layout

- Production web container: `CT140`
- Role: `web`
- IP: `192.168.8.140`

## Network standard

- Network: `192.168.8.0/24`
- Gateway: `192.168.8.1`
- Rule: last IP octet = container ID

## Relevant containers

- `CT101` — gateway — `192.168.8.101`
- `CT102` — dns — `192.168.8.102`
- `CT140` — web — `192.168.8.140`
- `CT150` — backup — `192.168.8.150`

## Repository role

This repository is the source of truth for the Balitrip website.

## Deployment model

- `main` = production
- `develop` = integration
- deploy target = `CT140`

## Notes for AI

- Do not assume direct editing on the production server
- GitHub is the source of truth
- Prefer branch → PR → merge workflow
- Keep website structure clean and predictable
