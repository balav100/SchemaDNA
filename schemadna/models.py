"""
Core data models for SchemaDNA.

SchemaDNA uses these models to represent dataset schemas
and schema-drift results in a structured way.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class ColumnSchema:
    """
    Represents the schema information for a single column.
    """

    name: str
    dtype: str


@dataclass
class Schema:
    """
    Represents the schema of a dataset.
    """

    columns: Dict[str, ColumnSchema] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, schema_mapping: Dict[str, str]) -> "Schema":
        """
        Create a Schema object from a simple mapping.

        Example:
            {
                "customer_id": "int64",
                "name": "object"
            }
        """

        columns = {
            name: ColumnSchema(name=name, dtype=dtype)
            for name, dtype in schema_mapping.items()
        }

        return cls(columns=columns)


@dataclass
class SchemaDrift:
    """
    Represents the differences detected between two schemas.
    """

    added: List[ColumnSchema] = field(default_factory=list)
    removed: List[ColumnSchema] = field(default_factory=list)
    modified: Dict[str, tuple[str, str]] = field(default_factory=dict)

    @property
    def has_drift(self) -> bool:
        """
        Return True if any schema changes were detected.
        """

        return bool(
            self.added
            or self.removed
            or self.modified
        )

    def summary(self) -> str:
        """
        Return a human-readable summary of the detected drift.
        """

        if not self.has_drift:
            return "No schema drift detected."

        lines = ["Schema Drift Detected", ""]

        if self.added:
            lines.append("Added columns:")
            for column in self.added:
                lines.append(
                    f"  + {column.name} ({column.dtype})"
                )
            lines.append("")

        if self.removed:
            lines.append("Removed columns:")
            for column in self.removed:
                lines.append(
                    f"  - {column.name} ({column.dtype})"
                )
            lines.append("")

        if self.modified:
            lines.append("Modified columns:")
            for name, (old_dtype, new_dtype) in self.modified.items():
                lines.append(
                    f"  ~ {name}: {old_dtype} -> {new_dtype}"
                )

        return "\n".join(lines)