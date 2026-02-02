import streamlit as st
from supabase import create_client, Client

# --- 1. Supabase接続設定 ---
# SecretsからURLとKEYを読み込み、データベースと接続します
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Supabaseの接続設定が見つかりません。StreamlitのSecrets設定を確認してください。")

# --- 2. アプリの設定とレイアウトの修正 ---
st.set_page_config(page_title="K-Pop推し診断", layout="wide")

# 【改良】aspect-ratioを使用して、すべての写真を「正方形」に統一し、中央で切り抜きます
st.markdown(
    """
    <style>
    img {
        aspect-ratio: 1 / 1 !important; /* 縦横比を1:1(正方形)に固定 */
        width: 100% !important;
        object-fit: cover !important; /* はみ出す部分を中央でカット */
        border-radius: 10px;
    }
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

# データの保存に必要なお名前入力
user_name = st.text_input("あなたのニックネーム", value="ゲスト")

# 3. セッション状態の初期化
if 'selections' not in st.session_state:
    st.session_state.selections = {"style": None, "hair": None, "face_type": None}

# --- 診断パーツ選択セクション (元の構成を維持) ---
st.header("1. 全体の雰囲気は？")
col1, col2 = st.columns(2)
with col1:
    st.image("https://assets.st-note.com/production/uploads/images/77120728/rectangle_large_type_2_1fbd4ace7023a5295f2b44f31681a476.jpg?width=1280", caption="柔らかい・愛らしい")
    if st.button("かわいい系を選ぶ"):
        st.session_state.selections["style"] = "かわいい系"
with col2:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFOP36TqXvqDwhGhH6kpvynSNHr9lQGFTZOg&s", caption="綺麗・大人っぽい")
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
    st.image("data:image/jpeg;base64,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", caption="人懐っこい愛嬌の犬顔")
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
        
        # 元の判定ロジックを活用
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

        # --- Supabaseへデータを保存 ---
        # 診断が行われた瞬間にテーブルへ書き込みます
        data = {
            "user_name": user_name,
            "result_group": res_name
        }
        try:
            supabase.table("kpop_diagnosis_logs").insert(data).execute()
            st.toast("診断結果をデータベースに保存しました！")
        except Exception as e:
            st.error(f"データの保存に失敗しました: {e}")

# 過去の履歴を表示する（みんなの結果が見えて楽しくなります）
if st.checkbox("みんなの診断履歴を表示"):
    try:
        res = supabase.table("kpop_diagnosis_logs").select("*").order("created_at", desc=True).execute()
        if res.data:
            st.table(res.data)
    except:
        st.info("履歴を取得できません。")