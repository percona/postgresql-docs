# Percona Server for PostgreSQL: Version Numbering

Our version strings use the following format:

`MAJOR.MINOR.PATCH-PERCONA`

Where:

- **MAJOR** = upstream PostgreSQL major (e.g. 17 → PostgreSQL 17)
- **MINOR** = upstream release iteration (feature or patch)
- **PERCONA** = Percona packaging/build iteration **only** (the third digit)

| **Release type** | **Version example** | **What changes?** |
| --- | --- | --- |
| **First Percona build** | 17.0.1 | Initial Percona build on upstream 17.0, build #1 |
| **Percona-only update** | 17.0.2 | Build #2 on the same upstream 17.0 |
| **Upstream patch/feature** | 17.1.1 | Upstream release → MINOR bump to 1, PERCONA reset to 1 |
| **Next Percona build** | 17.1.2 | Build #2 on upstream 17.1 |

!!! note
    The **third digit** is **always** Percona’s build number, never an upstream patch. If you see it go from …1 → …2 this means a Percona-specific update was shipped.

1. Does **MINOR** cover both upstream feature and patch releases?
2. When upstream bumps MINOR, should PERCONA **always** reset to 1?
3. Any edge cases where we’d ever touch both MINOR and PERCONA in one go?