import streamlit as st

# アプリのタイトル
st.set_page_config(page_title="K-Pop推し診断", layout="wide")
st.title("💖 K-Popパーツ診断アプリ 💖")
st.write("イメージ図を参考に、あなたの好みを直感的に選んでください！")

# セッション状態の初期化
if 'selections' not in st.session_state:
    st.session_state.selections = {"style": None, "hair": None, "eye": None, "face_type": None}

# 画像をリサイズして表示するための設定
# すべての st.image に use_container_width=True を追加します

# --- ステップ1：雰囲気 ---
st.header("1. 全体の雰囲気は？")
col1, col2 = st.columns(2)
with col1:
    st.image("https://assets.st-note.com/production/uploads/images/77120728/rectangle_large_type_2_1fbd4ace7023a5295f2b44f31681a476.jpg?width=1280", 
             caption="柔らかい・愛らしい", use_container_width=True)
    if st.button("かわいい系を選ぶ"):
        st.session_state.selections["style"] = "かわいい系"
with col2:
    st.image("https://hips.hearstapps.com/hmg-prod/images/tzuyu-of-twice-attends-the-29th-high1-seoul-music-awards-news-photo-1615387889.?crop=0.709xw:0.593xh;0.143xw,0", 
             caption="綺麗・大人っぽい", use_container_width=True)
    if st.button("美人系を選ぶ"):
        st.session_state.selections["style"] = "美人系"

# --- ステップ2：髪型 ---
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

# --- ステップ3：目元 ---
st.header("3. 目元の印象は？")
col5, col6 = st.columns(2)
with col5:
    st.image("https://via.placeholder.com/800x500.png?text=Double+Eyelid", 
             caption="ぱっちり二重", use_container_width=True)
    if st.button("二重を選ぶ"):
        st.session_state.selections["eye"] = "二重"
with col6:
    st.image("https://cdn.michill.jp/v2/w_640,h_640,f_webp,q_90/img/articles/73052/0.jpg", 
             caption="クールな一重・奥二重", use_container_width=True)
    if st.button("一重を選ぶ"):
        st.session_state.selections["eye"] = "一重"

# --- ステップ4：顔のタイプ (猫顔 or 犬顔) ---
st.header("4. 顔のタイプは？")
col7, col8 = st.columns(2)
with col7:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSiNP8fOOGeP7ptsf700c4M-bqmAdQgMmunTQIZchyJ-g&s", 
             caption="ツンとした美しさの猫顔", use_container_width=True)
    if st.button("猫顔を選ぶ"):
        st.session_state.selections["face_type"] = "猫顔"
with col8:
    st.image("https://via.placeholder.com/800x500.png?text=Dog+Face", 
             caption="人懐っこい愛嬌の犬顔", use_container_width=True)
    if st.button("犬顔を選ぶ"):
        st.session_state.selections["face_type"] = "犬顔"

# --- サイドバー ---
st.sidebar.header("現在の選択状況")
for key, value in st.session_state.selections.items():
    label = {"style": "雰囲気", "hair": "髪型", "eye": "目元", "face_type": "顔タイプ"}[key]
    st.sidebar.write(f"**{label}**: {value if value else '未選択'}")

# --- 診断実行 ---
if st.button("✨ この条件で推しを診断する ✨"):
    if None in st.session_state.selections.values():
        st.error("全ての項目を選択してください！")
    else:
        s = st.session_state.selections
        if s["style"] == "美人系" and s["face_type"] == "猫顔":
            res_name = "ウォニョン (IVE)"
            res_desc = "圧倒的なカリスマ性と猫のような気品溢れるビジュアル。まさに現代のアイコン！"
            res_img = "https://via.placeholder.com/400x500.png?text=WONYOUNG"
        elif s["style"] == "かわいい系" and s["face_type"] == "犬顔":
            res_name = "ソリュン (NMIXX)"
            res_desc = "お人形のような愛らしさと、犬のように人懐っこい瞳が魅力的なビジュアルクイーン。"
            res_img = "https://via.placeholder.com/400x500.png?text=SULLYOON"
        elif s["face_type"] == "猫顔":
            res_name = "チキータ (BABYMONSTER)"
            res_desc = "末っ子ながらクールで猫のような鋭いパフォーマンスが目を引く新星。"
            res_img = "https://via.placeholder.com/400x500.png?text=CHIQUITA"
        else:
            res_name = "アン・ユジン (IVE)"
            res_desc = "大型犬のような明るいエネルギーと、誰からも愛される健康的なビジュアルの持ち主。"
            res_img = "https://via.placeholder.com/400x500.png?text=ANYUJIN"

        st.divider()
        st.balloons()
        st.header(f"あなたへの提案：{res_name}")
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.image(res_img, use_container_width=True)
        with c_res2:
            st.write(res_desc)
            st.info("このアイドルをチェックしてみましょう！")