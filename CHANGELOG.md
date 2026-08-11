# Changelog

All notable changes to Daedalus are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and released versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Standalone Plugin packaging with an explicit runtime allowlist and installed-payload self-test.
- Living SDD and seven-stage FRAME／MODEL／BIND／PROVE／BUILD／RECONCILE／SEAL workflow.
- Deterministic necessary-UML routing with Mermaid required for all decision and reader-aid diagrams.
- Mandatory repository-root `CHANGELOG.md` planning and `[Unreleased]` evidence for every Daedalus-managed production change.

### Changed

- SDD templates, schema, validator, examples, and tests now keep requirements, TDD evidence, design reconciliation, and changelog impact in one traceable workflow.
- Public installation and verification no longer depend on another custom Skill or local development repository.

## [1.0.1] - 2026-08-11

### Fixed

- Repaired public installation by replacing author-local instructions with the GitHub marketplace commands.
- Added a root marketplace whose `daedalus` selector resolves the root `daedalus` Plugin.
- Restricted the formal runtime payload to the Plugin manifest, license, and Skill files, with a bundled standalone scaffold／validator self-test.
- Removed author-machine installation dependencies from current public documentation.

## [1.0.0] - 2026-08-11

### Added

- Initial public Daedalus Plugin and risk-tiered SDD／TDD workflow.

[Unreleased]: https://github.com/timshan/daedalus/compare/v1.0.0...HEAD
[1.0.1]: https://github.com/timshan/daedalus/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/timshan/daedalus/releases/tag/v1.0.0
