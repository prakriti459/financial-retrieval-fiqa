import os
import sys
import time
import pandas as pd

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from data_loader import load_fiqa, generate_dataset_visualizations
from models import TFIDFRetriever, BM25Retriever, DenseRetriever, reciprocal_rank_fusion
from evaluate import evaluate_retrieval_run, plot_precision_recall_curves, plot_model_comparison_barchart

def main():
    print("="*75)
    print("🚀 FINANCIAL RETRIEVAL USING FIQA: STANDARDIZED BENCHMARK PIPELINE")
    print("="*75)

    # 1. Load FiQA Dataset
    corpus, queries, qrels = load_fiqa(data_dir="data", split="test")

    # 2. Generate Section 2.1 Visualizations
    print("\n📊 Generating Section 2 Dataset Visualizations...")
    generate_dataset_visualizations(corpus, queries, qrels, save_dir="figures")

    # 3. Model 1: TF-IDF Vector Space Model
    print("\n--- [1/4] Running Model 1: TF-IDF ---")
    tfidf = TFIDFRetriever(corpus)
    tfidf_results = tfidf.batch_retrieve(queries, top_k=100)
    tfidf_metrics = evaluate_retrieval_run(tfidf_results, qrels)

    # 4. Model 2: Okapi BM25 Probabilistic Model
    print("\n--- [2/4] Running Model 2: Okapi BM25 ---")
    bm25 = BM25Retriever(corpus)
    bm25_results = bm25.batch_retrieve(queries, top_k=100)
    bm25_metrics = evaluate_retrieval_run(bm25_results, qrels)

    # 5. Model 3: Sentence Transformer (Dense Semantic)
    print("\n--- [3/4] Running Model 3: Sentence Transformer (all-MiniLM-L6-v2) ---")
    dense = DenseRetriever(corpus)
    dense_results = dense.batch_retrieve(queries, top_k=100)
    dense_metrics = evaluate_retrieval_run(dense_results, qrels)

    # 6. Model 4: Hybrid Reciprocal Rank Fusion (RRF)
    print("\n--- [4/4] Running Model 4: Hybrid RRF (BM25 + TF-IDF + Dense) ---")
    hybrid_results = {}
    for qid in queries:
        hybrid_results[qid] = reciprocal_rank_fusion(
            [tfidf_results[qid], bm25_results[qid], dense_results[qid]], 
            k_rrf=60, 
            top_k=100
        )
    hybrid_metrics = evaluate_retrieval_run(hybrid_results, qrels)

    # 7. Print Master Table 1 (Matching Sir's Report Format Exactly!)
    all_metrics = {
        "TF-IDF": tfidf_metrics,
        "BM25": bm25_metrics,
        "Sentence Transformer": dense_metrics,
        "Hybrid RRF (BM25 + TF-IDF + Dense)": hybrid_metrics
    }

    table_1_df = pd.DataFrame([
        {"Ranking Model": "TF-IDF", **tfidf_metrics},
        {"Ranking Model": "BM25", **bm25_metrics},
        {"Ranking Model": "Sentence Transformer", **dense_metrics},
        {"Ranking Model": "Hybrid RRF (BM25 + TF-IDF + Dense)", **hybrid_metrics}
    ])

    print("\n" + "="*75)
    print("🏆 TABLE 1: PERFORMANCE COMPARISON OF SEARCH MODELS ON FIQA BENCHMARK")
    print("="*75)
    print(table_1_df.to_string(index=False))
    print("="*75)

    # 8. Plot Precision-Recall Graph & Bar Chart
    print("\n📈 Plotting Deliverables for Report...")
    models_results = {
        "TF-IDF": tfidf_results,
        "BM25": bm25_results,
        "Sentence Transformer": dense_results,
        "Hybrid RRF": hybrid_results
    }
    plot_precision_recall_curves(models_results, qrels, save_dir="figures")
    plot_model_comparison_barchart(all_metrics, save_dir="figures")

    print("\n All experiments complete! Figures saved in 'figures/' directory.")
    print(" To launch the interactive search UI for your demonstration, run:")
    print("    streamlit run app.py")

if __name__ == "__main__":
    main()
