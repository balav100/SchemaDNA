from schemadna import SchemaDNA


def test_same_schema_has_same_fingerprint():
    dna = SchemaDNA()

    schema = {
        "customer_id": "int64",
        "name": "object",
        "age": "int64",
    }

    fingerprint_1 = dna.fingerprint(schema)
    fingerprint_2 = dna.fingerprint(schema)

    assert fingerprint_1 == fingerprint_2


def test_column_order_does_not_change_fingerprint():
    dna = SchemaDNA()

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


def test_different_schema_has_different_fingerprint():
    dna = SchemaDNA()

    schema_a = {
        "customer_id": "int64",
        "name": "object",
    }

    schema_b = {
        "customer_id": "int64",
        "name": "object",
        "age": "int64",
    }

    assert dna.fingerprint(schema_a) != dna.fingerprint(schema_b)