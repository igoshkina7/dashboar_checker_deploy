from playwright.sync_api import sync_playwright, expect
from settings import *
from pages import PAGES
import os

# ==========================
# РЕЗУЛЬТАТ ОДНОЙ СТРАНИЦЫ
# ==========================

class Result:
    def __init__(self, name, success, message=""):
        self.name = name
        self.success = success
        self.message = message


# ==========================
# ПРОВЕРКА ОДНОЙ СТРАНИЦЫ
# ==========================

def check_page(page, name, path):

    url = BASE_URL + path

    print(f"\n🔍 {name}")
    print(f"🌐 {url}")

    # 1. открываем страницу
    page.goto(url, wait_until="domcontentloaded")

    if "/auth" in page.url:
        return Result(name, False, "Редирект на авторизацию")

    # 2. ждём базовый UI
    page.wait_for_selector(
        ".gridview__charts-gridster-item",
        timeout=30000
    )

    print("✅ Dashboard loaded")

    # ==========================
    # 🔥 ВОТ СЮДА ВСТАВЛЯЕМ ЛОГИКУ ОШИБОК
    # ==========================

    error_locator = page.locator(".chart-wrapper__error-wrap")

    try:
        # ждём появление ошибки (если она появится)
        error_locator.first.wait_for(timeout=12000)
        

        print("❌ ERROR FOUND")

        try:
            # Находим родительский контейнер чарта
            parent = error_locator.first.locator("xpath=ancestor::*[contains(@class, 'chart-wrapper') or contains(@class, 'gridster-item')]").first
            # Ищем заголовок внутри родителя
            title_elem = parent.locator(".chart-header__headbar-title-text").first
            chart_title = title_elem.inner_text().strip()
        except Exception:
            chart_title = "Неизвестный чарт"

        return Result(name, False, f"Ошибка на чарте: {chart_title}")

    except:
        # если за 5 сек не появилась — значит OK
        print("✅ NO ERRORS")

        return Result(name, True, "OK")


# ==========================
# RUN ALL CHECKS
# ==========================

def run_checks():

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=HEADLESS,
            args=["--ignore-certificate-errors"]
        )

        if not os.path.exists(AUTH_FILE):
            raise Exception("AUTH_FILE not found. Run login first.")

        context = browser.new_context(
            storage_state=AUTH_FILE,
            ignore_https_errors=True
        )

        for name, path in PAGES.items():

            page = context.new_page()

            result = check_page(page, name, path)

            results.append(result)

            page.close()

        browser.close()

    return results


# ==========================
# PRINT RESULTS
# ==========================

def print_results(results):

    print("\n📊 RESULTS:\n")

    failed = 0

    for r in results:
        if r.success:
            print(f"✅ {r.name}")
        else:
            print(f"❌ {r.name} — {r.message}")
            failed += 1

    print("\n====================")

    if failed == 0:
        print("🎉 ALL OK")
    else:
        print(f"⚠️ FAILED: {failed}")

if __name__ == "__main__":

    print("🔥 RUNNING checker.py DIRECTLY")

    results = run_checks()

    print_results(results)
