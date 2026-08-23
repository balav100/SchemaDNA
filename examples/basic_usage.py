"""
Basic SchemaDNA usage example.
"""

import pandas as pd

from schemadna import SchemaDNA


def main() -> None:
    dna = SchemaDNA()

    old_df = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "revenue": [100.0, 200.0, 300.0],
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

    old_fingerprint = dna.fingerprint(old_df)
    new_fingerprint = dna.fingerprint(new_df)

    print("Old schema fingerprint:")
    print(old_fingerprint)

    print("\nNew schema fingerprint:")
    print(new_fingerprint)

    result = dna.compare(old_df, new_df)

    print("\nSchema comparison:")
    print(result.summary())


if __name__ == "__main__":
    main()