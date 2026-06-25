# Add upstream health policy

<!-- daily-pr-task: upstream-health-policy -->

Kong upstreams should expose health policy before traffic promotion. Active checks catch broken backends before traffic moves, while passive checks help detect runtime failures.

Required policy:

- active health check path
- healthy threshold
- unhealthy threshold
- passive failure detection

## Portfolio Value

Connects Kong route promotion with active upstream health checks.

## Validation

Run the unit test and confirm active and passive health checks are required.
