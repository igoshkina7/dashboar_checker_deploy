import streamlit as st
from playwright.sync_api import sync_playwright
from settings import AUTH_FILE, HEADLESS

def login_and_save_auth():
    try:
        BASE_URL = st.secrets["BASE_URL"]
        USERNAME = st.secrets["USERNAME"]
        PASSWORD = st.secrets["PASSWORD"]

        st.write("DEBUG: login_and_save_auth вызвана")
        st.write(f"BASE_URL = {BASE_URL}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS)
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()

            page.goto(f"{BASE_URL}/auth")
            st.write(f"Перешли на {BASE_URL}/auth")

            page.fill("input[type='text']", USERNAME)
            page.fill("input[type='password']", PASSWORD)
            st.write("LOGIN AND PASSWORD DONE")
            
            page.click("button:has-text('Войти')")
            page.wait_for_url(lambda url: "/auth" not in url, timeout=30000)

            st.write(f"CURRENT_URL = {page.url}")   # исправлено: f-строка и page.url
            context.storage_state(path=AUTH_FILE)   # исправлено: должен быть AUTH_FILE, а не page.url
            st.write("✅ AUTH SAVED")

            browser.close()
            return True

    except Exception as e:
        st.write(f"LOGIN ERROR: {e}")   # исправлено
        return False
