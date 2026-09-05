"""
Olist E-Commerce Analytics Pipeline Entrypoint
"""

from src.pipeline import parse_args, run_pipeline

if __name__ == "__main__":
    args = parse_args()
    run_pipeline(
        skip_db=args.skip_db,
        run_sql_setup=args.run_sql_setup,
        clean_only=args.clean_only,
        verify_db_only=args.verify_db,
    )
