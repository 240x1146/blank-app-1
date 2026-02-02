# 💖 K-Popパーツ診断アプリ 💖

直感的なパーツ選択で、あなたにぴったりのK-Pop推しメンを提案する診断アプリです。

## 🚀 アプリのURL
[こちらからアプリを試用できます](https://blank-app-bbgvnmfislv.streamlit.app/)

## ✨ 主な機能
- **ビジュアル診断**: 「雰囲気」「髪型」「顔のタイプ」の3つのステップを画像で選び、直感的に推しを診断。
- **データ永続化（Supabase連携）**: 診断結果をクラウドデータベース(Supabase)に保存。過去の診断データが消えずに残ります。
- **みんなの診断履歴**: これまでのユーザーの診断結果を一覧で確認することが可能です。
- **レスポンシブデザイン**: CSS(aspect-ratio)を活用し、どんな端末でも画像が綺麗に揃うUIを実現。

## 🛠 使用技術
- **Frontend**: Streamlit (Python)
- **Database**: Supabase
- **Styling**: CSS (Custom Markdown)

## 📝 セットアップ手順（開発者向け）
1. `pip install -r requirements.txt` でライブラリをインストール
2. StreamlitのSecretsに `SUPABASE_URL` と `SUPABASE_KEY` を設定
3. `streamlit run streamlit_app.py` で実行