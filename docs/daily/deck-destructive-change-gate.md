# Add decK destructive change gate

<!-- daily-pr-task: deck-destructive-change-gate -->

A decK diff may be syntactically valid while deleting routes, services, consumers, or upstreams that require explicit recovery evidence. This gate validates normalized change records, rejects duplicate entity mutations, and requires reviewer, change-ticket, and backup references whenever a destructive action is present. It evaluates an exported plan and never performs a sync.

## Portfolio Value

Adds review and recovery evidence to destructive gateway-as-code plans while keeping decK promotion validation deterministic and side-effect free.

## Validation

Run `python3 -m unittest discover -s tests` and confirm recoverable approved deletions pass while missing review/ticket/backup evidence, invalid records, duplicates, empty plans, and unsupported entity metadata fail.
