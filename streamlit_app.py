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
    st.image("https://hips.hearstapps.com/hmg-prod/images/aflo-287889748-68526e6e7650e.jpg?crop=1.00xw:0.527xh;0,0.156xh",
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
        elif s["style"] == "美人系" and s["face_type"] == "犬顔":
            res_name = "ソリュン (NMIXX)"
            res_desc = "お人形のような愛らしさと人懐っこい瞳。ビジュアルクイーンです。"
            res_img = "https://www.lemon8-app.com/seo/image?item_id=7486886065383588407&index=0&sign=a1759eff2a3c84d50a29c6dbf79e1725"
        elif s["style"]  == "かわいい系" and s["face_type"] == "犬顔":
              res_name = "ジウ(NMIXX)"
              res_desc = "一瞬で心を奪う、NMIXXのビタミンエース"
              res_img = "https://hips.hearstapps.com/hmg-prod/images/img-3583-6614d3e041dda.jpeg"
        else:
              res_name = "ウィンター(aespa)"
              res_desc = "静かに燃える、冷静なるエース"
              res_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBHPuPnwFRlur3HwH2tgRssLoJz2qkyQr53A&s" and "https://www.lemon8-app.com/seo/image?item_id=7322459646626267654&index=2&sign=ee609b5c9b0dbcf4ff38ff4c1b4ca6fa"
        
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
