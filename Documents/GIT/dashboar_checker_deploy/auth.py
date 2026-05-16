from playwright.sync_api import sync_playwright
from config import *

# ==========================
# СОХРАНЕНИЕ СЕССИИ
# ==========================

def login_and_save_auth():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS)
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()

            print("BASE_URL":", BASE_URL)
            print("USERNAME":", USERNAME)
            print("PASSWORD":", PASSWORD)

            page.goto(f"{BASE_URL}/auth")
            page.fill("input[type='text']", USERNAME)
            page.fill("input[type='password']", PASSWORD)
            page.click("button:has-text('Войти')")
            page.wait_for_load_state("networkidle")

            context.storage_state(path=AUTH_FILE)
            print("✅ AUTH SAVED")
            browser.close()
            return True
    except Exception as e:
        print(f"❌ Ошибка логина: {e}")
        return False
        browser.close()


if __name__ == "__main__":
    login_and_save_auth()
