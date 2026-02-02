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
    st.image("data:image/jpeg;base64,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", 
             caption="柔らかい・愛らしい", use_container_width=True)
    if st.button("かわいい系を選ぶ"):
        st.session_state.selections["style"] = "かわいい系"
with col2:
    # 綺麗・大人っぽい（リズちゃん）の画像
    st.image("https://cdn.livedoor.jp/kstyle/73b93eb0acf76c5e4b1cab943e4c77a6.jpg/r.580x0",        
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
    st.image("https://hips.hearstapps.com/hmg-prod/images/img-1856-66d1a55b5b742.jpeg?crop=1xw:1xh;center,top&resize=980:*", 
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