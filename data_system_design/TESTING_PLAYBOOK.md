# Data Platform Testing Playbook

[Scenario index](../DATA_SYSTEM_DESIGN_INDEX.md)

Test the product contract and failure boundaries, not only whether a job ran. The scenario documents propose workload-specific tests. This guide shows where to automate them and what evidence to retain; these are proposed platform tests, not claims that cloud deployments were executed for this catalog.

| Stage | Tests | Cadence | Evidence |
| --- | --- | --- | --- |
| Local and PR | Pure transforms, keys, business arithmetic, schema compatibility, SQL fixtures, DAG parse, diagram syntax, IaC policies | Every change | Deterministic fixtures, expected rows, artifact commit and failing contract |
| Staging integration | Actual connectors, loading, grants, source snapshots, deletes, API pagination, sink acknowledgments | Before promotion and on connector/runtime upgrades | Source/target checkpoints, input manifests, logs, row-level and business-level comparisons |
| State and failure | Duplicate replay, out-of-order delivery, broker rebalance, crash before/after sink commit, checkpoint recovery | Targeted fixtures each release; isolated scheduled fault drills | Injected fault position and externally visible state before and after recovery |
| Performance and cost | Skew, hot keys, expected concurrency, backlog catch-up, cold/warm cache, file sizes and egress | Major changes and periodic representative runs | Data volume, distribution, query classes, latency percentiles and cost per processed unit |
| Security | Allowed/denied queries, tenant boundaries, direct-storage bypass, source ACL propagation, runner identity | PR policies plus staging/runtime probes | Identity, requested action, expected allow/deny, actual access decision |
| Continuous product checks | Freshness, completeness, schema drift, key integrity, semantic invariants and volume anomalies | Every publish and continuously where appropriate | Consumer timestamp, source cutoff, completeness manifest and product release |
| Recovery | Protected copy restore, catalog/grant restore, checkpoint/source retention compatibility, RPO/RTO | Isolated regular drill and supervised production exercise when approved | Recovered data point, elapsed time, job version, reconciled outputs and deviations |

## High value fixture patterns

| Pattern | Fixture | Required observation |
| --- | --- | --- |
| Idempotency | Deliver the same stable event or file version twice | Business state and totals stay unchanged after the second application. |
| Delete ordering | Apply delete sequence 20, then replay update sequence 19 | The entity stays deleted. |
| Snapshot continuity | Update and delete keys while a historical snapshot is loading | The converged state matches the source at the agreed checkpoint. |
| Late event time | Deliver a record before and after the configured watermark threshold | Both outcomes follow the declared late-data policy and are visible in evidence. |
| One-to-many joins | Two payments and three adjustments for one order | Totals use the intended grain without multiplying amounts. |
| Schema drift | Rename or remove a field and introduce incompatible types | Breaking data is rejected, quarantined or deliberately migrated; no silent coercion. |
| Tenant isolation | Run equivalent reads as permitted and denied tenant identities | Every query, export, cache and storage path enforces the intended boundary. |
| Temporal truth | Change a dimension after a prediction or historical event time | The historical or point-in-time join does not use future information. |
| Atomic publish | Crash between staging and release visibility | Consumers see one accepted release or clearly marked partial/stale state. |
| Recovery | Restore data with a catalog and stream checkpoint from different times | The process detects inconsistency or performs a controlled reconstruction. |

## Reconciliation depth

Compare schema and type interpretation, primary-key sets, duplicate counts, expected partition coverage, selected record-level values, and grouped business totals. Counts alone can agree while keys or amounts are wrong. Hashes require canonicalization of NULLs, decimals, timezones and field order. Compare against a declared source checkpoint so live source changes do not look like ingestion errors.

## Automation technologies

Use pytest/JUnit or appropriate language frameworks for deterministic transformations and client behavior; dbt data tests for warehouse assertions; Great Expectations or equivalent for data contracts; SQL and independent reference oracles for reconciliation; Testcontainers or isolated services for real interfaces; cloud policy checks and explicit denied-access probes for authorization. Fault and load tools must exercise the real contracts of the selected broker, compute and sink. [dbt data tests](https://docs.getdbt.com/docs/build/data-tests), [Great Expectations Core](https://docs.greatexpectations.io/docs/core/introduction/).

## What should not be a blind automated claim

Do not treat SDK mocks as proof of real API quota, network, authentication or connector compatibility. Do not treat catalog scans as permission enforcement. Do not treat average load as proof of hot-key or peak behavior. Do not label arbitrary side effects exactly-once because the stream processor has checkpoints. Do not call a backup usable without a successful restore.

## Human acceptance

Business owners define semantic equivalence and reconciliation tolerance. Operators assess cutover and rollback consequences. Security and data owners assess purpose, retention, access, and location. Automation supplies repeatable evidence and blocks declared contract failures; it does not silently choose those organizational policies.

## This repository verification

The included validators check document completeness, source/diagram links, diagram identity, enumeration rules and candidate metadata. The diagram runner parses and renders Mermaid. Those tests do not connect to cloud services, test real workloads, or prove benchmark targets. See [actual validation results](VALIDATION.md).
