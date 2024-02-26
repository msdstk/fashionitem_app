import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from model import predict
import time

# CSSを使って背景色を設定する関数
def set_bg_color():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #f9f4ff;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 関数を呼び出して背景色を設定
set_bg_color()

st.sidebar.title("ファッションアイテム認識アプリ👚")
st.sidebar.write("読み込んだ画像から上位3位のアイテムを判定します。")

st.sidebar.write("")

img_source = st.sidebar.radio("画像を読み込む方法を選択してください。",
                              ("画像をアップロード", "カメラで撮影"))
if img_source == "画像をアップロード":
    img_file = st.sidebar.file_uploader("画像を選択してください。", type=["png", "jpg", "jpeg"])
elif img_source == "カメラで撮影":
    img_file = st.camera_input("カメラで撮影")

if img_file is not None:
    with st.spinner("判定中..."):
        time.sleep(3)
        img = Image.open(img_file)
        st.image(img, caption="対象の画像", width=480)
        st.write("")

        # 予測
        results = predict(img)

        # 結果の表示
        st.subheader("判定結果")
        # 確率が高い順に3位まで表示する
        n_top = 3
        for result in results[:n_top]:
            st.write(str(round(result[2]*100, 2)) + "%の確率で" + result[0] + "です。")
            st.snow()

        # 結果の円グラフを表示
        pie_labels = [result[1] for result in results[:n_top]]
        pie_labels.append("others")
        pie_probs = [result[2] for result in results[:n_top]]
        pie_probs.append(sum([result[2] for result in results[n_top:]]))
        fig, ax = plt.subplots()
        wedgeprops={"width":0.3, "edgecolor":"white"}
        textprops = {"fontsize":6}
        ax.pie(pie_probs, labels=pie_labels, counterclock=False, startangle=90,
               textprops=textprops, autopct="%.2f", wedgeprops=wedgeprops)
        st.pyplot(fig)

st.sidebar.write("")
st.sidebar.write("")
