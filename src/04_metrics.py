from pathlib import Path
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def main():
    base = Path(__file__).resolve().parents[1]
    out_dir = base / "outputs"
    graph_path = out_dir / "tx_graph.graphml"

    # Load graph built in Step 3
    G = nx.read_graphml(graph_path)

    # Degrees
    in_deg = dict(G.in_degree())
    out_deg = dict(G.out_degree())

    # PageRank using edge weight (amount aggregated)
    pagerank = nx.pagerank(G, weight="weight")

    # Build metrics table
    df = pd.DataFrame({
        "address": list(G.nodes()),
        "in_degree": [in_deg[n] for n in G.nodes()],
        "out_degree": [out_deg[n] for n in G.nodes()],
        "pagerank": [pagerank[n] for n in G.nodes()],
    })

    # Sort by pagerank (descending)
    df_sorted = df.sort_values("pagerank", ascending=False)

    # Save outputs
    df.to_csv(out_dir / "node_metrics.csv", index=False)
    df_sorted.head(20).to_csv(out_dir / "top20_pagerank.csv", index=False)

    print("✅ Saved outputs/node_metrics.csv")
    print("✅ Saved outputs/top20_pagerank.csv")
    print("Top 5 by PageRank:")
    print(df_sorted.head(5))

    # Plot degree distribution (out-degree)
    plt.figure()
    df["out_degree"].plot(kind="hist", bins=50)
    plt.xlabel("Out-degree")
    plt.ylabel("Count of addresses")
    plt.title("Out-degree distribution")
    plt.savefig(out_dir / "degree_distribution.png", dpi=200)
    plt.close()

    print("✅ Saved outputs/degree_distribution.png")

if __name__ == "__main__":
    main()
