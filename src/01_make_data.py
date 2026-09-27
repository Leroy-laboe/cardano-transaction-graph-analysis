import random
import string
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


def rand_addr(n=42):
    """Generate a synthetic Cardano-style address label."""
    return "addr_" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=n)
    )


def rand_txid(n=64):
    """Generate a synthetic hexadecimal transaction ID."""
    return "".join(random.choices("0123456789abcdef", k=n))


def generate_tx(num_txs=80000, num_addrs=12000, start_days_ago=45):
    """Generate a reproducible synthetic transaction network."""
    random.seed(42)

    addresses = [rand_addr() for _ in range(num_addrs)]
    start_time = datetime.now() - timedelta(days=start_days_ago)
    rows = []

    for _ in range(num_txs):
        tx_id = rand_txid()
        timestamp = start_time + timedelta(
            seconds=random.randint(0, start_days_ago * 24 * 3600)
        )

        from_addr = random.choice(addresses)

        # Introduce a small set of higher-activity synthetic hubs.
        if random.random() < 0.02:
            hub_count = max(1, int(num_addrs * 0.02))
            from_addr = addresses[random.randrange(hub_count)]

        to_addr = random.choice(addresses)
        while to_addr == from_addr:
            to_addr = random.choice(addresses)

        amount = round(random.random() * 1000, 6)

        rows.append(
            {
                "tx_id": tx_id,
                "timestamp": timestamp.isoformat(timespec="seconds"),
                "from_addr": from_addr,
                "to_addr": to_addr,
                "amount": amount,
            }
        )

    return pd.DataFrame(rows)


def main():
    df = generate_tx()
    out_path = Path(__file__).resolve().parents[1] / "data" / "tx.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    print(f"Wrote {len(df):,} synthetic transactions to {out_path}")
    print(df.head())


if __name__ == "__main__":
    main()
