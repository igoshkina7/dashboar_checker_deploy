from checker import run_checks


def run_dashboard_check():

    print("🚀 START CHECK")

    results = run_checks()

    text = "📊 <b>Результаты проверки</b>\n\n"

    for r in results:

        text += f"<b>{r.name}</b>\n"

        if r.success:
            text += "✅ загрузка: OK\n"
        else:
            text += "❌ загрузка: ERROR\n"
            text += f"   {r.message}\n"

        text += "\n"

    return text