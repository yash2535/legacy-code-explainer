import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="Legacy Code Explainer", layout="wide")

if "result" not in st.session_state:
    st.session_state.result = None

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
                "engine": "regex"   # 🔒 FORCE REGEX (ANTLR REMOVED)
            }

            try:
                response = requests.post(BACKEND_URL, json=payload)

                if response.status_code == 200:
                    st.session_state.result = response.json()
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

    st.success("Analysis Complete!")

    show_technical = st.checkbox("Show technical details (IR & Analysis)")

    st.subheader("📝 Explanation")
    st.write(result.get("explanation", ""))

    if show_technical:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📦 Intermediate Representation (IR)")
            st.json(result.get("intermediate_representation", {}))

        with col2:
            st.subheader("📊 Analysis Summary")
            st.json(result.get("analysis", {}))