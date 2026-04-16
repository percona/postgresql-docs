# Repository 404 errors and removed versions

Some Percona Distribution for PostgreSQL repository versions are no longer available and may return a `404 Not Found` error when accessed. This happens because these versions have been removed from the repository.

The following versions are affected:

- `ppg-14.19`
- `ppg-15.14`
- `ppg-16.10`
- `ppg-17.6`

## Reason for removal

These versions were part of a release that included known issues affecting stability and reliability.

To prevent unintended usage, these repositories were removed from distribution. These versions are not recommended for production use.

For additional details, see the [relevant release notes](release-notes/release-notes-v14.20.md).

## What should you do instead?

Use the latest available minor version for your PostgreSQL major version.

Examples:

- Replace `ppg-14.19` with the latest available `ppg-14.x`

For upgrade instructions, see the [minor upgrade guide](minor-upgrade.md).
