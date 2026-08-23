# SchemaDNA

Python package for deterministic schema fingerprinting and automated schema-drift detection.

SchemaDNA helps data engineers and developers track dataset structure across versions by identifying added columns, removed columns, and data-type modifications.

## Features

- Deterministic SHA-256 schema fingerprinting
- Column-order-independent fingerprints
- Added-column detection
- Removed-column detection
- Data-type modification detection
- Pandas DataFrame support
- Human-readable schema-drift summaries
- Lightweight Python API
- Automated test coverage
- Installable as a standard Python package

## Installation

Install SchemaDNA from PyPI:

    pip install schemadna

## Quick Start

    import pandas as pd

    from schemadna import SchemaDNA

    dna = SchemaDNA()

    old_df = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        }
    )

    new_df = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25.5, 30.5, 35.5],
            "email": [
                "alice@example.com",
                "bob@example.com",
                "charlie@example.com",
            ],
        }
    )

    result = dna.compare(old_df, new_df)

    print(result.summary())

Output:

    Schema Drift Detected

    Added columns:
      + email (str)

    Modified columns:
      ~ age: int64 -> float64

## Schema Fingerprinting

SchemaDNA generates a deterministic SHA-256 fingerprint from a normalized schema.

    from schemadna import SchemaDNA

    dna = SchemaDNA()

    schema = {
        "customer_id": "int64",
        "name": "object",
        "age": "int64",
    }

    fingerprint = dna.fingerprint(schema)

    print(fingerprint)

A fingerprint is useful for quickly determining whether a dataset schema has changed between versions.

### Column Order Independence

Column ordering does not affect the generated fingerprint.

    schema_a = {
        "customer_id": "int64",
        "name": "object",
        "age": "int64",
    }

    schema_b = {
        "age": "int64",
        "customer_id": "int64",
        "name": "object",
    }

    assert dna.fingerprint(schema_a) == dna.fingerprint(schema_b)

## Schema Drift Detection

SchemaDNA compares two schema versions and categorizes structural changes.

### Added Columns

    old_schema = {
        "id": "int64",
    }

    new_schema = {
        "id": "int64",
        "email": "object",
    }

    result = dna.compare(old_schema, new_schema)

    print(result.added)

### Removed Columns

    old_schema = {
        "id": "int64",
        "email": "object",
    }

    new_schema = {
        "id": "int64",
    }

    result = dna.compare(old_schema, new_schema)

    print(result.removed)

### Modified Data Types

    old_schema = {
        "id": "int64",
        "age": "int64",
    }

    new_schema = {
        "id": "int64",
        "age": "float64",
    }

    result = dna.compare(old_schema, new_schema)

    print(result.modified)

Output:

    {'age': ('int64', 'float64')}

## Supported Input Types

The SchemaDNA API currently accepts:

### Dictionary

    schema = {
        "id": "int64",
        "name": "object",
    }

### Schema Object

    from schemadna import Schema

    schema = Schema.from_mapping(
        {
            "id": "int64",
            "name": "object",
        }
    )

### Pandas DataFrame

    import pandas as pd

    df = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["Alice", "Bob"],
        }
    )

    fingerprint = dna.fingerprint(df)

## API

### SchemaDNA()

Creates the main SchemaDNA interface.

### dna.fingerprint(data)

Generates a deterministic SHA-256 fingerprint for the supplied schema.

### dna.compare(old_data, new_data)

Compares two schema versions.

Returns a SchemaDrift object containing:

    added
    removed
    modified
    has_drift

### result.summary()

Returns a human-readable description of detected schema changes.

## Example Workflow

A typical data-engineering workflow can use SchemaDNA before processing a new dataset version:

    Dataset Version N
           |
           v
    Schema Extraction
           |
           v
    Schema Fingerprint
           |
           v
    Dataset Version N+1
           |
           v
    Schema Extraction
           |
           v
    Schema Comparison
           |
           +-----------------------+
           |                       |
       No Drift                Drift Found
           |                       |
           v                       v
    Continue Pipeline       Inspect Changes

This can be integrated into ETL/ELT pipelines, data validation workflows, and CI/CD checks.

## Development

Clone the repository:

    git clone https://github.com/balav100/SchemaDNA.git
    cd SchemaDNA

Create a virtual environment:

    python -m venv .venv

Activate it on Windows:

    .venv\Scripts\Activate.ps1

Install development dependencies:

    python -m pip install -e ".[dev]"

## Testing

Run the complete test suite:

    pytest -v

The project includes automated tests covering:

- Schema fingerprint consistency
- Column-order independence
- Different schema fingerprints
- Added columns
- Removed columns
- Modified data types
- Multiple simultaneous schema changes
- Pandas DataFrame comparison
- Empty schemas
- Invalid input types

## Project Structure

    SchemaDNA/
    │
    ├── schemadna/
    │   ├── __init__.py
    │   ├── core.py
    │   ├── models.py
    │   ├── fingerprint.py
    │   └── drift.py
    │
    ├── tests/
    │   ├── test_fingerprint.py
    │   └── test_drift.py
    │
    ├── examples/
    │   └── basic_usage.py
    │
    ├── README.md
    ├── LICENSE
    ├── pyproject.toml
    └── .gitignore

## Requirements

- Python 3.9+
- Pandas 2.0+

## License

SchemaDNA is released under the MIT License.

## Author

Balasubramaniam V

GitHub: https://github.com/balav100

