import os
import json
from datetime import datetime

import streamlit as st

def main():
    st.title("スキル評価アプリ")

    # JSONデータの読み込み
    with open("checklist.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # ユーザーの評価結果を保存する辞書
    user_ratings = {}

    # チェックリストごとに表示
    for checklist in data["checklists"]:
        st.header(checklist["title"])
        for item in checklist["items"]:
            st.subheader(item["name"])
            
            # ラジオボタンのオプションを生成
            radio_options = []
            for level in item["levels"]:
                radio_options.append(f"レベル {level['level']}: {level['description']}")

            # ラジオボタンを表示
            selected_option = st.radio(f"{item['name']} のレベルを選択:", radio_options, key=f"{checklist['title']}-{item['name']}")
            
            # 選択されたオプションからレベルを抽出
            selected_level = int(selected_option.split(":")[0].split()[-1])  # ラベルからレベルの数値を取得

            # 選択されたレベルを user_ratings に保存
            user_ratings[f"{checklist['title']}-{item['name']}"] = selected_level

    # 評価結果の表示 (ここでは例として、選択されたレベルを表示)
    if st.button("評価結果を表示"):
        st.write("## 評価結果")
        for key, value in user_ratings.items():
            st.write(f"{key}: レベル {value}")
        
        # 結果を文字列として保存
        result_text = "評価結果\n" + "="*50 + "\n"
        for key, value in user_ratings.items():
            result_line = f"{key}: レベル {value}\n"
            st.write(result_line.strip())
            result_text += result_line

        # 結果をresultディレクトリに保存
        # resultディレクトリが存在しない場合は作成
        os.makedirs("result", exist_ok=True)

        # タイムスタンプを含むファイル名を生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"result/skill_evaluation_{timestamp}.txt"

        # 結果をファイルに保存
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result_text)
        
        st.success(f"結果を {filename} に保存しました")
            
        # ダウンロードボタンを作成
        st.download_button(
            label="結果をテキストファイルとして保存",
            data=result_text,
            file_name="skill_evaluation_result.txt",
            mime="text/plain"
        )
    

if __name__ == "__main__":
    main()