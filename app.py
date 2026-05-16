import streamlit as st
from auth import login_and_save_auth
from checker import run_checks
from settings import *
import os
os.system("playwright install chromium")

st.title("📊 Dashboard Checker")

if "log" not in st.session_state:
    st.session_state["log"]=""
    
def add_log(message: str):
    st.session_state["log"] += message +"\n"
    #st.rerun()
    

def ensure_auth():

    # всегда создаём новую сессию
    if os.path.exists(AUTH_FILE):
        add_log("✅AUTH FILE EXISTS")
        #os.remove(AUTH_FILE)
        return True

    ok = login_and_save_auth()

    if not ok:
        add_log("❌LOGIN FAILED")
        raise Exception("LOGIN FAILED")

    add_log("✅LOGIN SUCCESS")
    return True

if st.button("🔍 Запустить проверку"):
    try:
        add_log("START CHECK")
        ensure_auth()
        st.info("⏳ Проверка дашбордов...")
        add_log("⏳RUN CHECK")
        results = run_checks()
        add_log("RESULTS CHECK")
        text = ""
        for r in results:
            text += f"{r.name}\n"
            if r.success:
                add_log(f"✅{r.name} - OK")
            else: 
                add_log(f"❌{r.name} - {r.message}")
            text += "\n"

        add_log("DONE")
        st.success("Готово")
        st.text(text)
        
    except Exception as e:
        add_log(f"ERROR: {e}")
        st.error(f"❌ Ошибка: {e}")

st.subheader("Лог выполнения")
st.text_area(
    "debug log",
    value = st.session_state["log"],
    height=300
    )
