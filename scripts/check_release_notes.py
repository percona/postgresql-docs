#!/usr/bin/env python3
"""Cross-checks that every release-notes page is wired up correctly:

- referenced in the effective mkdocs nav (error if missing)
- linked from the release notes index page (error if missing)
- has a variables.yml date entry (error if the key is missing entirely,
  warning if it's present but still a placeholder like TBD)

Never writes anything back - read-only validation, safe to run on every PR.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE_RE = re.compile(r"^release-notes-v(?P<version>[\d.]+[a-z0-9.]*)\.md$")

errors = []
warnings = []


class _Loader(yaml.SafeLoader):
    """mkdocs-base.yml/mkdocs.yml use custom tags (!!python/name:..., !ENV,
    ...) for config we don't care about here - tolerate any unknown tag
    instead of blowing up the whole parse over it.
    Also: force all mapping keys to stay plain strings. PyYAML's default
    int resolver treats '18_6_1' as the integer 1861 (underscores are
    digit-group separators), which silently breaks lookups like
    date['18_6_1'] - every key in this repo's yaml is a version-ish
    string, never actually meant to be numeric."""


def _construct_str_keyed_mapping(loader, node):
    return {
        loader.construct_scalar(k): loader.construct_object(v, deep=True)
        for k, v in node.value
    }


def _construct_undefined(loader, node):
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    return loader.construct_mapping(node)


_Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_str_keyed_mapping)
_Loader.add_constructor(None, _construct_undefined)


def error(msg):
    errors.append(msg)
    print(f"::error::{msg}")


def warn(msg):
    warnings.append(msg)
    print(f"::warning::{msg}")


def load_yaml(path):
    with open(path) as f:
        return yaml.load(f, Loader=_Loader) or {}


def effective_nav():
    """mkdocs INHERIT semantics: a top-level key defined in the child
    (mkdocs.yml) fully replaces the same key in the parent (mkdocs-base.yml);
    if the child doesn't define it, the parent's value is used."""
    child = load_yaml(ROOT / "mkdocs.yml")
    if "nav" in child:
        return child["nav"]
    base_path = ROOT / (child.get("INHERIT") or "mkdocs-base.yml")
    base = load_yaml(base_path)
    return base.get("nav", [])


def collect_nav_paths(nav, acc):
    for item in nav:
        if isinstance(item, dict):
            for value in item.values():
                if isinstance(value, str):
                    acc.add(value)
                else:
                    collect_nav_paths(value, acc)
        elif isinstance(item, str):
            acc.add(item)
    return acc


def find_release_note_files():
    """Version files live either under docs/release-notes/ or flat under
    docs/ (15 uses the flat layout) - so check both."""
    found = []
    for base in (ROOT / "docs" / "release-notes", ROOT / "docs"):
        if not base.is_dir():
            continue
        for f in base.glob("release-notes-v*.md"):
            m = VERSION_FILE_RE.match(f.name)
            if m:
                found.append((f, m.group("version")))
    return found


def find_index_page(nav_paths):
    for path in nav_paths:
        if Path(path).name == "release-notes.md":
            return ROOT / "docs" / path
    return None


def main():
    nav_paths = collect_nav_paths(effective_nav(), set())
    nav_basenames = {Path(p).name for p in nav_paths}

    index_page = find_index_page(nav_paths)
    index_content = index_page.read_text() if index_page and index_page.exists() else ""
    if not index_page:
        error("Could not locate the 'Release notes index' page from the nav - skipping index-link check.")

    variables = load_yaml(ROOT / "variables.yml")
    dates = variables.get("date") or {}

    for file_path, version in find_release_note_files():
        label = f"{version} ({file_path.relative_to(ROOT)})"
        content = file_path.read_text()

        # 1. nav check
        if file_path.name not in nav_basenames:
            error(
                f"{label}: not referenced in the mkdocs nav - it won't show up "
                f"in the Release notes sidebar even though the page builds."
            )

        # 2. index page check
        if index_page and file_path.name not in index_content:
            error(
                f"{label}: not linked from the release notes index page "
                f"({index_page.relative_to(ROOT)})."
            )

        # 3. release date check - only applies to pages that actually use the
        # {{date.<key>}} macro; older pages hardcode the date in prose instead.
        key = version.replace(".", "_")
        macro = f"{{{{date.{key}}}}}"
        if macro not in content:
            continue
        if key not in dates:
            error(
                f"{label}: uses {macro} but variables.yml has no date.{key} "
                f"entry - the placeholder won't render."
            )
        else:
            value = str(dates[key]).strip()
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
                warn(
                    f"{label}: release date looks like a placeholder "
                    f"(date.{key} = '{value}') - remember to set the real date "
                    f"before this ships."
                )

    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
