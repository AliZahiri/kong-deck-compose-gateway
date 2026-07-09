_format_version: "3.0"

services:
  - name: sample-api
    url: http://sample-api-{{ACTIVE_COLOR}}:80
    plugins:
      - name: rate-limiting
        enabled: true
        config:
          minute: {{RATE_LIMIT_MINUTE}}
          policy: {{RATE_LIMIT_POLICY}}
          fault_tolerant: {{RATE_LIMIT_FAULT_TOLERANT}}
    routes:
      - name: sample-api-route
        paths:
          - /api
        strip_path: true
        preserve_host: false
