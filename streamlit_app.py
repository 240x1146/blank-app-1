import streamlit as st
from supabase import create_client, Client

# --- 1. Supabase接続設定 (Secretsから読み込み) ---
# ※あらかじめStreamlitのSettings > SecretsにURLとKEYを設定しておいてください
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Supabaseの接続設定が見つかりません。Secretsを確認してください。")

# --- 2. アプリの設定とタイトルの表示 ---
st.set_page_config(page_title="K-Pop推し診断", layout="wide")

# 画像をきれいに揃えるためのカスタムCSS
st.markdown(
    """
    <style>
    img {
        height: 300px !important;
        width: 100% !important;
        object-fit: cover !important;
        border-radius: 10px;
    }
    .stButton > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💖 K-Popパーツ診断アプリ 💖")
st.write("イメージ図を参考に、あなたの好みを直感的に選んでください！")

# ニックネーム入力（保存用に追加しました）
user_name = st.text_input("あなたのニックネーム", value="ゲスト")

# 3. セッション状態の初期化
if 'selections' not in st.session_state:
    st.session_state.selections = {"style": None, "hair": None, "face_type": None}

# --- 診断用パーツ選択セクション ---
st.header("1. 全体の雰囲気は？")
col1, col2 = st.columns(2)
with col1:
    st.image("https://assets.st-note.com/production/uploads/images/77120728/rectangle_large_type_2_1fbd4ace7023a5295f2b44f31681a476.jpg?width=1280", caption="柔らかい・愛らしい")
    if st.button("かわいい系を選ぶ"):
        st.session_state.selections["style"] = "かわいい系"
with col2:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSq_kX8fXQ_N8F5F1G5G-Z5G5G5G5G5G5G5G&s", caption="綺麗・大人っぽい")
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
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzR-rR1-rR1-rR1-rR1-rR1-rR1-rR1-rR1&s", caption="人懐っこい愛嬌の犬顔")
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
            res_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzR-rR1-rR1-rR1-rR1-rR1-rR1-rR1-rR1&s"
        else:
            res_name = "アン・ユジン (IVE)"
            res_desc = "大型犬のような明るいエネルギーと、誰からも愛される健康的なビジュアル。"
            res_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSiNP8fOOGeP7ptsf700c4M-bqmAdQgMmunTQIZchyJ-g&s"

        st.divider()
        st.balloons()
        st.header(f"あなたへの提案：{res_name}")
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.image(res_img, use_container_width=True)
        with c_res2:
            st.write(res_desc)
            st.info("このアイドルをチェックしてみましょう！")

        # --- ★ここでSupabaseに保存 ---
        data = {
            "user_name": user_name,
            "result_group": res_name
        }
        try:
            supabase.table("kpop_diagnosis_logs").insert(data).execute()
            st.toast("診断結果をデータベースに保存しました！")
        except Exception as e:
            st.error(f"データの保存に失敗しました: {e}")

# 過去の履歴を表示する（任意）
if st.checkbox("みんなの診断履歴を表示"):
    res = supabase.table("kpop_diagnosis_logs").select("*").order("created_at", desc=True).execute()
    if res.data:
        st.table(res.data)