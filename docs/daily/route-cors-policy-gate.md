# Add route CORS policy gate

<!-- daily-pr-task: route-cors-policy-gate -->

Gateway CORS configuration is a browser security boundary and should not combine credentialed requests with wildcard origins or expose undeclared methods and headers. This offline gate validates unique route policies, explicit HTTPS origins, bounded preflight caching, non-empty method sets, and the wildcard/credentials constraint before decK promotion.

## Portfolio Value

Adds a browser-facing gateway security contract so permissive credentialed origins and malformed preflight policies are rejected before decK sync.

## Validation

Run `python3 -m unittest discover -s tests` and confirm explicit HTTPS policies pass while empty input, duplicate routes/origins, insecure origins, wildcard credentials, invalid methods, excessive cache ages, and invalid policy values fail.
