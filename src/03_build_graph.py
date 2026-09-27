from pathlib import Path

import networkx as nx
from sqlalchemy import create_engine

from config import get_database_url


def main():
    base = Path(__file__).resolve().parents[1]
    out_dir = base / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    engine = create_engine(get_database_url())

    query = "SELECT from_addr, to_addr, amount FROM transactions"
    graph = nx.DiGraph()

    with engine.connect() as conn:
        result = conn.exec_driver_sql(query)

        for from_addr, to_addr, amount in result:
            amount = float(amount)

            if graph.has_edge(from_addr, to_addr):
                graph[from_addr][to_addr]["weight"] += amount
                graph[from_addr][to_addr]["tx_count"] += 1
            else:
                graph.add_edge(
                    from_addr,
                    to_addr,
                    weight=amount,
                    tx_count=1,
                )

    print("Graph built successfully")
    print("Nodes:", graph.number_of_nodes())
    print("Edges:", graph.number_of_edges())

    graph_path = out_dir / "tx_graph.graphml"
    nx.write_graphml(graph, graph_path)
    print("Saved graph to:", graph_path)


if __name__ == "__main__":
    main()
