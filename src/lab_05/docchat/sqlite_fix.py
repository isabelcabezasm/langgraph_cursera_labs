"""
SQLite version fix for ChromaDB compatibility.
This module ensures that ChromaDB uses a compatible SQLite version.
"""

import sys


def apply_sqlite_fix():
    """Apply SQLite version fix by replacing sqlite3 module with pysqlite3."""
    try:
        # Try to import pysqlite3 and replace sqlite3
        import pysqlite3.dbapi2 as sqlite3

        sys.modules["sqlite3"] = sqlite3
        print(f"✅ SQLite fix applied. Using SQLite version: {sqlite3.sqlite_version}")
        return True
    except ImportError:
        print(
            "❌ pysqlite3-binary not installed. Please run: pip install pysqlite3-binary"
        )
        return False


def check_sqlite_version():
    """Check if the current SQLite version is compatible with ChromaDB."""
    import sqlite3

    version = sqlite3.sqlite_version
    version_parts = [int(x) for x in version.split(".")]

    # Check if version >= 3.35.0
    required = [3, 35, 0]
    compatible = version_parts >= required

    print(f"Current SQLite version: {version}")
    print("Required version: >= 3.35.0")
    print(f"Compatible: {'✅ Yes' if compatible else '❌ No'}")

    return compatible


if __name__ == "__main__":
    print("SQLite Version Check:")
    print("-" * 40)

    # Check original version
    check_sqlite_version()

    print("\nApplying SQLite fix...")
    print("-" * 40)

    # Apply fix
    if apply_sqlite_fix():
        # Check again after fix
        check_sqlite_version()
