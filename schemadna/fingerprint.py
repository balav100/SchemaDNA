"""
Schema fingerprinting for SchemaDNA.

A schema fingerprint is a deterministic SHA-256 hash
generated from a normalized dataset schema.
"""

from __future__ import annotations

import hashlib
import json
from typing import Mapping

from .models import Schema


def normalize_schema(schema: Schema) -> list[dict[str, str]]:
    """
    Normalize a schema into a deterministic representation.

    Columns are sorted alphabetically by name so that
    column ordering does not affect the fingerprint.
    """

    return [
        {
            "name": column.name,
            "dtype": column.dtype,
        }
        for column in sorted(
            schema.columns.values(),
            key=lambda column: column.name,
        )
    ]


def fingerprint_schema(schema: Schema) -> str:
    """
    Generate a SHA-256 fingerprint for a schema.

    The same schema will always produce the same fingerprint.
    """

    normalized = normalize_schema(schema)

    serialized = json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()


def fingerprint_mapping(schema_mapping: Mapping[str, str]) -> str:
    """
    Generate a fingerprint directly from a column-to-dtype mapping.
    """

    schema = Schema.from_mapping(dict(schema_mapping))

    return fingerprint_schema(schema)