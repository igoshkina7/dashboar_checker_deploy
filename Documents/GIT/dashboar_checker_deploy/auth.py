import streamlit as st
from playwright.sync_api import sync_playwright
from settings import AUTH_FILE, HEADLESS



def login_and_save_auth():
    try:
        # берём секреты напрямую из Streamlit
        BASE_URL = st.secrets["BASE_URL"]
        USERNAME = st.secrets["USERNAME"]
        PASSWORD = st.secrets["PASSWORD"]

        print("=== DEBUG SECRETS ===")
        print("BASE_URL:", BASE_URL)
        print("USERNAME", USERNAME)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS)
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()

            page.goto(f"{BASE_URL}/auth")

            page.fill("input[type='text']", USERNAME)
            page.fill("input[type='password']", PASSWORD)

            page.click("button:has-text('Войти')")

            # ждём выхода из логина
            page.wait_for_url(lambda url: "/auth" not in url, timeout=30000)

            print("CURRENT_URL", page.url)

            context.storage_state(path=AUTH_FILE)

            print("✅ AUTH SAVED")

            browser.close()
            return True

    except Exception as e:
        print(f"LOGIN ERROR: {e}")
        return False
