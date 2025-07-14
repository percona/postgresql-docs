# Percona Server for PostgreSQL: Version Numbering

!!! important
    The below versioning is only applicable to PSP's 17.x.x releases. Only the first 2 digits scheme is used for PPG versions 13 to 16.

Our version strings use the following format:

`MAJOR.MINOR.PATCH`

Where:

- **MAJOR** = upstream PostgreSQL major (e.g. 17 → PostgreSQL 17)
- **MINOR** = upstream release iteration (feature or patch)
- **PATCH** = Percona's packaging/build number **only** (the third digit)

| **Release type** | **Version example** | **What changes?** |
| --- | --- | --- |
| **First Percona build** | 17.0.1 | Initial Percona build on upstream 17.0, build #1 |
| **Percona-only update** | 17.0.2 | Build #2 on the same upstream 17.0 |
| **Upstream patch/feature** | 17.1.1 | Upstream release → MINOR bump to 1, PATCH reset to 1 |
| **Next Percona build** | 17.1.2 | Build #2 on upstream 17.1 |

!!! note
    The **third digit** is **always** Percona’s build number, never an upstream patch. If you see it go from …1 → …2 this means a Percona-specific update was shipped.

    If you're looking for more information, check the [FAQ](faq.md#does-minor-cover-both-upstream-feature-and-patch-releases).
