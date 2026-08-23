from schemadna import SchemaDNA


def test_no_drift():
    dna = SchemaDNA()

    schema = {
        "id": "int64",
        "name": "object",
    }

    result = dna.compare(schema, schema)

    assert result.has_drift is False
    assert result.added == []
    assert result.removed == []
    assert result.modified == {}


def test_added_column():
    dna = SchemaDNA()

    old_schema = {
        "id": "int64",
        "name": "object",
    }

    new_schema = {
        "id": "int64",
        "name": "object",
        "email": "object",
    }

    result = dna.compare(old_schema, new_schema)

    assert result.has_drift is True
    assert [column.name for column in result.added] == ["email"]
    assert result.removed == []
    assert result.modified == {}


def test_removed_column():
    dna = SchemaDNA()

    old_schema = {
        "id": "int64",
        "name": "object",
        "email": "object",
    }

    new_schema = {
        "id": "int64",
        "name": "object",
    }

    result = dna.compare(old_schema, new_schema)

    assert result.has_drift is True
    assert [column.name for column in result.removed] == ["email"]
    assert result.added == []
    assert result.modified == {}


def test_modified_column_dtype():
    dna = SchemaDNA()

    old_schema = {
        "id": "int64",
        "age": "int64",
    }

    new_schema = {
        "id": "int64",
        "age": "float64",
    }

    result = dna.compare(old_schema, new_schema)

    assert result.has_drift is True
    assert result.modified == {
        "age": ("int64", "float64")
    }


def test_multiple_schema_changes():
    dna = SchemaDNA()

    old_schema = {
        "id": "int64",
        "name": "object",
        "age": "int64",
        "revenue": "float64",
    }

    new_schema = {
        "id": "int64",
        "name": "object",
        "age": "float64",
        "email": "object",
    }

    result = dna.compare(old_schema, new_schema)

    assert result.has_drift is True

    assert [column.name for column in result.added] == [
        "email"
    ]

    assert [column.name for column in result.removed] == [
        "revenue"
    ]

    assert result.modified == {
        "age": ("int64", "float64")
    }


def test_pandas_dataframe_comparison():
    import pandas as pd

    dna = SchemaDNA()

    old_df = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["A", "B"],
            "age": [20, 30],
        }
    )

    new_df = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["A", "B"],
            "age": [20.5, 30.5],
            "email": ["a@test.com", "b@test.com"],
        }
    )

    result = dna.compare(old_df, new_df)

    assert result.has_drift is True
    assert [column.name for column in result.added] == [
        "email"
    ]
    assert result.modified == {
        "age": ("int64", "float64")
    }

def test_empty_schema_has_no_drift():
    dna = SchemaDNA()

    old_schema = {}
    new_schema = {}

    result = dna.compare(old_schema, new_schema)

    assert result.has_drift is False
    assert result.added == []
    assert result.removed == []
    assert result.modified == {}


def test_empty_to_non_empty_schema():
    dna = SchemaDNA()

    old_schema = {}

    new_schema = {
        "id": "int64",
        "name": "object",
    }

    result = dna.compare(old_schema, new_schema)

    assert result.has_drift is True
    assert [column.name for column in result.added] == [
        "id",
        "name",
    ]


def test_non_empty_to_empty_schema():
    dna = SchemaDNA()

    old_schema = {
        "id": "int64",
        "name": "object",
    }

    new_schema = {}

    result = dna.compare(old_schema, new_schema)

    assert result.has_drift is True
    assert [column.name for column in result.removed] == [
        "id",
        "name",
    ]


def test_invalid_input_type():
    dna = SchemaDNA()

    try:
        dna.fingerprint(["invalid", "input"])
    except TypeError as error:
        assert "Unsupported input type" in str(error)
    else:
        raise AssertionError("Expected TypeError was not raised")