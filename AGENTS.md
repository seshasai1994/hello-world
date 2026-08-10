# AGENTS.md

## Cursor Cloud specific instructions

This is a **documentation-only repository**. There is no application source code, package
manager, dependency manifest, build system, linter, or automated test suite. The content is:

- `README.md`
- `docs/client-deck/` — planning/reference material for a Geth-powered on-chain trading
  platform pitch:
  - `competitor-slide.md` / `competitor-slide.html` — a self-contained static slide
    (inline CSS, no external assets or build step)
  - `1m-arr-plan.md`, `geth-endpoint-reference.md` — Markdown reference docs

### Working notes

- There are no dependencies to install and nothing to compile. The environment update
  script is intentionally a no-op.
- There is nothing to lint, test, or build. Do not add such tooling unless a task
  explicitly asks for it.
- The only runnable "application" is the static slide. To preview the docs, serve the repo
  root with any static file server and open the file in a browser, e.g.:

  ```bash
  python3 -m http.server 8000   # run from the repo root
  # then open http://localhost:8000/docs/client-deck/competitor-slide.html
  ```

  `competitor-slide.html` is fully self-contained, so it can also be opened directly as a
  `file://` URL without a server.
