import streamlit as st
import requests

# -----------------------------
# Backend URLs
# -----------------------------
BACKEND_ANALYZE_URL = "http://127.0.0.1:8000/analyze"
BACKEND_CHAT_URL = "http://127.0.0.1:8000/chat"

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Legacy Code Explainer",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "result" not in st.session_state:
    st.session_state.result = None

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# UI Header
# -----------------------------
st.title("🧾 Legacy Code Explainer")
st.markdown("Explain **COBOL** and **JCL** legacy mainframe code using AI.")

# -----------------------------
# Language Selection
# -----------------------------
language = st.selectbox(
    "Select Language",
    ["cobol", "jcl"]
)

# -----------------------------
# Code Input
# -----------------------------
code_input = st.text_area(
    "Paste Legacy Code Here",
    height=300,
    placeholder="Paste COBOL or JCL code here..."
)

# -----------------------------
# Analyze Button
# -----------------------------
if st.button("Analyze Code"):
    if not code_input.strip():
        st.warning("Please paste some code before analyzing.")
    else:
        with st.spinner("Analyzing legacy code..."):
            payload = {
                "code": code_input,
                "language": language,
                "engine": "regex"  # 🔒 FORCE REGEX (ANTLR REMOVED)
            }

            try:
                response = requests.post(BACKEND_ANALYZE_URL, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.result = data
                    st.session_state.session_id = data.get("session_id")
                    st.session_state.chat_history = []
                else:
                    st.error(f"Backend error: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error("Failed to connect to backend.")
                st.text(str(e))

# -----------------------------
# Results Display
# -----------------------------
if st.session_state.result:
    result = st.session_state.result

    st.success("✅ Analysis Complete!")

    show_technical = st.checkbox("Show technical details (IR & Analysis)", value=False)

    # -----------------------------
    # Explanation
    # -----------------------------
    st.subheader("📝 Explanation")
    st.write(result.get("explanation", "No explanation generated."))

    # -----------------------------
    # IR + Analysis Summary
    # -----------------------------
    if show_technical:
        col1, col2 = st.columns(2)

        # ---- IR COLUMN ----
        with col1:
            st.subheader("📦 Intermediate Representation (IR)")

            ir = (
                result.get("intermediate_representation")
                or result.get("ir")
                or result.get("analysis", {}).get("intermediate_representation")
                or {}
            )

            if ir:
                st.json(ir)
            else:
                st.info(
                    "ℹ️ No Intermediate Representation generated yet.\n\n"
                    "This usually means parser rules did not match the input code."
                )

        # ---- SUMMARY COLUMN ----
        with col2:
            st.subheader("📊 Analysis Summary")
            summary = result.get("analysis", {})
            if summary:
                st.json(summary)
            else:
                st.info("ℹ️ No analysis summary available.")

        # ---- DEBUG (OPTIONAL) ----
        with st.expander("🔍 Raw Backend Response (Debug)"):
            st.json(result)

# -----------------------------
# Chat Section
# -----------------------------
if st.session_state.session_id:
    st.subheader("💬 Ask Questions About This Code")

    user_input = st.chat_input("Ask about control flow, variables, logic...")

    if user_input:
        # 1️⃣ Store user message
        st.session_state.chat_history.append(("user", user_input))

        # 2️⃣ Call backend chat
        try:
            res = requests.post(
                BACKEND_CHAT_URL,
                json={
                    "session_id": st.session_state.session_id,
                    "user_message": user_input
                }
            )

            if res.status_code == 200:
                reply = res.json().get("reply", "")
            else:
                reply = "❌ Failed to get response from backend."

        except Exception:
            reply = "❌ Backend connection error."

        # 3️⃣ Store assistant reply
        st.session_state.chat_history.append(("assistant", reply))

        # 🔄 Refresh UI
        st.rerun()

    # 4️⃣ Render chat history
    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(msg)
