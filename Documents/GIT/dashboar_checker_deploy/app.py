import streamlit as st
from auth import login_and_save_auth
from checker import run_checks
from config import AUTH_FILE
import os

st.title("📊 Dashboard Checker")

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