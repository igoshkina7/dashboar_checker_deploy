import asyncio
from config import load_stand_env
from old.pages_2 import get_all_stands, get_stand_config
from old.checker_2 import check_all_pages_for_stand, format_results_for_telegram
from aiogram import Bot

async def main():
    print("🔍 Запуск auto_check.py...\n")
    
    stands = get_all_stands()
    print(f"📋 Доступные стенды: {stands}\n")
    
    if not stands:
        print("❌ Нет стендов в pages.py!")
        return
    
    first_stand = stands[0]
    env_vars = load_stand_env(first_stand)
    
    bot = Bot(token=env_vars["TG_BOT_TOKEN"])
    all_results = {}
    
    for stand_name in get_all_stands():
        print(f"\n{'='*50}")
        print(f"🚀 Проверка стенда: {stand_name.upper()}")
        print(f"{'='*50}\n")
        
        try:
            env_vars = load_stand_env(stand_name)
            stand_config = get_stand_config(stand_name)
            
            # ✅ ИСПРАВЛЕНО: Запускаем синхронные функции в отдельном потоке
            print("🔐 + 🔍 Авторизация и проверка страниц...")
            results = await asyncio.to_thread(check_all_pages_for_stand, stand_config, env_vars, True)
            all_results[env_vars["STAND_NAME"]] = results
            
            print(f"✅ Стенд {stand_name.upper()} проверен\n")
            
        except Exception as e:
            print(f"❌ Ошибка проверки стенда {stand_name}: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
    
    # Отправка отчета в Telegram
    print("📤 Отправляем отчет...")
    text = format_results_for_telegram(all_results)
    
    for user_id in env_vars["TG_ALLOWED_USERS"]:
        try:
            await bot.send_message(user_id, text, parse_mode="HTML")
            print(f"✅ Отправлено пользователю {user_id}")
        except Exception as e:
            print(f"❌ Ошибка отправки {user_id}: {e}")
    
    await bot.session.close()
    print("\n✅ Готово!")

if __name__ == "__main__":
    asyncio.run(main())