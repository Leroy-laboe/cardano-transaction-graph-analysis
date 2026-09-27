from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from config import get_database_url


def main():
    base = Path(__file__).resolve().parents[1]
    csv_path = base / "data" / "tx.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            "data/tx.csv not found. Run: python src/01_make_data.py"
        )

    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    engine = create_engine(get_database_url())

    df.to_sql("transactions", engine, if_exists="append", index=False)

    with engine.connect() as conn:
        count = conn.exec_driver_sql(
            "SELECT COUNT(*) FROM transactions"
        ).scalar_one()
        print("Rows in transactions table:", count)


if __name__ == "__main__":
    main()
