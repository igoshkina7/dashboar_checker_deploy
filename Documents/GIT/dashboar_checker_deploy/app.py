import streamlit as st
from auth import login_and_save_auth
from checker import run_checks
from settings import *
import os
os.system("playwright install chromium")

st.title("📊 Dashboard Checker")

if "log" not in st.session_state:
    st.session_state["log"]=""

    try:
            st.session_state["log"] += "⏳ RUN CHECKS\n"
    
            from checker import run_checks
            results = run_checks()
    
            st.session_state["log"] += "✅ DONE\n"

    except Exception as e:
        st.session_state["log"] += f"❌ ERROR: {e}\n"

def ensure_auth():

    # всегда создаём новую сессию
    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)

    ok = login_and_save_auth()

    if not ok:
        raise Exception("LOGIN FAILED")

    return True

if st.button("🔍 Запустить проверку"):
    try:
        ensure_auth()
        st.info("⏳ Проверка дашбордов...")
        results = run_checks()
        text = ""
        for r in results:
            text += f"{r.name}\n"
            text += "✅ OK\n" if r.success else f"❌ {r.message}\n"
            text += "\n"
        st.success("Готово")
        st.text(text)
    except Exception as e:
        st.error(f"❌ Ошибка: {e}")
