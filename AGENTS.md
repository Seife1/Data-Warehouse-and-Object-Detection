# Enterprise Engineering & Versioning Rules

You must strictly adhere to the following enterprise versioning and engineering standards across all repositories and agent workflows:

## 1. Semantic Versioning (SemVer 2.0.0)
Always follow strict `MAJOR.MINOR.PATCH` versioning for software releases, libraries, and microservices:
- **`MAJOR`**: Breaking changes, removed API routes, altered response schemas, or incompatible database migrations.
- **`MINOR`**: Backward-compatible new functionality (new endpoints, new tools, extended models).
- **`PATCH`**: Backward-compatible bug fixes, security remediations, performance enhancements, and internal refactors.

## 2. Conventional Git Commits & Release Tagging
Every Git commit must follow the Conventional Commits specification:
- `feat(scope):` New user-facing feature or capability
- `fix(scope):` Bug fix or error resolution
- `refactor(scope):` Code change that neither fixes a bug nor adds a feature
- `test(scope):` Adding missing tests or correcting existing tests
- `docs(scope):` Documentation only changes
- `perf(scope):` A code change that improves performance
- `build(scope):` Changes that affect the build system or external dependencies
- `ci(scope):` Changes to CI configuration files and scripts
- `chore(scope):` Maintenance tasks that do not alter src or test files

**Rule:** Every major milestone or release must be tagged with an annotated Git tag matching `vX.Y.Z` (e.g., `git tag -a v1.0.0 -m "Release v1.0.0"`).

## 3. API & Contract Versioning
- **URL Path Versioning:** All public and internal API endpoints must be version-prefixed (e.g., `/api/v1/...`).
- **Zero Breaking Changes:** Never mutate an existing endpoint's response shape or remove fields without introducing a new version (`/api/v2/...`) and an explicit deprecation grace period.
- **Backwards Compatibility:** Default optional fields to `None` with fallback values to ensure older clients and external merchants do not experience runtime serialization crashes.

## 4. Database Schema & Migration Versioning
- All relational schema alterations must be tracked via versioned, reproducible migration scripts (e.g., Alembic migrations, dbt migrations, or timestamped SQL files).
- Raw manual `ALTER TABLE` commands in production without versioned migration files are strictly forbidden.

## 5. Dependency & Runtime Version Pinning
- Never leave dependencies unpinned or floating with bare package names in production `requirements.txt` or `package.json`.
- Always declare tested minimum versions or pinned releases (e.g., `fastapi>=0.104.0,<1.0.0`).
- Container base images must always pin explicit OS/runtime tags (e.g., `python:3.11-slim`, `postgres:15-alpine`), never generic `:latest`.

## 6. Prompt & AI Model Artifact Versioning
- For LLM prompts, MCP tool schemas, and computer vision models, maintain explicit version metadata (`v1.0.0`) in tool registries and docstrings so changes can be tracked and benchmarked across regression suites.
