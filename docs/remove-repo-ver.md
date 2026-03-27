# Repository 404 errors and removed versions

Some Percona Distribution for PostgreSQL repository versions are no longer available and may return a `404 Not Found` error when accessed. This happens because these versions have been removed from the repository.

The affected versions are:

- `ppg-14.19`
- `ppg-15.14`
- `ppg-16.10`
- `ppg-17.6`

## Reason for removal

These versions were part of a release that included known issues affecting stability and reliability.

To prevent unintended usage, these repositories were removed from distribution.

These versions are not recommended for production use.

## What should you do instead?

Use the latest available minor version for your PostgreSQL major version.

Examples:

- Instead of `ppg-17.6`, use the latest `ppg-17.x`

For installation and upgrade instructions, see the [minor upgrade guide](minor-upgrade.md).
