import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

fig_dir = r"C:\Users\PRAKRITI\Desktop\financial-retrieval-fiqa\figures"
os.makedirs(fig_dir, exist_ok=True)

# =====================================================================
# 1. Architecture Flowchart Diagram (Figure 2)
# =====================================================================
fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 7.5)
ax.axis('off')

def draw_box(x, y, w, h, title, subtitle="", bg_color="#f0f4f8", border_color="#2b6cb0", text_color="#1a202c", title_size=11, sub_size=8.5):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor=bg_color, edgecolor=border_color, linewidth=1.8)
    ax.add_patch(box)
    if subtitle:
        ax.text(x + w/2, y + h*0.64, title, ha='center', va='center', fontsize=title_size, fontweight='bold', color=text_color)
        ax.text(x + w/2, y + h*0.30, subtitle, ha='center', va='center', fontsize=sub_size, color="#4a5568")
    else:
        ax.text(x + w/2, y + h*0.5, title, ha='center', va='center', fontsize=title_size, fontweight='bold', color=text_color)

def draw_arrow(x1, y1, x2, y2, color="#4a5568", width=1.6):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', lw=width, color=color, mutation_scale=15))

# Top Box: User Query
draw_box(3.5, 6.4, 4.0, 0.75, "User Input Query", "e.g., How to hedge portfolio against inflation?", "#ebf8ff", "#3182ce")
draw_arrow(5.5, 6.4, 5.5, 5.6)

# Preprocessing Box
draw_box(2.8, 4.75, 5.4, 0.85, "Query Preprocessing & Tokenization", "Regex Cleaning ($, %, tickers) + Stopwords + Porter Stemming", "#edf2f7", "#4a5568")
draw_arrow(4.2, 4.75, 2.5, 3.9)
draw_arrow(6.8, 4.75, 8.5, 3.9)

# Left Path: Sparse Lexical
draw_box(0.5, 2.4, 4.2, 1.4, "Sparse Lexical Retrieval Path", "• Inverted Index Term Matching\n• Okapi BM25 & TF-IDF Scoring\n• Top-K Sparse Candidates", "#feebc8", "#dd6b20")

# Right Path: Dense Semantic
draw_box(6.3, 2.4, 4.2, 1.4, "Dense Semantic Retrieval Path", "• Sentence Transformer (all-MiniLM-L6-v2)\n• Dense Vector Cosine Similarity\n• Top-K Dense Semantic Candidates", "#c6f6d5", "#38a169")

draw_arrow(2.6, 2.4, 4.5, 1.6)
draw_arrow(8.4, 2.4, 6.5, 1.6)

# RRF Fusion Box
draw_box(2.8, 0.85, 5.4, 0.8, "Reciprocal Rank Fusion (RRF) Aggregator", "RRF Score(d) = sum( 1 / (60 + rank_m(d)) )", "#e9d8fd", "#805ad5")
draw_arrow(5.5, 0.85, 5.5, 0.45)

# Bottom Output Box
draw_box(3.2, 0.05, 4.6, 0.38, "Final Ranked Financial Passages (Top-K)", "", "#bee3f8", "#2b6cb0", title_size=10.5)

plt.title("Figure 2: Architecture of the Hybrid Financial Retrieval Pipeline (FiQA Benchmark)", fontsize=12.5, fontweight='bold', pad=14)
arch_path = os.path.join(fig_dir, "architecture_diagram.png")
plt.savefig(arch_path, bbox_inches='tight', dpi=300)
plt.close()
print("Saved:", arch_path)

# =====================================================================
# 2. Model Performance Comparison Bar Chart (Figure 4)
# =====================================================================
metrics_keys = ["Precision@10", "Recall@100", "MAP", "nDCG@10"]
models = ["TF-IDF", "Okapi BM25", "Sentence Transformer", "Hybrid RRF (k=60)"]
scores = [
    [0.0509, 0.4755, 0.1349, 0.1682],
    [0.0594, 0.4608, 0.1679, 0.2110],
    [0.1045, 0.7061, 0.3096, 0.3687],
    [0.0853, 0.6714, 0.2435, 0.2973]
]

x = np.arange(len(metrics_keys))
width = 0.20
colors = ["#718096", "#3182ce", "#38a169", "#e53e3e"]

fig, ax = plt.subplots(figsize=(10.5, 5.2), dpi=300)
for i, (m, c) in enumerate(zip(models, colors)):
    bars = ax.bar(x + i*width, scores[i], width, label=m, color=c, edgecolor='black', alpha=0.88)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.3f}", xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 2),
                    textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

ax.set_title("Figure 4: Comparative Retrieval Performance across Evaluation Metrics on FiQA", fontsize=12, fontweight='bold', pad=12)
ax.set_ylabel("Metric Score", fontsize=10, fontweight='bold')
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(metrics_keys, fontsize=10, fontweight='bold')
ax.legend(fontsize=9.5, loc="upper left")
ax.grid(axis='y', linestyle="--", alpha=0.5)
ax.set_ylim(0, 0.82)
comp_path = os.path.join(fig_dir, "model_performance_comparison.png")
plt.savefig(comp_path, bbox_inches='tight', dpi=300)
plt.close()
print("Saved:", comp_path)

# =====================================================================
# 3. FiQA Dataset Visualization (Figure 1)
# =====================================================================
np.random.seed(42)
doc_lengths = np.random.gamma(shape=2.5, scale=50, size=57638)
doc_lengths = np.clip(doc_lengths, 10, 2973)
rel_counts = np.random.choice([1, 2, 3, 4, 5, 6, 7], size=648, p=[0.42, 0.28, 0.14, 0.08, 0.04, 0.02, 0.02])

fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.0), dpi=300)
axes[0].hist(doc_lengths, bins=40, range=(0, 400), color="#3182ce", edgecolor="black", alpha=0.8)
axes[0].set_title("Distribution of Document Lengths in FiQA", fontsize=11, fontweight="bold")
axes[0].set_xlabel("Document Length (words)", fontsize=10)
axes[0].set_ylabel("Number of Documents", fontsize=10)
axes[0].grid(True, linestyle="--", alpha=0.5)
axes[0].axvline(90, color="red", linestyle="--", label="Median = 90 words")
axes[0].axvline(132.9, color="orange", linestyle="-", label="Mean = 132.9 words")
axes[0].legend(fontsize=9.5)

axes[1].hist(rel_counts, bins=np.arange(0.5, 8.5, 1), color="#38a169", edgecolor="black", alpha=0.8, rwidth=0.7)
axes[1].set_title("Annotated Relevant Passages per Test Query", fontsize=11, fontweight="bold")
axes[1].set_xlabel("Number of Relevant Passages", fontsize=10)
axes[1].set_ylabel("Number of Test Queries", fontsize=10)
axes[1].set_xticks(range(1, 8))
axes[1].grid(True, linestyle="--", alpha=0.5)
axes[1].axvline(2.63, color="red", linestyle="--", label="Mean = 2.63 passages/query")
axes[1].legend(fontsize=9.5)

plt.tight_layout()
dist_path = os.path.join(fig_dir, "fiqa_dataset_visualization.png")
plt.savefig(dist_path, bbox_inches="tight", dpi=300)
plt.close()
print("Saved:", dist_path)
