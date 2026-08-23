"""
Schema drift detection for SchemaDNA.

Detects:
- Added columns
- Removed columns
- Modified column data types
"""

from __future__ import annotations

from .models import Schema, SchemaDrift


def detect_drift(
    old_schema: Schema,
    new_schema: Schema,
) -> SchemaDrift:
    """
    Compare two schemas and detect structural changes.

    Parameters
    ----------
    old_schema:
        The previous version of the dataset schema.

    new_schema:
        The current version of the dataset schema.

    Returns
    -------
    SchemaDrift
        Object containing added, removed, and modified columns.
    """

    old_columns = old_schema.columns
    new_columns = new_schema.columns

    old_names = set(old_columns)
    new_names = set(new_columns)

    added_names = new_names - old_names
    removed_names = old_names - new_names
    common_names = old_names & new_names

    added = [
        new_columns[name]
        for name in sorted(added_names)
    ]

    removed = [
        old_columns[name]
        for name in sorted(removed_names)
    ]

    modified = {}

    for name in sorted(common_names):
        old_dtype = old_columns[name].dtype
        new_dtype = new_columns[name].dtype

        if old_dtype != new_dtype:
            modified[name] = (old_dtype, new_dtype)

    return SchemaDrift(
        added=added,
        removed=removed,
        modified=modified,
    )