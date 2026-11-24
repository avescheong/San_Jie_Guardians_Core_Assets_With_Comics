## name: vm-drive-reconciliation description: Governed workflow for reconciling local VM sandbox state against canonical Google Drive Single Source of Truth (SSOT) repositories, auto-splitting >10 MB builds into <5 MB SHA-256-verified binary chunks with reassemble_*.py, sweeping superseded files into archive folders, generating ASSET_INVENTORY_INDEX.md and canonical folder mappings, and syncing HANDOVER_CURRENT.md. Auto-activates whenever the user says "sync to drive", "upload to google drive", "file by file", "by batches", "archive old unused files", "reorganise our asset", "inventory index", "folder mapping", "find gaps in my files", "where we stop", "don't forget the handover", or asks to reconcile, upload, or audit VM and Drive folders. allowed-tools: default_api drive context_service_agent
# VM and Google Drive Reconciliation (v2.1 - Auto-Chunking & Canonical Archive Edition)
Execute deterministic, read-first environment reconciliation, reference integrity validation, automatic <5 MB binary chunking for large builds, archive sweeping, and governed custody transfers between the local VM sandbox and Google Drive Single Source of Truth (SSOT) repositories without silent drift, pointer rot, evidence inflation, or cold-start disorientation.
## When to Use
Reconciling local VM directories against a canonical Google Drive repository or checking "where we stopped" / "find gaps in my files" from a Drive link.
Uploading large HTML5 engines, ZIP bundles, or packages (>9.5 MB) to Google Drive by automatically splitting into <5 MB binary parts with a SHA-256 reassemble_*.py script.
Archiving old or unused files into an archive/ or 99_ARCHIVE_SUPERSEDED/ folder and reorganizing project workspaces into canonical numbered folders with an ASSET_INVENTORY_INDEX.md.
Auditing document pointer chains, hyperlink integrity, and deprecated archive references.
Enforcing the Milestone Deviation Record (MDR) protocol for out-of-inventory code modifications.
Verifying bit-exact SHA-256 parity across environments and updating HANDOVER_CURRENT.md and CHANGELOG.md after every completed task.
## Execution Modes

| Execution Mode | Operational Scope & Trigger | Mandatory Steps | Bypassed Steps |
| :--- | :--- | :--- | :--- |
| Mode A: Quick Sync / Single File Custody | Routine transfers of 1 to few files, calculation models, scripts, or single-doc updates. | Steps 1, 2, 3, 7, 9 | Skips Pointer Audit, MDR, and Cold-Start Simulation. |
| Mode B: Milestone Promotion & Batch Sync | Multi-file software releases, >10 MB split uploads, folder reorganization, archive sweeps, or sprint checkpoints. | Steps 1, 2, 3, 5, 6, 7, 9 | Skips full-repository Pointer Audit and Cold-Start Simulation. |
| Mode C: Full SSOT Baseline Seal | Major release gates, constitutional vaults (RIE/AITG), production baseline freezes, or external handover. | All Steps (1 through 9) | None. Complete comprehensive audit and sealing protocol. |

## Core Steps
Enforce Pre-Flight Governance Invariants: Folder Invariance, Derived Identity (SHA-256), Zero Auto-Repair, and Four-Tier Evidence Classification (State A–State D).
Execute Two-Phase Environment Discovery: Online Drive Inventory Dump (drive_inventory_dump.json) followed by offline VM SHA-256 comparison.
Classify Environment Delta & Enforce Stop Conditions: VERIFIED_MATCH, PENDING_UPLOAD_REVIEW, PENDING_VM_SYNC_REVIEW, CRITICAL_DRIFT.
Audit Canonical Pointer & Reference Integrity (Mode C Only): Scoped pointer linter and Google Workspace export terminal section check.
Audit Milestone Scope Boundaries & Enforce MDR Protocol (Modes B & C).
Validate Evidence Claims (Modes B & C).
Perform Governed Custody Transfer, Auto-Chunking & Archive Sweep (All Modes): Pre-upload sanity check, SHA-256 hash, Archive-Never-Delete (99_ARCHIVE_SUPERSEDED/), <5 MB auto-chunking with reassemble_*.py for files >9.5 MB, cryptographic parity verification, and atomic HANDOVER_CURRENT.md / ASSET_INVENTORY_INDEX.md sync.
Execute Cold-Start Navigation Simulation Gate (Mode C Only).
Emit the Structured Reconciliation Report.
## Gotchas
Never Overclaim Evidence: Label static checks as "State C: Static Contract Compliance Verified."
Never Downscale Assets to Fit 10 MB: Always use the <5 MB binary chunker + reassemble_*.py protocol when a self-contained HTML5 or ZIP file exceeds 9.5 MB.
Always Sync Handover Docs: Never finish a file upload, batch generation, or folder reorganization without updating HANDOVER_CURRENT.md (and ASSET_INVENTORY_INDEX.md when assets change) in the same turn.
