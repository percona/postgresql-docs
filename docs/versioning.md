# Version Numbering

Starting with PostgreSQL {{pgversion}}, Percona uses the following format:

`MAJOR.MINOR.PATCH`

For example:

`{{pspgversion}}`

Where:

- **MAJOR** = The upstream PostgreSQL major version (e.g. {{pgversion}} → PostgreSQL {{pgversion}})
- **MINOR** = The upstream PostgreSQL release number
- **PATCH** = Percona's internal build number (specific to packaging or Percona-only updates)

| **Release type** | **Version example** | **What changes?** |
| --- | --- | --- |
| **First Percona build** | {{pgversion}}.0.1 | Initial Percona build on upstream {{pgversion}}.0, build #1 |
| **Percona-only update** | {{pgversion}}.0.2 | Build #2 on the same upstream {{pgversion}}.0 |
| **Upstream patch/feature** | {{pgversion}}.1.1 | Upstream release → MINOR bump to 1, PATCH reset to 1 |
| **Next Percona build** | {{pgversion}}.1.2 | Build #2 on upstream {{pgversion}}.1 |

The above versioning is only applicable to PSP {{pgversion}}.x.x as it is the only Percona forked server. The **third digit** is **always** PSP’s build number, never an upstream patch. If you see it go from …1 → …2 this means a PSP-specific update was shipped.

Since PPG 13 to 16 are pure community versions, only the first 2 digits scheme is used for them.

!!! note
    If you're looking for more information, check the [FAQ](faq.md#does-minor-cover-both-upstream-feature-and-patch-releases).
