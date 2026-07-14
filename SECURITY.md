# Security Policy

## Supported versions

Security fixes are applied to the current `main` branch and the latest published release candidate or stable release.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting or a private security advisory for this repository when available. Do not include credentials, access tokens, private keys, production data, or other secrets in a public issue.

For non-sensitive defects, open a normal GitHub issue with reproduction steps and affected versions.

## Security boundaries

The installer is dry-run by default and must not:

- modify `config.toml`;
- enable experimental features;
- access the network;
- modify business repositories;
- create commits, branches, pull requests, deployments, or external notifications.

Report any behavior that violates these boundaries as a security issue.
