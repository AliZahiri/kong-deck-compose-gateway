# Add gateway observability notes

<!-- daily-pr-task: gateway-observability -->

Gateway observability should show whether failures are caused by routing, upstream services, client behavior, or gateway policy.

Useful signals:

- request count by route and status code
- upstream latency
- gateway latency
- rate-limit rejections
- request size rejections
- Admin API change history through CI logs

## Portfolio Value

Connects Kong operations with monitoring and incident diagnosis.

## Validation

Review the markdown file and confirm the signals support troubleshooting.
