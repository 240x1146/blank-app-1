import streamlit as st

# アプリのタイトル
st.set_page_config(page_title="K-Pop推し診断", layout="wide")
st.title("💖 K-Popパーツ診断アプリ 💖")
st.write("イメージ図を参考に、あなたの好みを直感的に選んでください！")

# セッション状態の初期化（選択を保持するため）
if 'selections' not in st.session_state:
    st.session_state.selections = {"style": None, "hair": None, "eye": None, "height": None}

# --- ステップ1：雰囲気 ---
st.header("1. 全体の雰囲気は？")
col1, col2 = st.columns(2)
with col1:
    st.image("https://assets.st-note.com/production/uploads/images/77120728/rectangle_large_type_2_1fbd4ace7023a5295f2b44f31681a476.jpg?width=1280", caption="柔らかい・愛らしい")
    if st.button("かわいい系を選ぶ"):
        st.session_state.selections["style"] = "かわいい系"
with col2:
    st.image("https://hips.hearstapps.com/hmg-prod/images/tzuyu-of-twice-attends-the-29th-high1-seoul-music-awards-news-photo-1615387889.?crop=0.709xw:0.593xh;0.143xw,0", caption="綺麗・大人っぽい")
    if st.button("美人系を選ぶ"):
        st.session_state.selections["style"] = "美人系"

# --- ステップ2：髪型 ---
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

# --- ステップ3：目元 ---
st.header("3. 目元の印象は？")
col5, col6 = st.columns(2)
with col5:
    st.image("", caption="ぱっちり二重")
    if st.button("二重を選ぶ"):
        st.session_state.selections["eye"] = "二重"
with col6:
    st.image("https://via.placeholder.com/300x200.png?text=Single+Eyelid", caption="クールな一重・奥二重")
    if st.button("一重を選ぶ"):
        st.session_state.selections["eye"] = "一重"

# --- ステップ4：身長 ---
st.header("4. 身長は？")
col7, col8 = st.columns(2)
with col7:
    st.image("https://via.placeholder.com/300x200.png?text=Tall", caption="モデルのような高身長")
    if st.button("高身長を選ぶ"):
        st.session_state.selections["height"] = "高身長"
with col8:
    st.image("https://via.placeholder.com/300x200.png?text=Small", caption="守りたくなる低身長")
    if st.button("低身長を選ぶ"):
        st.session_state.selections["height"] = "低身長"

# --- 現在の選択状況の表示 ---
st.sidebar.header("現在の選択状況")
for key, value in st.session_state.selections.items():
    st.sidebar.write(f"{key}: {value if value else '未選択'}")

# --- 診断実行 ---
if st.button("✨ この条件で推しを診断する ✨"):
    # 全ての項目が選ばれているかチェック
    if None in st.session_state.selections.values():
        st.error("全ての項目を選択してください！")
    else:
        s = st.session_state.selections
        # 判定ロジック（例）
        if s["style"] == "美人系" and s["height"] == "高身長":
            res_name = "ウォニョン (IVE)"
            res_desc = "誰もが見惚れる圧倒的なスタイルと美人顔！"
            res_img = "https://via.placeholder.com/400x500.png?text=WONYOUNG"
        elif s["style"] == "かわいい系" and s["eye"] == "二重":
            res_name = "ソリュン (NMIXX)"
            res_desc = "お人形のような可愛らしさと大きな瞳が特徴！"
            res_img = "https://via.placeholder.com/400x500.png?text=SULLYOON"
        else:
            res_name = "チキータ (BABYMONSTER)"
            res_desc = "フレッシュな魅力とクールな表情を併せ持つ新星！"
            res_img = "https://via.placeholder.com/400x500.png?text=CHIQUITA"

        st.divider()
        st.balloons()
        st.header(f"あなたへの提案：{res_name}")
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.image(res_img)
        with c_res2:
            st.write(res_desc)