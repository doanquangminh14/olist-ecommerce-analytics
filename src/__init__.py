"""
Olist E-Commerce Analytics - ETL Package
"""

import sys

# Ensure UTF-8 output encoding on Windows console
if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .config import *
