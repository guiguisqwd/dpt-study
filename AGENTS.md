# Shared project instructions

Read `CLAUDE.md` and `README.md` before changing this project. The user requires
GitHub to be the shared source of truth for both Codex and Claude.
The intended independent Codex project name is **解剖学习工作台**; its maintenance scope covers
the whole Anatomy study workbench. Read [README.md](./README.md)
for project scope, source locations and handoff requirements.

The repository has two content blocks (2026-10-08): `library/` is the anatomy knowledge
library, one folder per chapter (`library/shoulder/`, `library/hip/`), each with `text/`,
`figures/`, `pdf/` and `3d/`; `daily/` generates each day's study pack from the library.
`site/` assembles and publishes the website. Rules live only in `standards/`.
Shoulder is the first chapter, not the limit of the product. The repository was renamed
`shoulder-study` → `dpt-study` on 2026-10-08. For a new
topic, read `library/README.md`, use `library/<id>/topic.json` and the shared
scaffold, validation and build scripts. Do not duplicate the entire viewer or
copy shoulder facts into another anatomical region. Keep topic content and model
bindings separate from shared application logic. A draft topic is not a finished
course and must be visibly identified as a draft.

For every authorized update, inspect the working tree, fetch and safely reconcile
the remote, edit the maintained sources, run appropriate checks, then commit and
push the task's changes. Verify the remote commit before reporting synchronization.
Preserve unrelated user/agent changes. Never force-push or reset them away.

Keep English before Chinese, preserve existing audio, and preserve the independent
`library/shoulder/3d/public/reading-claude.html` edition. See `CLAUDE.md` for the full
content, build, collaboration and deployment rules.

Apply the established six-stage learning structure to every topic from the start:
anatomy, innervation, movement, clinical anatomy, review, and paper reading.
Include labeled origin/insertion diagrams, complete English descriptions followed
by Chinese translations, anatomical nerve diagrams and explicit spinal-region
notation, validated model links, complete answers as well as mnemonics, and
source-based paper appraisal. Validate topic data and build the generated outputs;
also inspect diagrams, responsive layout and camera transitions in the browser.
Passing a schema check does not establish anatomical accuracy or publication
readiness. Preserve source evidence and document outstanding gaps accurately.
