# Add rate limit tier policy

<!-- daily-pr-task: rate-limit-tier-policy -->

Rate limit tier policy should keep public API limits explicit per customer plan. Limits should increase by tier and never leave free traffic unlimited.

Policy fields:

- free tier rpm
- basic tier rpm
- pro tier rpm
- burst multiplier

## Portfolio Value

Shows gateway controls can enforce plan-based API usage limits.

## Validation

Run the unit test and confirm free/basic/pro tiers have ordered limits.
