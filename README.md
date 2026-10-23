# Financial Retrieval using FiQA (Project 9)
**Comparative Performance Evaluation of Sparse, Dense, and Hybrid Retrieval Models**

---

## 📌 Project Overview
Enterprise financial search engines face unique linguistic hurdles: domain-specific acronyms (`401(k)`, `P/E`, `ETF`), complex regulatory terminology, and non-expert conversational phrasing. 

This repository implements the standardized Information Retrieval (IR) pipeline for **Project 9: Financial Retrieval using FiQA**, evaluating four distinct ranking paradigms across **57,638 financial documents** and **648 annotated queries**:
1. **TF-IDF Vector Space Model** (Sublinear TF, $L_2$ Cosine Distance)
2. **Okapi BM25** (Probabilistic Term Saturation $k_1=1.5$, Length Normalization $b=0.75$)
3. **Sentence Transformer** (`sentence-transformers/all-MiniLM-L6-v2` 384-dim Dense Bi-Encoder)
4. **Hybrid Reciprocal Rank Fusion (RRF)** ($k=60$ Rank Aggregation)

---

## 🏆 Performance Comparison Table (Table 1)
Evaluated across all 648 annotated queries on the FiQA test split:

| Ranking Model | Precision@10 | Recall@100 | MAP | nDCG@10 |
| :--- | :---: | :---: | :---: | :---: |
| **TF-IDF (Baseline)** | 0.0509 | 0.4755 | 0.1349 | 0.1682 |
| **Okapi BM25** | 0.0594 | 0.4608 | 0.1679 | 0.2110 |
| **Sentence Transformer (Dense)** | **0.1045** | **0.7061** | **0.3096** | **0.3687** |
| **Hybrid RRF (BM25 + TF-IDF + Dense)** | 0.0853 | 0.6714 | 0.2435 | 0.2973 |

### Key Analytical Takeaways:
* **BM25 vs. TF-IDF:** BM25 improves nDCG@10 by **+25.4%** (`0.1682` → `0.2110`) due to non-linear saturation factors that prevent long forum threads from dominating scores.
* **Semantic Superiority:** Sentence Transformer boosts **MAP by +84.4%** (`0.1679` → `0.3096`) and **nDCG@10 by +74.7%** over BM25, demonstrating that financial question answering is heavily conceptual.
* **Lexical Redundancy:** 3-Way RRF reveals that fusing multiple sparse models (TF-IDF + BM25) can dilute dense candidates, underscoring the importance of model-capacity weighting.

---

## 🚀 Setup & Execution Guide (For Team & Evaluators)

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/<your-username>/financial-retrieval-fiqa.git
cd financial-retrieval-fiqa
pip install -r requirements.txt
```

### 2. Run All Experiments & Generate Figures
To run the automated benchmark across all 4 models, print Table 1, and save the official Precision-Recall and bar chart figures:
```bash
python run_experiments.py
```
*Outputs saved:*
* `figures/fiqa_dataset_visualization.png` (Section 2.1)
* `figures/architecture_diagram.png` (Section 3)
* `figures/precision_recall_graph.png` (Section 4)
* `figures/model_performance_comparison.png` (Section 4)



## 📁 Repository Structure
```
financial-retrieval-fiqa/
├── data/
│   └── fiqa/                  # Automated download of 57k docs, queries, qrels
├── figures/                   # Publication-ready figures for report
│   ├── fiqa_dataset_visualization.png
│   ├── precision_recall_graph.png
│   └── model_performance_comparison.png
├── src/
│   ├── preprocessing.py       # Cleaning, tokenization, stopwords, Porter stemming
│   ├── data_loader.py         # Ingestion, statistics & dataset visualizations
│   ├── models.py              # TF-IDF, BM25, Dense & RRF implementations
│   └── evaluate.py            # Precision@10, Recall@100, MAP, nDCG@10 & PR curves
├── app.py                     # Streamlit interactive web interface
├── run_experiments.py         # Main benchmark execution runner
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```
