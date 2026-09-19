# Changelog

All notable changes to this project are documented in this file.

The project follows Semantic Versioning for public release snapshots. Gateway
policy helpers and supplied evidence remain advisory until an operator adopts
them in a reviewed promotion workflow.

## [0.2.0] - Unreleased

### Added

- Offline policy helpers for route ownership and authorization, configuration
  provenance and schema contracts, upstream capacity and certificate identity,
  data-plane freshness and convergence, and protected plugin changes.
- Gateway controls for credential rotation and revocation, JWKS rotation,
  sensitive-header redaction, client mTLS, Admin API exposure, break-glass
  access, audit retention, and control-plane backup evidence.
- Promotion checks for decK diff risk, destructive changes, route shadowing,
  path canonicalization, request schema and size limits, retry and idempotency
  safety, and distributed rate-limit consistency.
- Unit coverage for the gateway CLI, container-readiness behavior, policy
  helpers, and automation safety controls.

### Changed

- The gateway CLI now has a side-effect-free dry-run plan and treats stopped
  candidate containers as failed readiness states.
- The `check-plugin-change` command validates approval evidence for protected
  plugin changes and returns a machine-usable exit status.
- Daily portfolio automation validates generated destinations, performs
  validation in an isolated worktree, and requires the Python check before an
  eligible daily pull request can merge.
- GitHub Actions dependencies were upgraded to their Node 24-compatible major
  versions.

### Security

- Generated destinations reject traversal and Git-control paths before files
  are read or written.
- Gateway evidence can be bound to an approved workspace, promotion identity,
  and configuration digest.
- Default validation is offline and does not require gateway credentials or a
  live Kong control plane.

### Compatibility

- Python 3.10 or newer remains required.
- Existing `switch` and `scripts/switch-upstream.sh` entry points remain
  supported; `check-plugin-change` is additive.
- No state, data, or declarative-configuration migration is performed by this
  release.

[0.2.0]: https://github.com/AliZahiri/kong-deck-compose-gateway/compare/v0.1.0...v0.2.0
