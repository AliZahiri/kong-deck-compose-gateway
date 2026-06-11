_format_version: "3.0"

services:
  - name: sample-api
    url: http://sample-api-{{ACTIVE_COLOR}}:80
    routes:
      - name: sample-api-route
        paths:
          - /api
        strip_path: true
        preserve_host: false
