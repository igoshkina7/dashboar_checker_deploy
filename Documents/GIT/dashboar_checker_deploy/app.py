import streamlit as st
from playwright.sync_api import sync_playwright

AUTH_FILE = "auth.json"
HEADLESS = True


def login_and_save_auth():
    try:
        BASE_URL = st.secrets["BASE_URL"]
        USERNAME = st.secrets["USERNAME"]
        PASSWORD = st.secrets["PASSWORD"]

        print("BASE_URL:", BASE_URL)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS)
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()

            page.goto(f"{BASE_URL}/auth", wait_until="domcontentloaded")

            page.fill("input[type='text']", USERNAME)
            page.fill("input[type='password']", PASSWORD)

            page.click("button:has-text('Войти')")

            # ВАЖНО: НЕ URL WAIT
            page.wait_for_timeout(5000)

            print("CURRENT URL:", page.url)

            # проверяем, что логин реально прошёл
            if "/auth" in page.url:
                page.screenshot(path="login_failed.png")
                raise Exception("Still on auth page")

            context.storage_state(path=AUTH_FILE)

            browser.close()
            return True

    except Exception as e:
        print("❌ LOGIN ERROR:", e)
        return False
