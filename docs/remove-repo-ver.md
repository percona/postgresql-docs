# Removed repository versions

## Overview

Some Percona Distribution for PostgreSQL repository versions are no longer available and may return a `404 Not Found` error when accessed. The affected versions are:

- ppg-14.19
- ppg-15.14
- ppg-16.10
- ppg-17.6

## Reason for removal

These versions were part of a release that included known issues affecting stability and reliability (also referred to internally as the "assertion release").

To prevent unintended usage, these repositories were removed from distribution.

## What should you do instead?

Use the latest available minor version for your PostgreSQL major version.

Example:

- Instead of `ppg-16.10`, use the latest `ppg-16.x`

See [installation guide]

## Additional context

For more details, see the relevant release notes:
- [link to release notes]