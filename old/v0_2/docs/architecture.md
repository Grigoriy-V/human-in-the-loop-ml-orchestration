# Architecture

Core contains generic governance: roles, task contracts, ledgers, schemas,
profiles, validation, and version metadata. An adapter owns all domain policy.
Core has no model, dataset, or evaluation dependency.

Canonical bootstrap inputs live under `templates/base`. Explicit overlays live
under `templates/adapters/<adapter_type>`. The registry declares exactly which
immutable source becomes each target file and whether it is a `base_copy` or
`overlay_copy`. Both are byte-identical copy relationships.

Core's immutable source manifest hashes tools, configs, schemas, tests, and
templates. Live roadmaps, logs, reports, ledgers, and locks are mutable
evidence boundaries and are excluded. Target pins likewise exclude emitted
mutable evidence.
