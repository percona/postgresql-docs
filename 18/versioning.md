> For the complete documentation index, see [llms.txt](https://docs.percona.com/postgresql/18/llms.txt).

# Version Numbering

Starting with PostgreSQL 18, Percona uses the following format:

`MAJOR.MINOR.PATCH`

For example:

`18.7.1`

Where:

- **MAJOR** = The upstream PostgreSQL major version (e.g. 18 → PostgreSQL 18)
- **MINOR** = The upstream PostgreSQL release number
- **PATCH** = Percona’s internal build number (specific to packaging or Percona-only updates)

| **Release type**           | **Version example** | **What changes?**                                    |
| -------------------------- | ------------------- | ---------------------------------------------------- |
| **First Percona build**    | 18.0.1              | Initial Percona build on upstream 18.0, build #1     |
| **Percona-only update**    | 18.0.2              | Build #2 on the same upstream 18.0                   |
| **Upstream patch/feature** | 18.1.1              | Upstream release → MINOR bump to 1, PATCH reset to 1 |
| **Next Percona build**     | 18.1.2              | Build #2 on upstream 18.1                            |

The above versioning is only applicable to PSP 18.x.x as it is the only Percona forked server. The **third digit** is **always** PSP’s build number, never an upstream patch. If you see it go from …1 → …2 this means a PSP-specific update was shipped.

Since PPG 13 to 16 are pure community versions, only the first 2 digits scheme is used for them.

Note

If you’re looking for more information, check the [FAQ](https://docs.percona.com/postgresql/18/faq.html#does-minor-cover-both-upstream-feature-and-patch-releases).
