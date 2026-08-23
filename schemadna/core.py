"""
High-level SchemaDNA API.

Provides a simple interface for schema fingerprinting
and schema-drift detection.
"""

from __future__ import annotations

from typing import Any

from .drift import detect_drift
from .fingerprint import fingerprint_schema
from .models import Schema, SchemaDrift


class SchemaDNA:
    """
    High-level interface for schema fingerprinting
    and schema-drift detection.
    """

    def fingerprint(self, data: Any) -> str:
        """
        Generate a deterministic fingerprint for a dataset schema.

        Parameters
        ----------
        data:
            Either a Schema object, a mapping of column names to
            data types, or a Pandas DataFrame.

        Returns
        -------
        str
            SHA-256 schema fingerprint.
        """

        schema = self._to_schema(data)

        return fingerprint_schema(schema)

    def compare(
        self,
        old_data: Any,
        new_data: Any,
    ) -> SchemaDrift:
        """
        Compare two dataset schemas.

        Returns
        -------
        SchemaDrift
            Added, removed, and modified columns.
        """

        old_schema = self._to_schema(old_data)
        new_schema = self._to_schema(new_data)

        return detect_drift(old_schema, new_schema)

    @staticmethod
    def _to_schema(data: Any) -> Schema:
        """
        Convert supported input types into a Schema object.
        """

        if isinstance(data, Schema):
            return data

        if isinstance(data, dict):
            return Schema.from_mapping(data)

        # Pandas DataFrame support
        if hasattr(data, "columns") and hasattr(data, "dtypes"):
            mapping = {
                str(column): str(dtype)
                for column, dtype in zip(
                    data.columns,
                    data.dtypes,
                )
            }

            return Schema.from_mapping(mapping)

        raise TypeError(
            "Unsupported input type. Expected a Schema, "
            "dictionary, or Pandas DataFrame."
        )