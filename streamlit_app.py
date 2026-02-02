import streamlit as st
from supabase import create_client, Client

# --- 1. Supabase接続設定 ---
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Supabaseの接続設定が見つかりません。Secretsを確認してください。")

# --- 2. アプリの設定とレイアウトの修正 ---
st.set_page_config(page_title="K-Pop推し診断", layout="wide")

# 画像のサイズと比率を完全に統一するためのCSS
st.markdown(
    """
    <style>
    /* 全ての画像を正方形(1:1)に固定してサイズを統一 */
    [data-testid="stImage"] img {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important; /* 縦横比を1:1に固定 */
        object-fit: cover !important;  /* 比率を保ったまま枠いっぱいに表示（中央切り抜き） */
        border-radius: 10px;
        display: block;
    }
    /* ボタンの横幅を画像に合わせ、高さも揃える */
    .stButton > button {
        width: 100%;
        height: 3em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💖 K-Popパーツ診断アプリ 💖")
st.write("イメージ図を参考に、あなたの好みを直感的に選んでください！")

# ニックネーム入力
user_name = st.text_input("あなたのニックネーム", value="ゲスト")

# 3. セッション状態の初期化
if 'selections' not in st.session_state:
    st.session_state.selections = {"style": None, "hair": None, "face_type": None}

# --- 診断パーツ選択セクション ---
# カラムを使って画像を横に並べる。CSSの効果で高さが自動で揃います。
st.header("1. 全体の雰囲気は？")
col1, col2 = st.columns(2)
with col1:
    st.image("https://assets.st-note.com/production/uploads/images/77120728/rectangle_large_type_2_1fbd4ace7023a5295f2b44f31681a476.jpg?width=1280", caption="柔らかい・愛らしい")
    if st.button("かわいい系を選ぶ"):
        st.session_state.selections["style"] = "かわいい系"
with col2:
    st.image("data:image/jpeg;base64,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", caption="綺麗・大人っぽい")
    if st.button("美人系を選ぶ"):
        st.session_state.selections["style"] = "美人系"

st.header("2. 髪型は？")
col3, col4 = st.columns(2)
with col3:
    st.image("https://www.lemon8-app.com/seo/image?item_id=7486886065383588407&index=0&sign=a1759eff2a3c84d50a29c6dbf79e1725", caption="王道のロングヘア")
    if st.button("ロングを選ぶ"):
        st.session_state.selections["hair"] = "ロング"
with col4:
    st.image("https://cdn-ak.f.st-hatena.com/images/fotolife/t/teajo/20240630/20240630202242.jpg", caption="爽やかなショート・ボブ")
    if st.button("ショートを選ぶ"):
        st.session_state.selections["hair"] = "ショート"

st.header("3. 顔のタイプは？")
col5, col6 = st.columns(2)
with col5:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSiNP8fOOGeP7ptsf700c4M-bqmAdQgMmunTQIZchyJ-g&s", caption="ツンとした美しさの猫顔")
    if st.button("猫顔を選ぶ"):
        st.session_state.selections["face_type"] = "猫顔"
with col6:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2F4mKpmRaGDeFkiHw_rPEQqlfEffobyTZYA&s", caption="人懐っこい愛嬌の犬顔")
    if st.button("犬顔を選ぶ"):
        st.session_state.selections["face_type"] = "犬顔"

# サイドバーに現在の選択を表示
st.sidebar.header("現在の選択状況")
for key, value in st.session_state.selections.items():
    label = {"style": "雰囲気", "hair": "髪型", "face_type": "顔タイプ"}[key]
    st.sidebar.write(f"**{label}**: {value if value else '未選択'}")

# --- 4. 診断実行とデータ保存 ---
if st.button("✨ この条件で推しを診断する ✨"):
    if None in st.session_state.selections.values():
        st.error("全ての項目を選択してください！")
    else:
        s = st.session_state.selections
        
        # 判定ロジック
        if s["style"] == "美人系" and s["face_type"] == "猫顔":
            res_name = "ウォニョン (IVE)"
            res_desc = "圧倒的なカリスマ性と猫のような気品。まさに現代のアイコン！"
            res_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSEYPQPYGxNHam0YruA9HcVCi312VFThOR9PHnd9MyfQ&s"
        elif s["style"] == "かわいい系" and s["face_type"] == "犬顔":
            res_name = "ソリュン (NMIXX)"
            res_desc = "お人形のような愛らしさと人懐っこい瞳。ビジュアルクイーンです。"
            res_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSiNP8fOOGeP7ptsf700c4M-bqmAdQgMmunTQIZchyJ-g&s"
        elif s["face_type"] == "猫顔":
            res_name = "チキータ (BABYMONSTER)"
            res_desc = "クールで猫のような鋭いパフォーマンスが目を引く新星！"
            res_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfI3-rR1-rR1-rR1-rR1-rR1-rR1-rR1-rR1&s"
        else:
            res_name = "アン・ユジン (IVE)"
            res_desc = "大型犬のような明るいエネルギーと、誰からも愛される健康的なビジュアル。"
            res_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzR-rR1-rR1-rR1-rR1-rR1-rR1-rR1-rR1&s"

        st.divider()
        st.balloons()
        st.header(f"あなたへの提案：{res_name}")
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.image(res_img, use_container_width=True)
        with c_res2:
            st.write(res_desc)
            st.info("このアイドルをチェックしてみましょう！")

        # --- Supabaseへデータを保存 ---
        data = {"user_name": user_name, "result_group": res_name}
        try:
            supabase.table("kpop_diagnosis_logs").insert(data).execute()
            st.toast("診断結果を保存しました！")
        except Exception as e:
            st.error(f"保存失敗: {e}")

# 過去の履歴を表示
if st.checkbox("みんなの診断履歴を表示"):
    try:
        res = supabase.table("kpop_diagnosis_logs").select("*").order("created_at", desc=True).execute()
        if res.data:
            st.table(res.data)
    except:
        st.info("履歴を取得できません。")