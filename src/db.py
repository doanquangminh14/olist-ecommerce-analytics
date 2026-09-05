import sys
from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .config import DATABASE_URL, SQL_DIR


_engine: Optional[Engine] = None


def get_engine() -> Engine:
    """
    Returns a singleton SQLAlchemy engine connected to PostgreSQL.
    """
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    return _engine


def test_connection() -> bool:
    """
    Tests database connectivity.
    """
    engine = get_engine()
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
            print("[OK] Ket noi thanh cong toi co so du lieu PostgreSQL!")
            return True
    except Exception as e:
        print(f"[WARN] Ket noi co so du lieu that bai: {e}")
        return False


def execute_sql_file(sql_file_path: Path, engine: Optional[Engine] = None) -> None:
    """
    Executes a multi-statement SQL script file against the database.
    """
    if engine is None:
        engine = get_engine()

    if not sql_file_path.exists():
        raise FileNotFoundError(f"[ERROR] Khong tim thay file SQL: {sql_file_path}")

    print(f"  [EXEC] Dang thuc thi script: {sql_file_path.name}...")
    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    with engine.connect() as conn:
        with conn.begin():
            conn.execute(text(sql_content))

    print(f"  [OK] Da thuc thi thanh cong: {sql_file_path.name}")


def setup_database_schemas_and_views(engine: Optional[Engine] = None) -> None:
    """
    Executes all SQL files in sql/ directory in sequence:
    1. create_db.sql (Staging tables & schemas)
    2. create_indx.sql (B-Tree indexes)
    3. create_view.sql (Star schema analytics views)
    """
    if engine is None:
        engine = get_engine()

    print("=" * 70)
    print("[DATABASE SETUP] THUC THI SCRIPTS TAO SCHEMA, BANG, INDEX & VIEWS")
    print("=" * 70)

    execute_sql_file(SQL_DIR / "create_db.sql", engine)
    execute_sql_file(SQL_DIR / "create_indx.sql", engine)
    execute_sql_file(SQL_DIR / "create_view.sql", engine)

    print("[OK] Da thiet lap hoan tat toan bo Database Schema, Indexes va Views!\n")
