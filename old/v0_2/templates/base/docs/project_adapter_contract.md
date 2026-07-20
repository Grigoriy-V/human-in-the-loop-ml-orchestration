# Project adapter contract

An adapter is self-contained: it carries local rules, profiles, helpers,
schemas, ledger, roadmap, log, Core pin, and managed manifest. Generic Core
rules are universal; an overlay may add domain policy but may not weaken
supervision, privacy, lifecycle, or human gates.

`base_copy` entries come from `templates/base`. `overlay_copy` entries come
from the selected declared adapter overlay. Both relationships require
byte-identical target/Core hashes. Generated lock metadata and mutable project
evidence are not managed copies.
