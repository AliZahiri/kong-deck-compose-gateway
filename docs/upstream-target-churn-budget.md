# Upstream target churn budget

A decK diff can be schema-valid while replacing or reweighting most of an upstream in one promotion. That change concentrates rollout risk and can remove healthy rollback capacity before active health checks reveal a problem.

`kong_deck_gateway.upstream_target_churn` compares two declarative target lists. It validates unique target identities and Kong-compatible positive weights, then counts additions, removals, and weight changes against the union of both sets. Promotion fails when the configured percentage budget is exceeded.

Run the focused tests with:

```bash
python3 -m unittest tests.test_upstream_target_churn
```

The gate is intentionally offline. Pair it with decK diff, upstream health evidence, target drain policy, and rollback state before syncing configuration.
