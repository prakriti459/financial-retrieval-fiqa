import os
import sys
import time
import numpy as np
import streamlit as st

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from data_loader import load_fiqa
from models import TFIDFRetriever, BM25Retriever, DenseRetriever, reciprocal_rank_fusion

# Page Configuration
st.set_page_config(
    page_title="FinSearch: Financial Information Retrieval System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Light Fintech CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    .hero-banner {
        background: linear-gradient(135deg, #1B365D 0%, #0F5C6E 100%);
        padding: 24px 28px;
        border-radius: 10px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(27, 54, 93, 0.12);
    }
    .hero-banner h1 {
        color: #FFFFFF !important;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
    }
    .hero-banner p {
        color: #E2E8F0;
        font-size: 13.5px;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    .result-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .badge-rank {
        background-color: #1B365D;
        color: #FFFFFF;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        letter-spacing: 0.04em;
    }
    .badge-meta {
        font-family: 'JetBrains Mono', monospace;
        color: #475569;
        font-size: 12px;
        float: right;
    }
    .passage-title {
        font-size: 15px;
        font-weight: 600;
        color: #0F172A;
        margin: 10px 0 6px 0;
    }
    .passage-snippet {
        font-size: 13px;
        color: #334155;
        line-height: 1.6;
        background-color: #F8FAFC;
        padding: 12px 14px;
        border-radius: 0 6px 6px 0;
        border-left: 3px solid #008080;
    }
    .success-banner {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #065F46;
        padding: 10px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        font-size: 13px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Cache Models & Corpus in Memory for High-Speed Demonstration
@st.cache_resource(show_spinner="⚡ Initializing FiQA dataset & indexing models...")
def load_all_components():
    corpus, queries, qrels = load_fiqa(data_dir="data", split="test")
    tfidf = TFIDFRetriever(corpus)
    bm25 = BM25Retriever(corpus)
    dense = DenseRetriever(corpus)
    return corpus, queries, qrels, tfidf, bm25, dense

corpus, queries, qrels, tfidf, bm25, dense = load_all_components()

# Hero Header
st.markdown("""
<div class="hero-banner">
    <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; opacity: 0.85; margin-bottom: 4px;">Information Retrieval System · Project 9</div>
    <h1>📈 FinSearch: Financial Information Retrieval System</h1>
    <p>Comparative Evaluation of <b>TF-IDF</b>, <b>Okapi BM25</b>, <b>Sentence Transformers</b>, and <b>Hybrid RRF</b> on the FiQA Benchmark (57,638 Documents).</p>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab_search, tab_benchmark, tab_dataset = st.tabs(["🔍 Interactive Search Engine", "📊 Benchmark Performance (Table 1)", "📖 About FiQA Dataset"])

SAMPLE_QUERIES = [
    "Select a preset query or type your own below...",
    "What is the difference between an ETF and a mutual fund?",
    "How to deposit a cheque issued to an associate in my business into my business account?",
    "What are the tax implications and penalties for a 401(k) early withdrawal?",
    "How to hedge an equity portfolio against sudden market crash and inflation risk?",
    "What does short selling a stock mean and what are the primary risks involved?",
    "How do index fund expense ratios impact long-term compounding returns?",
    "Can capital losses be carried forward to offset future capital gains?"
]

# --- TAB 1: INTERACTIVE SEARCH INTERFACE ---
with tab_search:
    col_left, col_right = st.columns([1, 1.4], gap="large")
    
    with col_left:
        st.subheader("⚙️ Search Controls")
        
        sample_pick = st.selectbox("💡 Choose a Preset Financial Query:", SAMPLE_QUERIES)
        default_val = "" if sample_pick == SAMPLE_QUERIES[0] else sample_pick
        
        user_query = st.text_area("Search Query:", value=default_val if default_val else "What is the difference between an ETF and a mutual fund?", height=85)
        
        model_choice = st.radio(
            "Ranking Architecture:",
            [
                "Hybrid RRF (Sparse + Dense)", 
                "Sentence Transformer (Dense Semantic)", 
                "Okapi BM25 (Lexical)", 
                "TF-IDF (Vector Space)"
            ],
            index=0
        )
        
        top_k = st.slider("Top-K Passages:", min_value=1, max_value=10, value=3)
        run_btn = st.button("🔍 Run Search", type="primary", use_container_width=True)

    with col_right:
        st.subheader("📋 Ranked Retrieval Results")
        
        if run_btn:
            if not user_query.strip():
                st.warning("Please enter a financial question.")
            else:
                t0 = time.time()
                
                if model_choice == "TF-IDF (Vector Space)":
                    results = tfidf.retrieve(user_query, top_k=top_k)
                elif model_choice == "Okapi BM25 (Lexical)":
                    results = bm25.retrieve(user_query, top_k=top_k)
                elif model_choice == "Sentence Transformer (Dense Semantic)":
                    results = dense.retrieve(user_query, top_k=top_k)
                else:  # Hybrid RRF
                    bm25_res = bm25.retrieve(user_query, top_k=40)
                    dense_res = dense.retrieve(user_query, top_k=40)
                    bm25_ids = [d for d, _ in bm25_res]
                    dense_ids = [d for d, _ in dense_res]
                    fused = reciprocal_rank_fusion([bm25_ids, dense_ids], k_rrf=60, top_k=top_k)
                    results = [(did, 1.0 / (60 + rank)) for rank, did in enumerate(fused, start=1)]
                    
                latency_ms = (time.time() - t0) * 1000
                
                st.markdown(f"""
                <div class="success-banner">
                    ✓ Found <b>{len(results)}</b> passages in <b>{latency_ms:.1f} ms</b> using <u>{model_choice}</u>
                </div>
                """, unsafe_allow_html=True)
                
                for rank, (doc_id, score) in enumerate(results, start=1):
                    doc = corpus[doc_id]
                    title = doc['title'].strip() if doc['title'] else "Financial Discussion Passage"
                    text = doc['text'].replace('\n', ' ').strip()
                    
                    st.markdown(f"""
                    <div class="result-card">
                        <div>
                            <span class="badge-rank">RANK #{rank}</span>
                            <span class="badge-meta">Doc ID: <b>{doc_id}</b> &nbsp;|&nbsp; Score: <b>{score:.4f}</b></span>
                        </div>
                        <div class="passage-title">{title}</div>
                        <div class="passage-snippet">"{text[:340]}..."</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Select a query on the left and click **Run Search** to inspect retrieved passages.")

# --- TAB 2: BENCHMARK TABLE & EVALUATION ---
with tab_benchmark:
    st.subheader("📊 Official Benchmark Evaluation on FiQA Test Set")
    st.markdown("Evaluated across all **648 annotated queries** against **57,638 documents** (1,706 ground-truth judgments):")
    
    benchmark_df = {
        "Ranking Model": [
            "TF-IDF (Vector Space)",
            "Okapi BM25",
            "Sentence Transformer (all-MiniLM-L6-v2)",
            "Hybrid RRF (BM25 + TF-IDF + Dense)"
        ],
        "Precision@10": [0.0509, 0.0594, 0.1045, 0.0853],
        "Recall@100": [0.4755, 0.4608, 0.7061, 0.6714],
        "MAP": [0.1349, 0.1679, 0.3096, 0.2435],
        "nDCG@10": [0.1682, 0.2110, 0.3687, 0.2973]
    }
    st.table(benchmark_df)
    
    st.markdown("""
    ### 📌 Key Analytical Findings for Project Viva:
    1. **BM25 vs. TF-IDF:** BM25 improves nDCG@10 by **+25.4%** due to non-linear term saturation ($k_1=1.5$) and document length normalization ($b=0.75$).
    2. **Dense Semantic Superiority:** Sentence Transformer increases **MAP by +84.4%** and **nDCG@10 by +74.7%** over BM25, proving that financial search requires conceptual understanding rather than exact token repetition.
    3. **Lexical Redundancy in 3-Way RRF:** Combining multiple sparse models (TF-IDF + BM25) can dilute dense candidates in equal-voting fusion, highlighting the importance of asymmetric weighting.
    """)

# --- TAB 3: ABOUT DATASET ---
with tab_dataset:
    st.subheader("📖 FiQA Benchmark Dataset Overview")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("""
        * **Domain:** Unstructured financial forum discussions, personal investment questions, and news commentary.
        * **Total Documents:** 57,638 passages.
        * **Evaluation Test Queries:** 648 queries.
        * **Total Ground-Truth Judgments (Qrels):** 1,706 pairs.
        * **Mean Document Length:** 132.9 words (Median: 90 words).
        """)
    with col_d2:
        st.markdown("""
        * **Core Challenge:** **Vocabulary Mismatch Problem**.
        * **Example:** A user asking *"how to deposit a cheque issued to an associate into business account"* requires legal banking advice about *"third-party check endorsement"*. 
        * Dense retrieval maps both concepts into adjacent vector spaces.
        """)
