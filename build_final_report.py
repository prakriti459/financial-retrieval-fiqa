import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

FIG_DIR = r"C:\Users\PRAKRITI\Desktop\financial-retrieval-fiqa\figures"
OUTPUT_DOCX = r"C:\Users\PRAKRITI\Desktop\Financial_IR_Project_Report.docx"

doc = docx.Document()

# Set standard 1-inch margins
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Configure default style
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
font.color.rgb = RGBColor(0x22, 0x22, 0x22)
style.paragraph_format.line_spacing = 1.15
style.paragraph_format.space_after = Pt(6)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

def add_heading1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

def add_heading2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

def add_caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(9.5)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

def add_image_centered(img_path, width_inches=6.0):
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.add_run().add_picture(img_path, width=Inches(width_inches))

# =====================================================================
# DOCUMENT GENERATION
# =====================================================================

# Title
add_title("Comparative Performance Evaluation of Sparse, Dense, and Hybrid Retrieval Models on the FiQA Financial Benchmark")

# Student Details Table (Exact match to course template)
table = doc.add_table(rows=4, cols=3)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Students Name", "Registration No.", "Email-id"]
hdr_cells = table.rows[0].cells
for i, h in enumerate(headers):
    hdr_cells[i].text = h
    set_cell_background(hdr_cells[i], "2B6CB0")
    set_cell_margins(hdr_cells[i], top=120, bottom=120, left=150, right=150)
    for p in hdr_cells[i].paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

students_data = [
    ("Prakriti", "23FE10CSE00459", "PRAKRITI.23FE10CSE00459@muj.manipal.edu"),
    ("Nishtha", "[Registration No.]", "[email@muj.manipal.edu]"),
    ("[Student 3 Name]", "[Registration No.]", "[email@muj.manipal.edu]")
]

for row_idx, data in enumerate(students_data, start=1):
    row_cells = table.rows[row_idx].cells
    bg = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(data):
        row_cells[col_idx].text = text
        set_cell_background(row_cells[col_idx], bg)
        set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=150, right=150)
        for p in row_cells[col_idx].paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Abstract
p_abs = doc.add_paragraph()
p_abs.paragraph_format.space_before = Pt(4)
p_abs.paragraph_format.space_after = Pt(6)
r_abs_bold = p_abs.add_run("Abstract — ")
r_abs_bold.font.bold = True
p_abs.add_run(
    "Modern Information Retrieval (IR) systems rely on a spectrum of search architectures ranging from classical "
    "sparse lexical algorithms to high-dimensional dense neural embeddings. While sparse models like TF-IDF and BM25 "
    "excel at exact keyword matching, specialized ticker identification, and computational throughput, dense bi-encoders "
    "effectively resolve vocabulary mismatch through semantic understanding. To explore the complementary strengths "
    "of both paradigms, this study conducts an empirical investigation into a Hybrid Retrieval pipeline utilizing "
    "Reciprocal Rank Fusion (RRF). We evaluate four core retrieval strategies—TF-IDF, Okapi BM25, Sentence Transformers "
    "(all-MiniLM-L6-v2), and Hybrid RRF—on the FiQA-2018 financial information retrieval benchmark comprising 57,638 "
    "documents and 648 annotated queries. Our findings establish that dense semantic encoding delivers substantial gains "
    "over lexical baselines (improving nDCG@10 from 0.2110 to 0.3687 and MAP from 0.1679 to 0.3096). Furthermore, while "
    "hybrid rank aggregation outperforms both classical sparse baselines, it encounters the Lexical Redundancy Problem "
    "when combining multiple sparse models with a single dense ranker. We provide an end-to-end evaluation with 11-point "
    "interpolated precision-recall curves and a lightweight interactive search interface for system demonstration."
)

# Keywords
p_kw = doc.add_paragraph()
p_kw.paragraph_format.space_before = Pt(2)
p_kw.paragraph_format.space_after = Pt(12)
r_kw_bold = p_kw.add_run("Keywords: ")
r_kw_bold.font.bold = True
p_kw.add_run("Information Retrieval • Okapi BM25 • Sentence Transformers • Reciprocal Rank Fusion • FiQA Benchmark • Dense Semantic Search • Financial Domain IR")

# ---------------------------------------------------------------------
# 1. Introduction (1 page)
# ---------------------------------------------------------------------
add_heading1("1. Introduction")

doc.add_paragraph(
    "Information Retrieval (IR) serves as the indispensable computational backbone for modern search engines, enterprise "
    "knowledge bases, and Retrieval-Augmented Generation (RAG) architectures. In highly specialized verticals such as finance, "
    "retrieval systems are tasked with delivering authoritative, context-specific information—ranging from complex taxation "
    "statutes, SEC filings, and portfolio hedging strategies to personal financial advice—in response to queries that are often "
    "brief, syntactically ambiguous, and phrased by non-specialists."
)

doc.add_paragraph(
    "Historically, information retrieval has been anchored in sparse lexical scoring. Foundational vector space formulations "
    "such as Term Frequency-Inverse Document Frequency (TF-IDF) and probabilistic scoring functions like Okapi BM25 evaluate "
    "relevance through inverted indices and exact token overlap. These algorithms are computationally efficient, scale "
    "gracefully to millions of documents, and remain highly effective for queries featuring rare financial identifiers, "
    "stock tickers, and exact numerical quantities. However, sparse retrieval inherently suffers from the vocabulary mismatch "
    "problem: when a query and an authoritative document express the same conceptual reality using disparate vocabularies, "
    "lexical matching fails to retrieve the relevant record."
)

doc.add_paragraph(
    "The emergence of transformer architectures and dense bi-encoders (e.g., Sentence Transformers) has addressed this "
    "deficiency. Dense encoders project both queries and documents into a shared continuous latent embedding space, enabling "
    "similarity computation via dot product or cosine distance. This captures latent semantic intent, synonyms, and paraphrastic "
    "variations. Nevertheless, dense models can falter when queries hinge upon exact alphanumeric symbols, ticker symbols (e.g., "
    "AAPL, SPY), or precise monetary figures ($10,000 vs. $100,000), where exact lexical presence is critical."
)

doc.add_paragraph(
    "To achieve a robust balance between semantic intent and lexical precision, hybrid search architectures fuse rank lists "
    "generated by complementary retrieval paradigms. Reciprocal Rank Fusion (RRF) provides an unsupervised, parameter-free "
    "mechanism to merge ranked lists from diverse scorers without demanding score calibration or scale normalization. In "
    "this report, we evaluate the comparative performance of TF-IDF, Okapi BM25, Sentence Transformers, and Hybrid RRF on the "
    "FiQA benchmark dataset across standard academic metrics: Precision@10, Recall@100, Mean Average Precision (MAP), and "
    "Normalized Discounted Cumulative Gain (nDCG@10)."
)

# ---------------------------------------------------------------------
# 2. About Dataset (1 page)
# ---------------------------------------------------------------------
add_heading1("2. About Dataset")

doc.add_paragraph(
    "The empirical benchmarks conducted in this investigation utilize the FiQA-2018 (Financial Opinion Mining and Question "
    "Answering) dataset, hosted within the internationally acknowledged BEIR (Benchmarking Information Retrieval) benchmark suite. "
    "Originally introduced at The Web Conference (WWW 2018), FiQA was curated to simulate real-world financial inquiry and "
    "opinion discovery over authentic web communications, StackExchange forums, microblogs, and financial news reports."
)

doc.add_paragraph(
    "Unlike synthetic academic corpora, FiQA embodies the linguistic messiness of open-web financial discourse: informal "
    "slang, specialized tax terminology, stock abbreviations, numerical figures, and wide variations in document length. Table 1 "
    "summarizes the statistical parameters of the benchmark corpus."
)

# Table 1: Dataset Stats
p_tbl1_cap = doc.add_paragraph()
p_tbl1_cap.paragraph_format.space_before = Pt(6)
p_tbl1_cap.paragraph_format.space_after = Pt(3)
r_t1 = p_tbl1_cap.add_run("Table 1. Statistical Summary of the FiQA-2018 Information Retrieval Benchmark.")
r_t1.font.bold = True
r_t1.font.size = Pt(10)

t1 = doc.add_table(rows=7, cols=2)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
t1_headers = ["Characteristic", "Empirical Value / Description"]
for j, h in enumerate(t1_headers):
    t1.rows[0].cells[j].text = h
    set_cell_background(t1.rows[0].cells[j], "2B6CB0")
    set_cell_margins(t1.rows[0].cells[j], top=100, bottom=100, left=150, right=150)
    for p in t1.rows[0].cells[j].paragraphs:
        for r in p.runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

t1_rows = [
    ("Corpus Domain", "Financial Discussions, StackExchange, Microblogs, News Commentary"),
    ("Total Passages / Documents", "57,638 passages"),
    ("Annotated Evaluation Queries", "648 test queries"),
    ("Ground-Truth Relevance Pairs (Qrels)", "1,706 annotated relevance judgments"),
    ("Mean Document Length", "132.90 words (Median: 90 words)"),
    ("Document Length Range (Min / Max)", "0 words to 2,973 words")
]

for idx, (k, v) in enumerate(t1_rows, start=1):
    bg = "F7FAFC" if idx % 2 == 1 else "FFFFFF"
    t1.rows[idx].cells[0].text = k
    t1.rows[idx].cells[1].text = v
    set_cell_background(t1.rows[idx].cells[0], bg)
    set_cell_background(t1.rows[idx].cells[1], bg)
    set_cell_margins(t1.rows[idx].cells[0], top=70, bottom=70, left=150, right=150)
    set_cell_margins(t1.rows[idx].cells[1], top=70, bottom=70, left=150, right=150)
    t1.rows[idx].cells[0].paragraphs[0].runs[0].font.bold = True

add_heading2("2.1 Visualization of Dataset in Form of Graphs and Conceptual Example")

doc.add_paragraph(
    "To better understand the underlying distribution of the corpus, Figure 1 illustrates the statistical distribution of "
    "passage lengths (left) and the distribution of annotated relevant documents per query (right)."
)

add_image_centered(os.path.join(FIG_DIR, "fiqa_dataset_visualization.png"), width_inches=6.2)
add_caption("Figure 1: Statistical distribution of passage length in words (left) and ground-truth relevant passages per query (right) across FiQA.")

doc.add_paragraph(
    "As demonstrated in Figure 1 (left), passage lengths exhibit a pronounced right-skewed log-normal distribution. While "
    "the median passage is concise at 90 words, comprehensive legal explanations and corporate financial analyses extend "
    "up to 2,973 words. This pronounced length variance poses a severe challenge for unnormalized vector space models (such "
    "as standard TF-IDF), which tend to favor longer documents simply because term occurrences accumulate. In contrast, "
    "BM25's length normalization coefficient b actively penalizes overly verbose texts."
)

doc.add_paragraph(
    "Furthermore, Figure 1 (right) illustrates that each query possesses an average of only 2.63 relevant passages, with "
    "over 42% of queries having only a single annotated answer. This sparse relevance profile necessitates models with "
    "exceptional Precision@10, as missing the few ground-truth passages at early rank positions results in severe evaluation penalties."
)

# Concrete Query Example
doc.add_paragraph(
    "Concrete Vocabulary Mismatch Example: Consider Test Query ID 8: \"How to deposit a cheque issued to an associate in "
    "my business into my business account?\". The ground-truth passage (Document ID 65404) provides the authoritative legal "
    "guidance: \"...sign the back... third party cheque... endorsement...\". Notice that the relevant document contains "
    "neither the phrase \"deposit into business account\" nor \"associate\". Classical lexical search models (TF-IDF and BM25) "
    "fail to place this document within the top 50 ranks. Conversely, the dense Sentence Transformer model maps the semantic "
    "concept of third-party cheque endorsement directly to the user's intent, ranking it at Position 1."
)

# ---------------------------------------------------------------------
# 3. Methodology (2 pages)
# ---------------------------------------------------------------------
add_heading1("3. Methodology")

doc.add_paragraph(
    "Our end-to-end evaluation pipeline comprises four unified modular stages: domain-specific text preprocessing, dual-path "
    "sparse and dense candidate retrieval, rank fusion, and standard academic evaluation. The architectural flowchart "
    "depicting this complete retrieval pipeline is illustrated in Figure 2."
)

add_image_centered(os.path.join(FIG_DIR, "architecture_diagram.png"), width_inches=5.8)
add_caption("Figure 2: Architectural Flowchart of the Dual-Path Hybrid Financial Information Retrieval Pipeline.")

add_heading2("3.1 Preprocessing and Indexing")

doc.add_paragraph(
    "Financial texts present unique tokenization challenges. Standard NLP tokenizers often strip punctuation, inadvertently "
    "corrupting critical financial semantics such as monetary amounts ($500 -> 500), percentages (12.5% -> 12 5), and stock ticker "
    "identifiers. Our preprocessing pipeline applies the following disciplined transformations:"
)

p_p1 = doc.add_paragraph()
p_p1.paragraph_format.left_indent = Inches(0.25)
p_p1.add_run("1. Cleaning and Normalization: ").bold = True
p_p1.add_run("Text is stripped of HTML tags, control codes, and non-printable characters. Text is converted to lowercase while preserving domain symbols.")

p_p2 = doc.add_paragraph()
p_p2.paragraph_format.left_indent = Inches(0.25)
p_p2.add_run("2. Financial Entity & Term Preservation: ").bold = True
p_p2.add_run("A specialized regular expression pattern [\\$€£]?\\d+(?:\\.\\d+)?%? preserves currency values ($50B), decimal figures (3.75), and percentages (8.4%). Common ticker symbols and capitalized financial tokens are isolated.")

p_p3 = doc.add_paragraph()
p_p3.paragraph_format.left_indent = Inches(0.25)
p_p3.add_run("3. Stop-Word Removal: ").bold = True
p_p3.add_run("High-frequency function words from the standard English stop-word lexicon (e.g., 'the', 'is', 'at') are filtered out to prevent inverted index bloat.")

p_p4 = doc.add_paragraph()
p_p4.paragraph_format.left_indent = Inches(0.25)
p_p4.add_run("4. Porter Stemming: ").bold = True
p_p4.add_run("Morphological variants are reduced to their root linguistic forms (e.g., 'investing', 'investments', 'investor' -> 'invest') using the NLTK Porter Stemmer for sparse index matching.")

add_heading2("3.2 Candidate Ranking Models")

doc.add_paragraph(
    "We implement and evaluate four distinct retrieval algorithms representing both classical and modern information retrieval paradigms:"
)

doc.add_paragraph(
    "1. TF-IDF Vector Space Model: Represents passages and queries as sparse weighted vectors where weights are computed as "
    "the product of local term frequency (TF) and logarithmic inverse document frequency (IDF). Passage relevance is measured "
    "via cosine similarity between query and passage vectors in high-dimensional term space."
)

doc.add_paragraph(
    "2. Okapi BM25: A probabilistic retrieval function derived from the BM25 framework. BM25 enhances TF-IDF by incorporating "
    "two critical parameters: k1 (term frequency saturation, set to 1.5) and b (document length normalization, set to 0.75). "
    "The BM25 score for document d given query q is formulated as:"
)

p_bm = doc.add_paragraph()
p_bm.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_bm.paragraph_format.space_before = Pt(4)
p_bm.paragraph_format.space_after = Pt(4)
r_bm = p_bm.add_run("Score_BM25(d, q) = Σ [ IDF(t) · (f(t, d) · (k1 + 1)) / (f(t, d) + k1 · (1 - b + b · (|d| / avgdl))) ]")
r_bm.font.bold = True
r_bm.font.size = Pt(10)

doc.add_paragraph(
    "3. Sentence Transformer (Dense Semantic Search): Employs a pre-trained Siamese transformer bi-encoder (specifically "
    "sentence-transformers/all-MiniLM-L6-v2, mapping text into 384-dimensional dense vectors). Passages are encoded offline and "
    "stored in a dense vector index. At query time, the incoming question is embedded into the same 384-dimensional space, and "
    "candidate ranking is executed via cosine similarity against all passage embeddings."
)

doc.add_paragraph(
    "4. Hybrid Reciprocal Rank Fusion (RRF): Merges candidate rank lists from the sparse and dense retrieval paths. Because "
    "lexical BM25 scores (unbounded probabilistic logs) and dense cosine similarities (bounded between -1.0 and 1.0) occupy "
    "incompatible mathematical ranges, raw score interpolation is problematic. RRF circumvents this by operating strictly on "
    "ordinal rank positions."
)

add_heading2("3.3 Reciprocal Rank Fusion Formulation")

doc.add_paragraph(
    "Introduced by Cormack et al. (SIGIR 2009), Reciprocal Rank Fusion aggregates the reciprocal position of a document across "
    "multiple individual rankings. Given a set of rankers M and a smoothing hyperparameter constant k (conventionally set to 60), "
    "the RRF score for document d is formulated as:"
)

p_rrf = doc.add_paragraph()
p_rrf.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_rrf.paragraph_format.space_before = Pt(4)
p_rrf.paragraph_format.space_after = Pt(4)
r_rrf = p_rrf.add_run("RRF_Score(d ∈ D) = Σ_{m ∈ M} [ 1 / (k + r_m(d)) ]")
r_rrf.font.bold = True
r_rrf.font.size = Pt(10.5)

doc.add_paragraph(
    "where r_m(d) denotes the 1-based rank position of document d in the candidate list produced by model m. The smoothing "
    "constant k = 60 prevents top-ranked candidates from disproportionately dominating the fused score while maintaining high "
    "sensitivity to consensus across models."
)

# ---------------------------------------------------------------------
# 4. Experimental Setup and Performance Analysis (2 pages)
# ---------------------------------------------------------------------
add_heading1("4. Experimental Setup and Performance Analysis")

doc.add_paragraph(
    "The experimental evaluation is executed across all 648 annotated test queries of the FiQA benchmark against the complete "
    "57,638 passage corpus. In accordance with established TREC and BEIR evaluation protocols, we record four primary metrics:"
)

doc.add_paragraph(
    "• Precision@10: Proportion of relevant documents among the top 10 retrieved candidates.\n"
    "• Recall@100: Proportion of all known relevant documents retrieved within the top 100 ranks.\n"
    "• Mean Average Precision (MAP): Mean of average precision scores computed across all queries at every relevant document cutoff.\n"
    "• Normalized Discounted Cumulative Gain (nDCG@10): Evaluates graded relevance ranking quality with logarithmic rank discounting."
)

# Table 2: Benchmark Scores
p_tbl2_cap = doc.add_paragraph()
p_tbl2_cap.paragraph_format.space_before = Pt(8)
p_tbl2_cap.paragraph_format.space_after = Pt(3)
r_t2 = p_tbl2_cap.add_run("Table 2. Empirical Performance Comparison of Information Retrieval Models on the FiQA Benchmark.")
r_t2.font.bold = True
r_t2.font.size = Pt(10)

t2 = doc.add_table(rows=5, cols=5)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
t2_headers = ["Retrieval Model", "Precision@10", "Recall@100", "MAP", "nDCG@10"]
for j, h in enumerate(t2_headers):
    t2.rows[0].cells[j].text = h
    set_cell_background(t2.rows[0].cells[j], "2B6CB0")
    set_cell_margins(t2.rows[0].cells[j], top=100, bottom=100, left=120, right=120)
    for p in t2.rows[0].cells[j].paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

t2_rows = [
    ("TF-IDF Vector Space Model", "0.0509", "0.4755", "0.1349", "0.1682"),
    ("Okapi BM25", "0.0594", "0.4608", "0.1679", "0.2110"),
    ("Sentence Transformer (all-MiniLM-L6-v2)", "0.1045", "0.7061", "0.3096", "0.3687"),
    ("Hybrid RRF (BM25 + TF-IDF + Dense)", "0.0853", "0.6714", "0.2435", "0.2973")
]

for idx, row in enumerate(t2_rows, start=1):
    bg = "F7FAFC" if idx % 2 == 1 else "FFFFFF"
    for col_idx, val in enumerate(row):
        t2.rows[idx].cells[col_idx].text = val
        set_cell_background(t2.rows[idx].cells[col_idx], bg)
        set_cell_margins(t2.rows[idx].cells[col_idx], top=70, bottom=70, left=120, right=120)
        p = t2.rows[idx].cells[col_idx].paragraphs[0]
        if col_idx == 0:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.runs[0].font.bold = True
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

add_heading2("4.1 Precision-Recall Curves and Performance Visualizations")

doc.add_paragraph(
    "To evaluate model retrieval behavior across all recall thresholds, Figure 3 displays the official 11-point interpolated "
    "Precision-Recall graph. Furthermore, Figure 4 provides a grouped bar chart summarizing comparative metric values."
)

add_image_centered(os.path.join(FIG_DIR, "precision_recall_graph.png"), width_inches=5.8)
add_caption("Figure 3: 11-Point Interpolated Precision-Recall Graph across Retrieval Models on the FiQA Benchmark.")

add_image_centered(os.path.join(FIG_DIR, "model_performance_comparison.png"), width_inches=6.0)
add_caption("Figure 4: Comparative Retrieval Metric Summary across TF-IDF, Okapi BM25, Sentence Transformer, and Hybrid RRF.")

add_heading2("4.2 In-Depth Empirical Performance Analysis")

doc.add_paragraph(
    "1. Lexical Baseline Comparison (TF-IDF vs. Okapi BM25): As reported in Table 2, Okapi BM25 substantially outperforms "
    "the baseline TF-IDF Vector Space Model in ranking quality, achieving a +25.4% improvement in nDCG@10 (0.2110 vs. 0.1682) "
    "and a +24.5% improvement in MAP (0.1679 vs. 0.1349). This performance gap is directly attributable to BM25's sublinear term "
    "saturation (k1) and length normalization (b). In informal financial forums, repetitive keyword stuffing frequently inflates "
    "TF-IDF scores; BM25 caps the marginal impact of repeated terms, prioritizing compact, informative passages."
)

doc.add_paragraph(
    "2. The Decisive Advantage of Dense Semantic Search: The Sentence Transformer (all-MiniLM-L6-v2) establishes a dominant "
    "lead across every evaluation metric, dramatically surpassing all lexical baselines:\n"
    "• Precision@10 increases from 0.0594 (BM25) to 0.1045 (+75.9% relative gain).\n"
    "• Recall@100 surges from 0.4608 (BM25) to 0.7061 (+53.2% relative gain).\n"
    "• MAP increases from 0.1679 to 0.3096 (+84.4% relative gain).\n"
    "• nDCG@10 increases from 0.2110 to 0.3687 (+74.7% relative gain)."
)

doc.add_paragraph(
    "As visualized in the Precision-Recall curves of Figure 3, the Sentence Transformer curve (green) dominates the entire "
    "recall spectrum, initiating at an interpolated precision of ~0.46 at recall 0.0 and remaining significantly higher than "
    "lexical curves through recall 0.7. This confirms that financial question-answering relies fundamentally on semantic intent: "
    "users rarely know precise institutional jargon, making dense conceptual alignment indispensable."
)

doc.add_paragraph(
    "3. Analysis of Hybrid RRF and the Lexical Redundancy Problem: Hybrid Reciprocal Rank Fusion delivers an nDCG@10 of 0.2973 "
    "and MAP of 0.2435, reflecting a +40.9% improvement over BM25 and a +44.7% improvement over TF-IDF. However, unweighted "
    "3-way RRF achieves a lower overall score than the standalone dense encoder (0.2973 vs. 0.3687). This empirical outcome "
    "highlights the Lexical Redundancy Problem: because TF-IDF and BM25 are both sparse lexical matching algorithms, they share "
    "a high degree of candidate overlap. In an unweighted voting scheme (1/3 each), sparse candidates effectively receive two "
    "votes while semantic candidates receive only one, diluting the ranking position of high-quality semantic matches. This "
    "finding provides crucial architectural guidance: hybrid pipelines should either fuse a single sparse ranker with a dense "
    "model or employ weighted fusion coefficients (e.g., α · Dense + (1 - α) · BM25)."
)

# ---------------------------------------------------------------------
# 5. Conclusion (1 page)
# ---------------------------------------------------------------------
add_heading1("5. Conclusion")

doc.add_paragraph(
    "In this study, we conducted a rigorous comparative performance evaluation of classical lexical, dense neural, and hybrid "
    "information retrieval architectures on the FiQA-2018 financial benchmark. Our empirical findings substantiate the following "
    "three key conclusions:"
)

doc.add_paragraph(
    "1. Probabilistic BM25 provides a markedly superior sparse baseline compared to TF-IDF (+25.4% nDCG@10), proving that document "
    "length normalization is indispensable when searching unstructured, variable-length financial discussions."
)

doc.add_paragraph(
    "2. Dense Sentence Transformers (all-MiniLM-L6-v2) resolve the financial domain's severe vocabulary mismatch challenge, "
    "delivering a +74.7% boost in nDCG@10 and an +84.4% boost in MAP over lexical baselines by mapping conceptual intent."
)

doc.add_paragraph(
    "3. While Reciprocal Rank Fusion robustly combines disparate retrieval algorithms without requiring score calibration, "
    "unweighted multi-model fusion can suffer from lexical redundancy if multiple correlated sparse models are fused against "
    "a single dense model."
)

doc.add_paragraph(
    "Future Work: Future extensions of this research will investigate domain-adapted financial language models (such as FinBERT), "
    "dynamic parameterized alpha weighting between dense and sparse ranks, and two-stage cross-encoder re-ranking applied to the "
    "top-50 retrieved candidates."
)

# ---------------------------------------------------------------------
# References
# ---------------------------------------------------------------------
add_heading1("References")

refs = [
    "[1] Robertson, S., Zaragoza, H.: The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in Information Retrieval 3(4), 333–389 (2009)",
    "[2] Reimers, N., Gurevych, I.: Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In: Proceedings of EMNLP-IJCNLP, pp. 3982–3992 (2019)",
    "[3] Cormack, G.V., Clarke, C.R., Buettcher, S.: Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods. In: Proceedings of SIGIR, pp. 758–759 (2009)",
    "[4] Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., Gurevych, I.: BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models. In: Proceedings of NeurIPS Datasets and Benchmarks Track (2021)",
    "[5] Maia, M., Handschuh, S., Freitas, A., Davis, B., McDermott, R., Zarrouk, M., Balahur, A.: WWW'18 Open Challenge: Financial Opinion Mining and Question Answering. In: Companion Proceedings of The Web Conference, pp. 1941–1942 (2018)",
    "[6] Manning, C.D., Raghavan, P., Schütze, H.: Introduction to Information Retrieval. Cambridge University Press (2008)"
]

for ref in refs:
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.left_indent = Inches(0.25)
    p_ref.paragraph_format.space_after = Pt(4)
    run_ref = p_ref.add_run(ref)
    run_ref.font.size = Pt(9.5)
    run_ref.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

doc.save(OUTPUT_DOCX)
print(" Successfully created master report docx at:", OUTPUT_DOCX)
