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

# 【修正ポイント】画像を正方形に統一し、ボタンの幅を揃えるCSS
st.markdown(
    """
    <style>
    /* 全ての画像(imgタグ)の比率を1:1(正方形)に固定 */
    [data-testid="stImage"] img {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        object-fit: cover !important; /* 比率を保ったまま中央で切り抜き */
        border-radius: 10px;
    }
    /* ボタンの横幅を画像に合わせる */
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
# 各質問の st.image に use_container_width=True を追加してサイズを揃えます

st.header("1. 全体の雰囲気は？")
col1, col2 = st.columns(2)
with col1:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROI7J4hAMAg4bLhmvidEVtm0n9W6CWy9_WKw&s", 
             caption="柔らかい・愛らしい", use_container_width=True)
    if st.button("かわいい系を選ぶ"):
        st.session_state.selections["style"] = "かわいい系"
with col2:
    # 綺麗・大人っぽい（リズちゃん）の画像
    st.image("data:image/jpeg;base64,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", 
             caption="綺麗・大人っぽい", use_container_width=True)
    if st.button("美人系を選ぶ"):
        st.session_state.selections["style"] = "美人系"

st.header("2. 髪型は？")
col3, col4 = st.columns(2)
with col3:
    st.image("https://www.lemon8-app.com/seo/image?item_id=7486886065383588407&index=0&sign=a1759eff2a3c84d50a29c6dbf79e1725", 
             caption="王道のロングヘア", use_container_width=True)
    if st.button("ロングを選ぶ"):
        st.session_state.selections["hair"] = "ロング"
with col4:
    st.image("https://cdn-ak.f.st-hatena.com/images/fotolife/t/teajo/20240630/20240630202242.jpg", 
             caption="爽やかなショート・ボブ", use_container_width=True)
    if st.button("ショートを選ぶ"):
        st.session_state.selections["hair"] = "ショート"

st.header("3. 顔のタイプは？")
col5, col6 = st.columns(2)
with col5:
    st.image("https://i.pinimg.com/736x/d6/69/0d/d6690d5d62a5b5e314113a01ce03e1ff.jpg", 
             caption="ツンとした美しさの猫顔", use_container_width=True)
    if st.button("猫顔を選ぶ"):
        st.session_state.selections["face_type"] = "猫顔"
with col6:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTC839uKaB0HhWMGsCfys9G54cXe3A573czTUPdXd9KXkOD5Go5oGUz6HY&s", 
             caption="人懐っこい愛嬌の犬顔", use_container_width=True)
    if st.button("犬顔を選ぶ"):
        st.session_state.selections["face_type"] = "犬顔"

# サイドバー表示
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
        
        # 診断ロジック
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