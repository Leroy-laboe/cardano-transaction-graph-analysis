from pathlib import Path
import pandas as pd

def top_percent_threshold(series, pct=0.01):
    # threshold for top X% values
    return series.quantile(1 - pct)

def main():
    base = Path(__file__).resolve().parents[1]
    out_dir = base / "outputs"

    metrics_path = out_dir / "node_metrics.csv"
    df = pd.read_csv(metrics_path)

    # compute thresholds for top 1%
    out_deg_thr = top_percent_threshold(df["out_degree"], pct=0.01)
    in_deg_thr = top_percent_threshold(df["in_degree"], pct=0.01)
    pr_thr = top_percent_threshold(df["pagerank"], pct=0.01)

    # flags
    df["flag_high_out_degree"] = df["out_degree"] >= out_deg_thr
    df["flag_high_in_degree"] = df["in_degree"] >= in_deg_thr
    df["flag_high_pagerank"] = df["pagerank"] >= pr_thr

    # suspicious score (simple)
    df["suspicious_score"] = (
        df["flag_high_out_degree"].astype(int)
        + df["flag_high_in_degree"].astype(int)
        + df["flag_high_pagerank"].astype(int)
    )

    suspicious = df[df["suspicious_score"] > 0].copy()
    suspicious = suspicious.sort_values(
        ["suspicious_score", "pagerank", "out_degree", "in_degree"],
        ascending=False
    )

    # add a "reason" column
    def reason(row):
        reasons = []
        if row["flag_high_out_degree"]:
            reasons.append("high_out_degree")
        if row["flag_high_in_degree"]:
            reasons.append("high_in_degree")
        if row["flag_high_pagerank"]:
            reasons.append("high_pagerank")
        return ",".join(reasons)

    suspicious["reason"] = suspicious.apply(reason, axis=1)

    suspicious.to_csv(out_dir / "suspicious.csv", index=False)

    print("✅ Saved outputs/suspicious.csv")
    print("Suspicious threshold values:")
    print("out_degree >= ", out_deg_thr)
    print("in_degree >= ", in_deg_thr)
    print("pagerank >= ", pr_thr)

    print("\nTop 10 suspicious nodes:")
    print(suspicious.head(10)[["address", "in_degree", "out_degree", "pagerank", "suspicious_score", "reason"]])

if __name__ == "__main__":
    main()
