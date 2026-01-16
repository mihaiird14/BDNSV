import time
import streamlit as st
import pandas as pd

from neo4j import GraphDatabase
from neo4j.graph import Node, Relationship, Path
from pyvis.network import Network
import streamlit.components.v1 as components


import config

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="LinkedIn Graph Traversal",
    layout="wide"
)

st.title("LinkedIn – Graph Traversal UI")
st.caption("Input a node → run traversal → visualize subgraph")

# ---------------- NEO4J ----------------
@st.cache_resource
def get_driver():
    return GraphDatabase.driver(
        config.URI,
        auth=(config.USER, config.PASSWORD)
    )

driver = get_driver()

def run_query(query, params=None, raw=False):
    with driver.session() as session:
        start = time.time()
        result = session.run(query, params or {})
        ms = (time.time() - start) * 1000
        if raw:
            return list(result), ms
        return [r.data() for r in result], ms

# ---------------- GRAPH HELPERS ----------------
COLORS = {
    "User": "#1f77b4",
    "Company": "#ff7f0e",
    "University": "#2ca02c",
    "Project": "#d62728",
    "Certification": "#9467bd",
    "Post": "#8c564b",
}

def node_label(node: Node):
    labels = list(node.labels)
    ntype = labels[0] if labels else "Node"
    label = node.get("name") or node.get("id") or ntype
    return str(label), ntype

def extract_graph(records):
    nodes = {}
    rels = {}

    def handle(v):
        if v is None:
            return
        if isinstance(v, Node):
            nodes[v.element_id] = v
        elif isinstance(v, Relationship):
            rels[v.element_id] = v
            nodes[v.start_node.element_id] = v.start_node
            nodes[v.end_node.element_id] = v.end_node
        elif isinstance(v, Path):
            for n in v.nodes:
                nodes[n.element_id] = n
            for r in v.relationships:
                rels[r.element_id] = r
        elif isinstance(v, list):
            for x in v:
                handle(x)
        elif isinstance(v, dict):
            for x in v.values():
                handle(x)

    for rec in records:
        for k in rec.keys():
            handle(rec[k])

    return list(nodes.values()), list(rels.values())

def draw_graph(nodes, rels, height=600):
    net = Network(height=f"{height}px", width="100%", directed=True)

    for n in nodes:
        label, ntype = node_label(n)
        net.add_node(
            n.element_id,
            label=label,
            title=str(dict(n)),
            color=COLORS.get(ntype, "#999999"),
            size=28 if ntype == "User" else 20,
        )

    for r in rels:
        net.add_edge(
            r.start_node.element_id,
            r.end_node.element_id,
            label=r.type,
            arrows="to"
        )

    html = net.generate_html()
    components.html(html, height=height)

    return len(nodes), len(rels)

# ---------------- DATA ----------------
users, _ = run_query("""
MATCH (u:User)
RETURN u.id AS id, u.name AS name
ORDER BY name
""")

if not users:
    st.error("Nu există noduri :User. Rulează notebook-ul pentru a încărca datele.")
    st.stop()

user_ids = [u["id"] for u in users]
id_to_name = {u["id"]: u["name"] for u in users}

# ---------------- UI ----------------
mode = st.sidebar.radio(
    "Traversal type",
    ["K-hop neighborhood", "Friends-of-friends", "Shortest path"]
)

# ---------- 1) K-hop ----------
if mode == "K-hop neighborhood":
    st.subheader("K-hop neighborhood")

    user_id = st.selectbox(
        "User",
        user_ids,
        format_func=lambda x: f"{id_to_name[x]} ({x})"
    )
    depth = st.slider("Depth", 1, 3, 2)
    limit = st.slider("Limit paths", 5, 50, 25)

    if st.button("Run traversal", type="primary"):
        query = f"""
        MATCH p = (u:User {{id:$id}})-[*1..{depth}]-(n)
        RETURN p
        LIMIT $limit
        """
        records, ms = run_query(query, {"id": user_id, "limit": limit}, raw=True)

        nodes, rels = extract_graph(records)
        nN, nE = draw_graph(nodes, rels)

        c1, c2, c3 = st.columns(3)
        c1.metric("Exec time", f"{ms:.2f} ms")
        c2.metric("Nodes", nN)
        c3.metric("Edges", nE)

# ---------- 2) Friends of friends ----------
elif mode == "Friends-of-friends":
    st.subheader("Friends-of-friends")

    user_id = st.selectbox(
        "User",
        user_ids,
        format_func=lambda x: f"{id_to_name[x]} ({x})"
    )

    if st.button("Run traversal", type="primary"):
        query = """
        MATCH p = (u:User {id:$id})-[:FOLLOWS]->(:User)-[:FOLLOWS]->(rec:User)
        WHERE NOT (u)-[:FOLLOWS]->(rec) AND u.id <> rec.id
        RETURN p
        LIMIT 25
        """
        records, ms = run_query(query, {"id": user_id}, raw=True)

        nodes, rels = extract_graph(records)
        nN, nE = draw_graph(nodes, rels)

        c1, c2, c3 = st.columns(3)
        c1.metric("Exec time", f"{ms:.2f} ms")
        c2.metric("Nodes", nN)
        c3.metric("Edges", nE)

# ---------- 3) Shortest path ----------
else:
    st.subheader("Shortest path")

    start = st.selectbox(
        "Start user",
        user_ids,
        format_func=lambda x: f"{id_to_name[x]} ({x})"
    )
    end = st.selectbox(
        "End user",
        user_ids,
        index=1,
        format_func=lambda x: f"{id_to_name[x]} ({x})"
    )
    maxlen = st.slider("Max length", 2, 8, 6)

    if st.button("Run traversal", type="primary"):
        query = f"""
        MATCH (a:User {{id:$a}}), (b:User {{id:$b}})
        MATCH p = shortestPath((a)-[:FOLLOWS*..{maxlen}]->(b))
        RETURN p
        """
        records, ms = run_query(query, {"a": start, "b": end}, raw=True)

        if not records or records[0]["p"] is None:
            st.warning("Nu există path.")
        else:
            p = records[0]["p"]
            st.success(f"Hops: {len(p.relationships)}")

            nodes, rels = extract_graph(records)
            nN, nE = draw_graph(nodes, rels, height=450)

            c1, c2, c3 = st.columns(3)
            c1.metric("Exec time", f"{ms:.2f} ms")
            c2.metric("Nodes", nN)
            c3.metric("Edges", nE)
