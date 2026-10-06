# Shared project instructions

Read `CLAUDE.md` and `README.md` before changing this project. The user requires
GitHub to be the shared source of truth for both Codex and Claude.

This product is **Anatomy study / 解剖学习**, with multiple anatomy topics.
Shoulder is the first topic, not the limit of the product. Keep the existing
`shoulder-study` repository URL and historical local paths compatible. For a new
topic, read `docs/ADDING_A_TOPIC.md`, use `topics/<slug>/topic.json` and the shared
scaffold, validation and build scripts. Do not duplicate the entire viewer or
copy shoulder facts into another anatomical region. Keep topic content and model
bindings separate from shared application logic. A draft topic is not a finished
course and must be visibly identified as a draft.

For every authorized update, inspect the working tree, fetch and safely reconcile
the remote, edit the maintained sources, run appropriate checks, then commit and
push the task's changes. Verify the remote commit before reporting synchronization.
Preserve unrelated user/agent changes. Never force-push or reset them away.

Keep English before Chinese, preserve existing audio, and preserve the independent
`肩部3D学习/public/reading-claude.html` edition. See `CLAUDE.md` for the full
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
