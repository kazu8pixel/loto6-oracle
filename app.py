"""
ロト6 統計分析＆ハイブリッド番号生成ツール（モバイル・タブレット対応版）
"""

import random
import itertools
from collections import Counter

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# ページ設定
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LOTO6 ORACLE",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",   # モバイルでは最初から折りたたむ
)

# ─────────────────────────────────────────────
# レスポンシブ CSS
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* ══ ベース ══ */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; -webkit-text-size-adjust: 100%; }
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1526 40%, #0a1020 100%);
        color: #e2e8f0;
    }

    /* ══ メインコンテナ余白 ══ */
    .block-container {
        padding: 1rem 1rem 2rem 1rem !important;
        max-width: 1200px !important;
    }

    /* ══ ヒーロー ══ */
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: clamp(1.4rem, 5vw, 2.6rem);
        font-weight: 900;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #e879f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 0.08em;
        text-align: center;
        margin-bottom: 0;
        padding-top: 0.5rem;
        line-height: 1.2;
    }
    .hero-sub {
        text-align: center;
        font-size: clamp(0.6rem, 2.5vw, 0.85rem);
        color: #64748b;
        letter-spacing: 0.15em;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 0.2rem;
        margin-bottom: 1rem;
    }

    /* ══ サイドバーオープンヒント ══ */
    .sidebar-hint {
        text-align: center;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.78rem;
        color: #38bdf8;
        letter-spacing: 0.1em;
        margin-bottom: 0.8rem;
        padding: 0.4rem 0.8rem;
        background: rgba(56,189,248,0.06);
        border: 1px solid #38bdf822;
        border-radius: 8px;
    }

    /* ══ サイドバー ══ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #0d1526 100%);
        border-right: 1px solid #1e3a5f44;
        min-width: 280px !important;
    }
    [data-testid="stSidebar"] .block-container {
        padding: 1rem 0.8rem !important;
    }
    .sidebar-title {
        font-family: 'Orbitron', monospace;
        font-size: 0.9rem;
        font-weight: 700;
        color: #38bdf8;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #1e3a5f;
    }
    .sidebar-section {
        background: rgba(30, 58, 95, 0.2);
        border: 1px solid #1e3a5f55;
        border-radius: 10px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
    }

    /* ══ レスポンシブ カラム ══ */
    /* タブレット以下でカラムをスタック */
    @media (max-width: 768px) {
        [data-testid="column"] {
            width: 100% !important;
            flex: 0 0 100% !important;
            min-width: 100% !important;
        }
        /* KPIは2列を維持 */
        .kpi-row [data-testid="column"] {
            width: 50% !important;
            flex: 0 0 50% !important;
            min-width: 50% !important;
        }
        .block-container {
            padding: 0.5rem 0.5rem 2rem 0.5rem !important;
        }
    }
    @media (max-width: 480px) {
        /* スマホではKPIも1列 */
        [data-testid="column"] {
            width: 100% !important;
            flex: 0 0 100% !important;
            min-width: 100% !important;
        }
    }

    /* ══ KPI カード ══ */
    [data-testid="metric-container"] {
        background: rgba(15,23,42,0.7);
        border: 1px solid #1e3a5f55;
        border-radius: 10px;
        padding: 0.7rem 0.8rem;
        min-height: 80px;
    }
    [data-testid="metric-container"] label {
        color: #64748b !important;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'Orbitron', monospace;
        color: #38bdf8 !important;
        font-size: clamp(1.1rem, 4vw, 1.6rem) !important;
    }

    /* ══ セクションヘッダー ══ */
    .section-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(0.9rem, 3vw, 1.1rem);
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin: 1.2rem 0 0.7rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #1e3a5f55;
    }
    .section-header span { color: #38bdf8; }

    /* ══ stat-card ══ */
    .stat-card {
        background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(13,21,38,0.9) 100%);
        border: 1px solid #1e3a5f66;
        border-radius: 12px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(56,189,248,0.08);
    }
    .stat-card-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.65rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        margin-bottom: 0.2rem;
    }
    .stat-card-value {
        font-family: 'Orbitron', monospace;
        font-size: clamp(1.3rem, 5vw, 2rem);
        font-weight: 700;
        color: #38bdf8;
        line-height: 1.1;
    }
    .stat-card-unit {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-left: 0.2rem;
    }

    /* ══ 予想ボール ══ */
    .ball-row {
        display: flex;
        gap: clamp(6px, 2vw, 12px);
        align-items: center;
        flex-wrap: wrap;
        margin: 8px 0;
    }
    .ball {
        width: clamp(38px, 10vw, 50px);
        height: clamp(38px, 10vw, 50px);
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: clamp(0.7rem, 2.5vw, 1rem);
        box-shadow: 0 2px 12px rgba(0,0,0,0.5),
                    inset 0 -2px 4px rgba(0,0,0,0.3),
                    inset 0 2px 4px rgba(255,255,255,0.15);
        flex-shrink: 0;
        touch-action: manipulation;
    }
    .ball-blue {
        background: radial-gradient(circle at 35% 35%, #60a5fa, #1d4ed8);
        color: #fff; border: 1.5px solid #3b82f6aa;
    }
    .ball-red {
        background: radial-gradient(circle at 35% 35%, #f87171, #b91c1c);
        color: #fff; border: 1.5px solid #ef4444aa;
    }
    .ball-gold {
        background: radial-gradient(circle at 35% 35%, #fbbf24, #d97706);
        color: #1a1a1a; border: 1.5px solid #f59e0baa;
    }

    /* ══ 予想カード ══ */
    .pred-card {
        background: linear-gradient(135deg, rgba(15,23,42,0.95) 0%, rgba(10,18,38,0.95) 100%);
        border: 1px solid #1e3a5f88;
        border-radius: 14px;
        padding: 1rem 1rem 1rem 1.3rem;
        margin-bottom: 0.9rem;
        position: relative;
        overflow: hidden;
    }
    .pred-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 4px; height: 100%;
        background: linear-gradient(180deg, #38bdf8, #818cf8);
        border-radius: 4px 0 0 4px;
    }
    .pred-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 0.7rem;
    }
    .pred-card-num {
        font-family: 'Orbitron', monospace;
        font-size: 0.72rem;
        color: #38bdf8;
        letter-spacing: 0.1em;
        font-weight: 700;
    }
    .badge-row { display: flex; gap: 6px; flex-wrap: wrap; }
    .badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        letter-spacing: 0.04em;
        white-space: nowrap;
    }
    .badge-ok  { background: rgba(56,189,248,0.15); color: #38bdf8; border: 1px solid #38bdf840; }
    .badge-off { background: rgba(100,116,139,0.1);  color: #64748b; border: 1px solid #64748b40; }
    .pred-meta {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 0.7rem;
    }
    .pred-meta-item {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.8rem;
        color: #94a3b8;
        white-space: nowrap;
    }
    .pred-meta-item span { color: #e2e8f0; font-weight: 600; }

    /* ══ タブ ══ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 3px;
        background: rgba(15,23,42,0.6);
        border-radius: 10px;
        padding: 3px;
        border: 1px solid #1e3a5f44;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: clamp(0.85rem, 3vw, 1rem);
        color: #64748b;
        letter-spacing: 0.06em;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none !important;
        white-space: nowrap;
        min-height: 44px;  /* タッチターゲット */
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a5f, #0f2a4a) !important;
        color: #38bdf8 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    /* ══ ボタン ══ */
    .stButton > button {
        background: linear-gradient(135deg, #1e3a5f, #0f2a4a);
        color: #38bdf8;
        border: 1px solid #38bdf855;
        border-radius: 10px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: clamp(0.95rem, 3vw, 1.05rem);
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.7rem 1rem;
        width: 100%;
        min-height: 52px;     /* タッチしやすい高さ */
        transition: all 0.2s;
        -webkit-tap-highlight-color: transparent;
    }
    .stButton > button:hover, .stButton > button:active {
        background: linear-gradient(135deg, #2a4f7a, #1a3a6a);
        border-color: #38bdf8aa;
        box-shadow: 0 0 20px rgba(56,189,248,0.2);
        color: #7dd3fc;
    }

    /* ══ number_input タッチ対応 ══ */
    input[type="number"] {
        font-size: 1rem !important;
        min-height: 44px !important;
    }
    [data-testid="stNumberInput"] button {
        min-width: 40px !important;
        min-height: 40px !important;
    }

    /* ══ スライダー ══ */
    [data-testid="stSlider"] {
        padding: 0.2rem 0;
    }
    [data-testid="stSlider"] [role="slider"] {
        width: 22px !important;
        height: 22px !important;  /* タッチしやすい */
    }

    /* ══ ファイルアップロード ══ */
    [data-testid="stFileUploader"] {
        background: rgba(15,23,42,0.5);
        border: 1px dashed #1e3a5f;
        border-radius: 10px;
        padding: 0.4rem;
    }

    /* ══ チェックボックス ══ */
    [data-testid="stCheckbox"] label {
        font-size: 0.9rem;
        min-height: 44px;
        display: flex;
        align-items: center;
    }

    /* ══ テーブル（横スクロール） ══ */
    .stDataFrame {
        border: 1px solid #1e3a5f44;
        border-radius: 10px;
        overflow: hidden;
    }
    [data-testid="stDataFrameResizable"] {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch;
    }

    /* ══ plotly グラフ ══ */
    .js-plotly-plot .plotly { touch-action: pan-x pan-y; }

    /* ══ フッター ══ */
    .footer-bar {
        text-align: center;
        color: #334155;
        font-size: 0.72rem;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 0.08em;
        border-top: 1px solid #1e3a5f33;
        padding-top: 1rem;
        margin-top: 2rem;
        line-height: 1.6;
    }

    /* ══ スクロールバー ══ */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #0a0e1a; }
    ::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }

    /* ══ 分割線 ══ */
    hr { border-color: #1e3a5f44; }

    /* ══ 凡例バー ══ */
    .legend-bar {
        margin-top: 0.8rem;
        padding: 0.7rem 1rem;
        background: rgba(15,23,42,0.6);
        border: 1px solid #1e3a5f44;
        border-radius: 8px;
        font-size: 0.78rem;
        color: #64748b;
        font-family: 'Rajdhani', sans-serif;
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        align-items: center;
    }
    .legend-ball {
        display: inline-flex;
        width: 20px; height: 20px;
        border-radius: 50%;
        align-items: center;
        justify-content: center;
        font-size: 0;
        vertical-align: middle;
        margin-right: 4px;
        flex-shrink: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# ユーティリティ関数
# ─────────────────────────────────────────────
COLS_NUMBERS = ["第1数字", "第2数字", "第3数字", "第4数字", "第5数字", "第6数字"]
BONUS_COL = "ボーナス数字"
REQUIRED_COLS = ["開催回", "日付"] + COLS_NUMBERS + [BONUS_COL]


@st.cache_data(show_spinner=False)
def load_and_validate(file_bytes: bytes, filename: str) -> pd.DataFrame:
    # ── エンコーディング自動判定
    df = None
    for enc in ["utf-8-sig", "utf-8", "shift_jis", "cp932", "euc-jp"]:
        try:
            df = pd.read_csv(pd.io.common.BytesIO(file_bytes), encoding=enc)
            break
        except (UnicodeDecodeError, Exception):
            continue
    if df is None:
        raise ValueError("CSVのエンコーディングを判定できませんでした。UTF-8またはShift-JISで保存してください。")

    # ── 列名の正規化（前後空白・BONUS数字 → ボーナス数字）
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"BONUS数字": "ボーナス数字", "bonus数字": "ボーナス数字"})

    # ── 必須列チェック（ボーナス数字は任意扱いに緩和）
    must = ["開催回"] + COLS_NUMBERS
    missing = [c for c in must if c not in df.columns]
    if missing:
        raise ValueError(f"以下の列が見つかりません: {missing}")

    # ── ボーナス数字列がなければ 0 で補完
    if BONUS_COL not in df.columns:
        df[BONUS_COL] = 0

    for c in COLS_NUMBERS + [BONUS_COL]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=COLS_NUMBERS).copy()
    df[COLS_NUMBERS] = df[COLS_NUMBERS].astype(int)
    df = df.sort_values("開催回").reset_index(drop=True)
    return df


def get_all_drawn_numbers(df: pd.DataFrame) -> list:
    return df[COLS_NUMBERS].values.flatten().tolist()


def frequency_ranking(df: pd.DataFrame) -> pd.DataFrame:
    nums = get_all_drawn_numbers(df)
    counter = Counter(nums)
    rows = [{"数字": i, "出現回数": counter.get(i, 0)} for i in range(1, 44)]
    result = pd.DataFrame(rows).sort_values("出現回数", ascending=False).reset_index(drop=True)
    result.index += 1
    return result


def pair_affinity(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    pair_counter: Counter = Counter()
    for _, row in df.iterrows():
        nums = sorted(row[COLS_NUMBERS].tolist())
        for a, b in itertools.combinations(nums, 2):
            pair_counter[(a, b)] += 1
    rows = [{"数字A": a, "数字B": b, "同時出現回数": cnt} for (a, b), cnt in pair_counter.most_common(top_n)]
    return pd.DataFrame(rows).reset_index(drop=True)


def carry_over_rate(df: pd.DataFrame) -> float:
    if len(df) < 2:
        return 0.0
    total, hit = 0, 0
    for i in range(1, len(df)):
        prev = set(df.loc[i - 1, COLS_NUMBERS].tolist())
        curr = set(df.loc[i, COLS_NUMBERS].tolist())
        total += 1
        if prev & curr:
            hit += 1
    return round(hit / total * 100, 2) if total else 0.0


# ─────────────────────────────────────────────
# ハイブリッド生成エンジン
# ─────────────────────────────────────────────
def has_consecutive(nums: list) -> bool:
    s = sorted(nums)
    return any(s[i + 1] - s[i] == 1 for i in range(len(s) - 1))


def generate_hybrid(
    prev_nums: list,
    n_patterns: int = 5,
    sum_min: int = 100,
    sum_max: int = 180,
    high_min: int = 2,
    high_threshold: int = 32,
    max_trials: int = 500_000,
) -> list:
    results = []
    prev_set = set(prev_nums)
    trial = 0
    while len(results) < n_patterns and trial < max_trials:
        trial += 1
        nums = sorted(random.sample(range(1, 44), 6))
        total = sum(nums)
        if not (sum_min <= total <= sum_max):
            continue
        high_count = sum(1 for n in nums if n >= high_threshold)
        if high_count < high_min:
            continue
        carry = bool(set(nums) & prev_set)
        consec = has_consecutive(nums)
        if not (carry or consec):
            continue
        results.append({
            "numbers": nums, "trial": trial, "total": total,
            "high_count": high_count, "carry": carry, "consecutive": consec,
        })
    return results


# ─────────────────────────────────────────────
# Plotly テーマ
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Rajdhani, sans-serif", color="#94a3b8"),
    margin=dict(l=4, r=4, t=36, b=4),
    xaxis=dict(gridcolor="#1e3a5f44", zerolinecolor="#1e3a5f44"),
    yaxis=dict(gridcolor="#1e3a5f44", zerolinecolor="#1e3a5f44"),
)

COLORSCALE = [[0.0,"#1e3a5f"],[0.3,"#1d4ed8"],[0.6,"#38bdf8"],[1.0,"#e879f9"]]

# ─────────────────────────────────────────────
# サイドバー
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙ Configuration</div>', unsafe_allow_html=True)

    # CSV
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**📂 データファイル**")
    uploaded_file = st.file_uploader(
        "CSVをアップロード", type=["csv"],
        help="列: 開催回, 日付, 第1数字〜第6数字, ボーナス数字",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # 最新番号
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**🔢 最新当選番号**")
    latest_round = st.number_input("開催回", min_value=1, value=1, step=1)
    # 3列×2行で入力 → モバイルでも収まる
    ca, cb, cc = st.columns(3)
    n1 = ca.number_input("①", 1, 43, 1,  key="n1", label_visibility="visible")
    n2 = cb.number_input("②", 1, 43, 7,  key="n2", label_visibility="visible")
    n3 = cc.number_input("③", 1, 43, 15, key="n3", label_visibility="visible")
    n4 = ca.number_input("④", 1, 43, 22, key="n4", label_visibility="visible")
    n5 = cb.number_input("⑤", 1, 43, 31, key="n5", label_visibility="visible")
    n6 = cc.number_input("⑥", 1, 43, 40, key="n6", label_visibility="visible")
    manual_prev = sorted(list({n1, n2, n3, n4, n5, n6}))
    if len(manual_prev) < 6:
        st.warning("6つの異なる数字を入力してください。")
    st.markdown('</div>', unsafe_allow_html=True)

    # パラメータ
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**🎛 生成パラメータ**")
    sum_min  = st.slider("合計値 下限", 70,  150, 100)
    sum_max  = st.slider("合計値 上限", 130, 250, 180)
    high_thr = st.slider("高数字の閾値",  20,  42,  32)
    high_min = st.slider("高数字の最低個数", 1, 4, 2)
    n_patterns = st.slider("生成パターン数", 1, 10, 5)
    use_manual = st.checkbox("手動入力番号を「前回」として使用", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# データ読み込み
# ─────────────────────────────────────────────
df = None
if uploaded_file is not None:
    try:
        df = load_and_validate(uploaded_file.read(), uploaded_file.name)
        st.sidebar.success(f"✅ {len(df)} 件読み込み完了")
    except Exception as e:
        st.sidebar.error(f"❌ {e}")

if df is not None and len(df) >= 1:
    last_row = df.iloc[-1]
    prev_nums_csv = last_row[COLS_NUMBERS].tolist()
    prev_round    = int(last_row["開催回"])
else:
    prev_nums_csv = None
    prev_round    = None

if use_manual or prev_nums_csv is None:
    prev_nums = manual_prev
    prev_round_display = f"第{latest_round}回（手動入力）"
else:
    prev_nums = prev_nums_csv
    prev_round_display = f"第{prev_round}回（CSV最終行）"

# ─────────────────────────────────────────────
# ヘッダー
# ─────────────────────────────────────────────
st.markdown('<div class="hero-title">🎯 LOTO6 ORACLE</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Statistical Analysis &amp; Hybrid Number Generation Engine</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sidebar-hint">← 左上のメニュー（☰）から設定・CSV読込ができます</div>',
    unsafe_allow_html=True,
)

# 前回番号バー
balls_prev = " ".join(
    [f'<span style="display:inline-block;background:radial-gradient(circle at 35% 35%,#60a5fa,#1d4ed8);'
     f'color:#fff;border-radius:50%;width:32px;height:32px;line-height:32px;text-align:center;'
     f'font-family:Orbitron,monospace;font-weight:700;font-size:0.75rem;margin:2px;">{n}</span>'
     for n in prev_nums]
)
st.markdown(
    f'<div class="stat-card" style="padding:0.7rem 1rem;">'
    f'<div class="stat-card-title">前回参照番号 ── {prev_round_display}</div>'
    f'<div style="margin-top:0.4rem;display:flex;flex-wrap:wrap;gap:4px;align-items:center;">{balls_prev}</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# タブ
# ─────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊  統計データ分析", "🎯  番号予想エンジン"])

# ══════════════════════════════════════════════
# TAB 1 : 統計データ分析
# ══════════════════════════════════════════════
with tab1:
    if df is None:
        st.markdown(
            """
            <div style="text-align:center;padding:3rem 1rem;color:#64748b;">
                <div style="font-size:2.5rem;margin-bottom:0.8rem;">📂</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;letter-spacing:0.08em;">
                    左上のメニュー（☰）からCSVをアップロード
                </div>
                <div style="font-size:0.82rem;margin-top:0.4rem;color:#475569;">
                    列構成: 開催回, 日付, 第1数字〜第6数字, ボーナス数字
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # ── KPI（2列 → スマホでは1列）
        all_nums   = get_all_drawn_numbers(df)
        freq       = Counter(all_nums)
        most_n, most_c = freq.most_common(1)[0]
        rarest_n   = min(freq, key=freq.get)
        carry_rate = carry_over_rate(df)

        k1, k2 = st.columns(2)
        k1.metric("総開催回数",     f"{len(df):,} 回")
        k2.metric("ひっぱり発生率", f"{carry_rate} %")
        k3, k4 = st.columns(2)
        k3.metric("最多出現数字", f"No.{most_n}", f"{most_c} 回")
        k4.metric("最少出現数字", f"No.{rarest_n}", f"{freq[rarest_n]} 回")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 出現回数バーチャート
        st.markdown(
            '<div class="section-header"><span>▎</span> 各数字の出現回数ランキング</div>',
            unsafe_allow_html=True,
        )
        freq_df = frequency_ranking(df)
        fig_freq = go.Figure(go.Bar(
            x=freq_df["数字"].tolist(),
            y=freq_df["出現回数"].tolist(),
            marker=dict(color=freq_df["出現回数"].tolist(), colorscale=COLORSCALE, showscale=False, line=dict(width=0)),
            hovertemplate="数字 %{x}<br>出現 %{y} 回<extra></extra>",
        ))
        fig_freq.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="数字別出現回数（1〜43）", font=dict(color="#94a3b8", size=12)),
            height=280,
            bargap=0.12,
        )
        fig_freq.update_xaxes(tickmode="linear", tick0=1, dtick=2)
        st.plotly_chart(fig_freq, use_container_width=True)

        # ── ヒートマップ
        heat_vals = [freq.get(i, 0) for i in range(1, 44)]
        padded    = heat_vals + [0] * (48 - len(heat_vals))
        heat_mat  = np.array(padded, dtype=float).reshape(6, 8)
        labels    = [[str(r*8+c+1) if r*8+c+1 <= 43 else "" for c in range(8)] for r in range(6)]
        fig_heat  = go.Figure(go.Heatmap(
            z=heat_mat, text=labels, texttemplate="%{text}",
            colorscale=COLORSCALE, showscale=True,
            hovertemplate="数字 %{text}<br>出現 %{z:.0f} 回<extra></extra>",
        ))
        fig_heat.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text="出現頻度ヒートマップ（濃いほど高頻度）", font=dict(color="#94a3b8", size=12)),
            height=220,
            xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

        # ── ペア相性
        st.markdown(
            '<div class="section-header"><span>▎</span> ペア相性 TOP20</div>',
            unsafe_allow_html=True,
        )
        pair_df = pair_affinity(df, top_n=20)
        pair_df["ペア"] = pair_df["数字A"].astype(str) + " - " + pair_df["数字B"].astype(str)
        fig_pair = go.Figure(go.Bar(
            x=pair_df["同時出現回数"].tolist()[::-1],
            y=pair_df["ペア"].tolist()[::-1],
            orientation="h",
            marker=dict(color=pair_df["同時出現回数"].tolist()[::-1], colorscale=COLORSCALE, showscale=False),
            hovertemplate="%{y}<br>同時出現 %{x} 回<extra></extra>",
        ))
        fig_pair.update_layout(**PLOTLY_LAYOUT, height=400, bargap=0.2)
        st.plotly_chart(fig_pair, use_container_width=True)

        # データテーブル（2列 → タブレット以下で1列ずつ）
        c1, c2 = st.columns(2)
        with c1:
            st.caption("ペア相性ランキング")
            st.dataframe(pair_df[["ペア","同時出現回数"]].head(20), use_container_width=True, hide_index=True)
        with c2:
            st.caption("数字出現回数ランキング")
            st.dataframe(freq_df.head(20), use_container_width=True)

        # ── ひっぱり分析
        st.markdown(
            '<div class="section-header"><span>▎</span> ひっぱり数字の分析</div>',
            unsafe_allow_html=True,
        )
        carry_counts = []
        for i in range(1, len(df)):
            prev_s = set(df.loc[i-1, COLS_NUMBERS].tolist())
            curr_s = set(df.loc[i,   COLS_NUMBERS].tolist())
            carry_counts.append(len(prev_s & curr_s))

        fig_carry = go.Figure(go.Histogram(
            x=carry_counts, nbinsx=7,
            marker=dict(color="#38bdf8", opacity=0.8, line=dict(color="#0f172a", width=1)),
            hovertemplate="ひっぱり個数 %{x}<br>回数 %{y}<extra></extra>",
        ))
        fig_carry.update_layout(
            **PLOTLY_LAYOUT,
            title=dict(text=f"ひっぱり個数分布  （全体発生率: {carry_rate}%）", font=dict(color="#94a3b8", size=12)),
            height=240,
        )
        fig_carry.update_xaxes(title_text="ひっぱり個数", dtick=1)
        fig_carry.update_yaxes(title_text="開催回数")
        st.plotly_chart(fig_carry, use_container_width=True)

        with st.expander("📋 読み込みデータプレビュー（最新20件）"):
            st.dataframe(df.tail(20), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# TAB 2 : 番号予想エンジン
# ══════════════════════════════════════════════
with tab2:
    # 条件サマリー（3列 → モバイルで縦スタック）
    cond1, cond2, cond3 = st.columns(3)
    with cond1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-card-title">条件A ─ 合計値</div>'
            f'<div class="stat-card-value">{sum_min}<span class="stat-card-unit">〜{sum_max}</span></div></div>',
            unsafe_allow_html=True,
        )
    with cond2:
        st.markdown(
            f'<div class="stat-card"><div class="stat-card-title">条件B ─ 高数字 ≥{high_thr}</div>'
            f'<div class="stat-card-value">{high_min}<span class="stat-card-unit">個以上</span></div></div>',
            unsafe_allow_html=True,
        )
    with cond3:
        st.markdown(
            '<div class="stat-card"><div class="stat-card-title">条件C ─ ひっぱり or 連番</div>'
            '<div class="stat-card-value">1<span class="stat-card-unit">つ以上</span></div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if len(manual_prev) < 6 and use_manual:
        st.error("⚠️ サイドバーで6つの異なる前回番号を入力してください。")
    else:
        if st.button(f"🎯  予想番号を {n_patterns} パターン生成する"):
            with st.spinner("ハイブリッドエンジン稼働中..."):
                results = generate_hybrid(
                    prev_nums=prev_nums,
                    n_patterns=n_patterns,
                    sum_min=sum_min, sum_max=sum_max,
                    high_min=high_min, high_threshold=high_thr,
                )

            if not results:
                st.error("⚠️ 条件を満たす組み合わせが見つかりませんでした。パラメータを緩和してください。")
            else:
                st.markdown(
                    '<div class="section-header"><span>▎</span> 推奨買い目</div>',
                    unsafe_allow_html=True,
                )
                prev_set_local = set(prev_nums)

                for idx, r in enumerate(results, start=1):
                    nums_list = r["numbers"]

                    # ボール HTML
                    balls_html = ""
                    for n in nums_list:
                        if n in prev_set_local:
                            cls = "ball ball-red"
                        elif n >= high_thr:
                            cls = "ball ball-gold"
                        else:
                            cls = "ball ball-blue"
                        balls_html += f'<div class="{cls}">{n}</div>'

                    carry_b = (
                        '<span class="badge badge-ok">✓ ひっぱり</span>'
                        if r["carry"] else
                        '<span class="badge badge-off">─ ひっぱりなし</span>'
                    )
                    consec_b = (
                        '<span class="badge badge-ok">✓ 連番</span>'
                        if r["consecutive"] else
                        '<span class="badge badge-off">─ 連番なし</span>'
                    )

                    st.markdown(
                        f"""
                        <div class="pred-card">
                            <div class="pred-card-header">
                                <div class="pred-card-num">PATTERN #{idx:02d}</div>
                                <div class="badge-row">{carry_b}{consec_b}</div>
                            </div>
                            <div class="ball-row">{balls_html}</div>
                            <div class="pred-meta">
                                <div class="pred-meta-item">試行 <span>{r['trial']:,}</span></div>
                                <div class="pred-meta-item">合計 <span>{r['total']}</span></div>
                                <div class="pred-meta-item">≥{high_thr} が <span>{r['high_count']}個</span></div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # 凡例
                st.markdown(
                    f"""
                    <div class="legend-bar">
                        <span><span class="legend-ball ball-red" style="background:radial-gradient(circle at 35% 35%,#f87171,#b91c1c);"> </span>ひっぱり（前回重複）</span>
                        <span><span class="legend-ball ball-gold" style="background:radial-gradient(circle at 35% 35%,#fbbf24,#d97706);"> </span>高数字 ≥{high_thr}</span>
                        <span><span class="legend-ball ball-blue" style="background:radial-gradient(circle at 35% 35%,#60a5fa,#1d4ed8);"> </span>その他</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # サマリーテーブル
                if len(results) > 1:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(
                        '<div class="section-header"><span>▎</span> 生成結果サマリー</div>',
                        unsafe_allow_html=True,
                    )
                    summary_df = pd.DataFrame([
                        {
                            "Pattern": f"#{i+1:02d}",
                            "数字": " - ".join(map(str, r["numbers"])),
                            "合計": r["total"],
                            f"≥{high_thr}": r["high_count"],
                            "ひっぱり": "✓" if r["carry"] else "─",
                            "連番": "✓" if r["consecutive"] else "─",
                            "試行": r["trial"],
                        }
                        for i, r in enumerate(results)
                    ])
                    st.dataframe(summary_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# フッター
# ─────────────────────────────────────────────
st.markdown(
    """
    <div class="footer-bar">
        LOTO6 ORACLE ─ Statistical Analysis Tool<br>
        ※ 本ツールは統計的分析に基づく参考情報です。当選を保証するものではありません。
    </div>
    """,
    unsafe_allow_html=True,
)
