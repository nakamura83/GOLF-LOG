import streamlit as st
import google.generativeai as genai
import os

# ページ設定
st.set_page_config(page_title="My AI App")
st.title("AIチャットアプリ")

# 1. APIキーの設定（後でStreamlitの画面で設定します）
# 念のため環境変数から読み込む設定
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    # Streamlit CloudのSecretsから読み込む
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except:
        st.error("APIキーが設定されていません。StreamlitのSecretsにGEMINI_API_KEYを設定してください。")
        st.stop()

genai.configure(api_key=api_key)

# ---------------------------------------------------------
# 2. ここから下を、あなたのGoogle AI Studioのコードに書き換えます
# ---------------------------------------------------------

# ★ここにある generation_config と model の設定を
# Google AI Studioの「Get code」の内容で上書きしてください！

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# system_instructionがあればここに書く
system_instruction ="""
あなたはプロのゴルフコーチです。
優しく指導してください。
"""

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash", # または gemini-1.5-pro
  generation_config=generation_config,
  system_instruction=system_instruction,
)

# ---------------------------------------------------------
# 書き換えエリア終了
# ---------------------------------------------------------

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 履歴を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーの入力待ち
if prompt := st.chat_input("何か話しかけてください"):
    # ユーザーの入力を表示
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AIの応答を生成
    with st.chat_message("assistant"):
        # チャットセッションを開始（履歴を含める）
        chat_history = [
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1] # 今回の入力以外を履歴とする
        ]
        chat = model.start_chat(history=chat_history)
        
        response = chat.send_message(prompt)
        st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})
