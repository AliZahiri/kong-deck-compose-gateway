# Add gateway plugin secret-reference gate

<!-- daily-pr-task: plugin-config-secret-reference-gate -->

Gateway plugin configuration should not embed credential values in declarative state. This offline gate validates sensitive plugin settings: sensitive keys must use an approved environment-variable reference, literal credentials are rejected, and reference names are unique. It evaluates supplied configuration metadata without reading environment values.

## Portfolio Value

Makes decK configuration safer to publish and review by treating plugin credential references as an explicit policy boundary.

## Validation

Run `python3 -m unittest discover -s tests` and confirm environment-referenced secrets pass while empty sets, literal sensitive values, malformed references, and duplicate references fail.
