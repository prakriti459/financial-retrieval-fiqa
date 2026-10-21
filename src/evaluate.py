import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List

def compute_precision_at_k(retrieved_docs: List[str], qrel_dict: Dict[str, int], k: int = 10) -> float:
    top_k = retrieved_docs[:k]
    if not top_k:
        return 0.0
    relevant_retrieved = sum(1 for doc_id in top_k if qrel_dict.get(doc_id, 0) > 0)
    return relevant_retrieved / k

def compute_recall_at_k(retrieved_docs: List[str], qrel_dict: Dict[str, int], k: int = 100) -> float:
    total_relevant = sum(1 for rel in qrel_dict.values() if rel > 0)
    if total_relevant == 0:
        return 0.0
    top_k = retrieved_docs[:k]
    relevant_retrieved = sum(1 for doc_id in top_k if qrel_dict.get(doc_id, 0) > 0)
    return relevant_retrieved / total_relevant

def compute_average_precision(retrieved_docs: List[str], qrel_dict: Dict[str, int]) -> float:
    total_relevant = sum(1 for rel in qrel_dict.values() if rel > 0)
    if total_relevant == 0:
        return 0.0
    hits = 0
    sum_precisions = 0.0
    for rank, doc_id in enumerate(retrieved_docs, start=1):
        if qrel_dict.get(doc_id, 0) > 0:
            hits += 1
            sum_precisions += hits / rank
    return sum_precisions / total_relevant

def compute_ndcg_at_k(retrieved_docs: List[str], qrel_dict: Dict[str, int], k: int = 10) -> float:
    top_k = retrieved_docs[:k]
    dcg = 0.0
    for i, doc_id in enumerate(top_k):
        rel = qrel_dict.get(doc_id, 0)
        if rel > 0:
            dcg += (2**rel - 1) / math.log2(i + 2)

    ideal_rels = sorted(qrel_dict.values(), reverse=True)[:k]
    idcg = sum((2**rel - 1) / math.log2(i + 2) for i, rel in enumerate(ideal_rels))
    return (dcg / idcg) if idcg > 0 else 0.0

def evaluate_retrieval_run(results: Dict[str, List[str]], qrels_dict: Dict[str, Dict[str, int]]) -> Dict[str, float]:
    p10_list, r100_list, ap_list, ndcg10_list = [], [], [], []
    eval_qids = [qid for qid in results if qid in qrels_dict]

    for qid in eval_qids:
        ranked = results[qid]
        qrel_q = qrels_dict[qid]
        p10_list.append(compute_precision_at_k(ranked, qrel_q, k=10))
        r100_list.append(compute_recall_at_k(ranked, qrel_q, k=100))
        ap_list.append(compute_average_precision(ranked, qrel_q))
        ndcg10_list.append(compute_ndcg_at_k(ranked, qrel_q, k=10))

    return {
        "Precision@10": round(float(np.mean(p10_list)), 4),
        "Recall@100": round(float(np.mean(r100_list)), 4),
        "MAP": round(float(np.mean(ap_list)), 4),
        "nDCG@10": round(float(np.mean(ndcg10_list)), 4)
    }

def compute_11_point_pr(results_dict: Dict[str, List[str]], qrels_dict: Dict[str, Dict[str, int]]) -> np.ndarray:
    recall_levels = np.linspace(0.0, 1.0, 11)
    all_query_interpolated = []

    for qid in results_dict:
        if qid not in qrels_dict:
            continue
        ranked_docs = results_dict[qid]
        qrel_for_q = qrels_dict[qid]
        total_relevant = sum(1 for score in qrel_for_q.values() if score > 0)
        if total_relevant == 0:
            continue

        precisions, recalls = [], []
        hits = 0
        for rank, doc_id in enumerate(ranked_docs, start=1):
            if qrel_for_q.get(doc_id, 0) > 0:
                hits += 1
                precisions.append(hits / rank)
                recalls.append(hits / total_relevant)

        if not precisions:
            all_query_interpolated.append(np.zeros(11))
            continue

        interpolated = []
        for r_target in recall_levels:
            valid_p = [p for p, r in zip(precisions, recalls) if r >= r_target]
            interpolated.append(max(valid_p) if valid_p else 0.0)
        all_query_interpolated.append(interpolated)

    return np.mean(all_query_interpolated, axis=0)

def plot_precision_recall_curves(models_results: Dict[str, Dict[str, List[str]]], qrels_dict: Dict, save_dir: str = "figures") -> str:
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "precision_recall_graph.png")
    recall_levels = np.linspace(0.0, 1.0, 11)

    colors = {
        "TF-IDF": ("#7f7f7f", "--", "s"),
        "BM25": ("#1f77b4", "-", "o"),
        "Sentence Transformer": ("#2ca02c", "-", "^"),
        "Hybrid RRF": ("#d62728", "-", "D")
    }

    plt.figure(figsize=(9, 6))
    for model_name, results in models_results.items():
        color, linestyle, marker = colors.get(model_name, ("#333333", "-", "x"))
        pr_curve = compute_11_point_pr(results, qrels_dict)
        plt.plot(recall_levels, pr_curve, marker=marker, linestyle=linestyle, color=color, linewidth=2.0, label=model_name)

    plt.title("11-Point Interpolated Precision-Recall Graph on FiQA Benchmark", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Recall", fontsize=11, fontweight='bold')
    plt.ylabel("Interpolated Precision", fontsize=11, fontweight='bold')
    plt.xticks(recall_levels, [f"{r:.1f}" for r in recall_levels])
    plt.ylim(0.0, 0.60)
    plt.xlim(0.0, 1.0)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10.5, loc='upper right')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"📈 Precision-Recall graph saved to: {save_path}")
    return save_path

def plot_model_comparison_barchart(all_metrics: Dict[str, Dict[str, float]], save_dir: str = "figures") -> str:
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "model_performance_comparison.png")

    models = list(all_metrics.keys())
    metrics_keys = ["Precision@10", "Recall@100", "MAP", "nDCG@10"]
    colors = ["#7f7f7f", "#1f77b4", "#2ca02c", "#d62728"]

    data_matrix = np.array([[all_metrics[m][k] for k in metrics_keys] for m in models])
    x = np.arange(len(metrics_keys))
    width = 0.20

    fig, ax = plt.subplots(figsize=(11, 5.5))
    for i, (m_name, color) in enumerate(zip(models, colors)):
        rects = ax.bar(x + i*width, data_matrix[i], width, label=m_name, color=color, edgecolor="black", alpha=0.85)
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f"{height:.3f}",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=7.5, fontweight="bold")

    ax.set_title("Comparative Retrieval Performance across Evaluation Metrics on FiQA", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylabel("Metric Score", fontsize=10, fontweight="bold")
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(metrics_keys, fontsize=10, fontweight="bold")
    ax.legend(fontsize=9.5, loc="upper left")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.set_ylim(0, 0.85)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📊 Performance comparison bar chart saved to: {save_path}")
    return save_path
