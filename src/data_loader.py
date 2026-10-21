import os
import json
import csv
import zipfile
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Tuple

DATASET_NAME = "fiqa"
DATASET_URL = f"https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{DATASET_NAME}.zip"

def download_and_extract_fiqa(data_dir: str = "data") -> str:
    """Downloads and extracts the FiQA dataset from official BEIR mirror."""
    os.makedirs(data_dir, exist_ok=True)
    dataset_folder = os.path.join(data_dir, DATASET_NAME)
    zip_path = os.path.join(data_dir, f"{DATASET_NAME}.zip")

    if not os.path.exists(dataset_folder):
        if not os.path.exists(zip_path):
            print(f"[INFO] Downloading FiQA dataset (~18MB) from {DATASET_URL}...")
            response = requests.get(DATASET_URL, stream=True)
            response.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=16384):
                    if chunk:
                        f.write(chunk)
            print("[OK] Download completed.")

        print(f"[INFO] Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(data_dir)
        print("[OK] Extraction completed.")

    return dataset_folder

def load_fiqa(data_dir: str = "data", split: str = "test") -> Tuple[Dict[str, Dict[str, str]], Dict[str, str], Dict[str, Dict[str, int]]]:
    """
    Loads FiQA corpus, queries, and ground truth relevance for the test split.
    Returns:
        corpus: Dict[doc_id, {"title": str, "text": str}]
        queries: Dict[query_id, query_text]
        qrels: Dict[query_id, Dict[doc_id, score]]
    """
    dataset_folder = download_and_extract_fiqa(data_dir)

    # 1. Load Corpus
    corpus_path = os.path.join(dataset_folder, "corpus.jsonl")
    corpus = {}
    print(f"[INFO] Loading corpus from {corpus_path}...")
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            corpus[item["_id"]] = {
                "title": item.get("title") or "",
                "text": item.get("text") or ""
            }
    print(f" Loaded {len(corpus):,} documents in corpus.")

    # 2. Load Queries
    queries_path = os.path.join(dataset_folder, "queries.jsonl")
    queries = {}
    with open(queries_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            queries[item["_id"]] = item.get("text") or ""

    # 3. Load Qrels
    qrels_path = os.path.join(dataset_folder, "qrels", f"{split}.tsv")
    qrels = {}
    with open(qrels_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        for row in reader:
            if len(row) >= 3:
                qid, doc_id, score = row[0], row[1], int(row[2])
                if qid not in qrels:
                    qrels[qid] = {}
                qrels[qid][doc_id] = score

    # Filter to annotated test queries
    test_queries = {qid: queries[qid] for qid in qrels if qid in queries}
    print(f" Loaded {len(test_queries):,} evaluation test queries with {sum(len(v) for v in qrels.values()):,} annotations.")

    return corpus, test_queries, qrels

def generate_dataset_visualizations(corpus: Dict, queries: Dict, qrels: Dict, save_dir: str = "figures") -> str:
    """Generates and saves the Section 2.1 visualization plots."""
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "fiqa_dataset_visualization.png")

    doc_lengths = [len((doc["title"] + " " + doc["text"]).split()) for doc in corpus.values()]
    relevant_counts = [len(rel_docs) for rel_docs in qrels.values()]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Graph A: Document length distribution
    axes[0].hist(doc_lengths, bins=40, range=(0, 400), color="#1f77b4", edgecolor="black", alpha=0.75)
    axes[0].set_title("Distribution of Document Lengths in FiQA", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Document Length (Words)", fontsize=11)
    axes[0].set_ylabel("Number of Documents", fontsize=11)
    axes[0].axvline(np.mean(doc_lengths), color="red", linestyle="--", linewidth=1.5, label=f"Mean: {np.mean(doc_lengths):.1f}")
    axes[0].axvline(np.median(doc_lengths), color="black", linestyle=":", linewidth=1.5, label=f"Median: {int(np.median(doc_lengths))}")
    axes[0].legend(fontsize=10)
    axes[0].grid(axis="y", linestyle="--", alpha=0.5)

    # Graph B: Relevant documents per query
    rel_counts_series = pd.Series(relevant_counts).value_counts().sort_index()
    axes[1].bar(rel_counts_series.index, rel_counts_series.values, color="#ff7f0e", edgecolor="black", alpha=0.75, width=0.6)
    axes[1].set_title("Relevant Documents per Query Distribution", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Number of Relevant Documents Annotated", fontsize=11)
    axes[1].set_ylabel("Number of Queries", fontsize=11)
    axes[1].set_xticks(range(1, min(16, max(relevant_counts) + 1)))
    axes[1].grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📊 Dataset visualization saved to: {save_path}")
    return save_path

if __name__ == "__main__":
    corpus, queries, qrels = load_fiqa()
    generate_dataset_visualizations(corpus, queries, qrels)
