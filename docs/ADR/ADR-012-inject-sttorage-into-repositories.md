ADR-012 — Inject Storage into Repositories

Decision: Repository objects receive their storage dependency through the constructor rather than constructing it internally.

Rationale: This preserves single responsibility, reduces coupling, and improves testability

