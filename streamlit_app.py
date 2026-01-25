import streamlit as st

# アプリのタイトル
st.title("💖 K-Pop推しメン診断アプリ 💖")
st.write("あなたの理想のタイプを選択して、「診断する」を押してください！")

# --- 入力セクション ---
st.header("1. 好みのタイプを選択")

# セレクトボックスで条件を選択
type_style = st.radio("全体の雰囲気", ["かわいい系", "美人系"], horizontal=True)
hair = st.radio("髪型", ["ロング", "ショート"], horizontal=True)
eye = st.radio("目元", ["二重", "一重"], horizontal=True)
height = st.radio("身長", ["高身長", "低身長"], horizontal=True)

# --- 診断ロジック ---
def diagnose(type_style, hair, eye, height):
    # 組み合わせに応じたアイドル判定（例）
    if type_style == "かわいい系" and eye == "二重" and height == "低身長":
        return {
            "name": "チキータ (BABYMONSTER)",
            "desc": "末っ子らしい愛らしさと、パワフルなダンスのギャップが魅力！",
            "img": "https://via.placeholder.com/400x500.png?text=Chiquita"
        }
    elif type_style == "美人系" and eye == "二重" and height == "高身長":
        return {
            "name": "ウォニョン (IVE)",
            "desc": "圧倒的なスタイルと気品溢れるビジュアル。まさに現代のアイコンです。",
            "img": "https://via.placeholder.com/400x500.png?text=Wonyoung"
        }
    elif type_style == "美人系" and eye == "二重" and height == "低身長" and hair == "ロング":
        return {
            "name": "ソリュン (NMIXX)",
            "desc": "『ビジュアルの奇跡』と呼ばれるほど整った顔立ちと、高い歌唱力を兼ね備えています。",
            "img": "https://via.placeholder.com/400x500.png?text=Sullyoon"
        }
    elif type_style == "かわいい系" and hair == "ショート":
        return {
            "name": "アン・ユジン (IVE)",
            "desc": "ショートヘアも似合う爽やかで明るいエネルギーが魅力のリーダー！",
            "img": "https://via.placeholder.com/400x500.png?text=An+Yujin"
        }
    else:
        # どの条件にも当てはまらなかった場合のランダム、もしくはデフォルト
        return {
            "name": "K-Pop界のニュースター",
            "desc": "あなたのこだわり条件に合うアイドルは、他にもたくさんいます！ぜひ色々なグループをチェックしてみてください。",
            "img": "https://via.placeholder.com/400x500.png?text=K-Pop+Star"
        }

# --- 実行ボタン ---
if st.button("診断する"):
    result = diagnose(type_style, hair, eye, height)
    
    st.divider()
    st.header(f"あなたにおすすめなのは... {result['name']}")
    
    col_img, col_txt = st.columns([1, 1])
    with col_img:
        st.image(result['img'])
    with col_txt:
        st.write(result['desc'])
        st.success("相性抜群のアイドルが見つかりました！")
        st.balloons()