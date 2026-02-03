import telebot
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot("8416864662:AAG5uvlkoRC1kw1CcI9F8OhKh6E6WKqjCAY")
ADMINS = [5899789755]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Бот работает 24/7! Добавь меня в чат админом.")

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "🏓 Понг! Бот жив и работает.")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    help_text = """
    📋 Команды:
    /start - проверка работы
    /ping - проверка 24/7
    /verify - ответь на сообщение пользователя для проверки подписки
    /check - проверить подписку пользователя
    """
    bot.reply_to(message, help_text)

@bot.message_handler(content_types=['new_chat_members'])
def check_subscription(message):
    for user in message.new_chat_members:
        logger.info(f"Новый пользователь: {user.id} - {user.first_name}")
        
        if user.id == bot.get_me().id:
            continue
            
        if user.id in ADMINS:
            continue
            
        try:
            logger.info(f"Проверяю подписку {user.id} на канал...")
            status = bot.get_chat_member("@kf_haron_info", user.id).status
            logger.info(f"Статус: {status}")
            
            if status in ['member', 'administrator', 'creator']:
                logger.info(f"Пользователь {user.id} подписан, разблокирую...")
                bot.restrict_chat_member(
                    message.chat.id, 
                    user.id,
                    permissions=telebot.types.ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_polls=True,
                        can_send_other_messages=True,
                        can_add_web_page_previews=True,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False
                    )
                )
                bot.send_message(message.chat.id, f"✅ {user.first_name} получил доступ к чату!")
                logger.info(f"Доступ выдан для {user.id}")
            else:
                logger.info(f"Пользователь {user.id} НЕ подписан, блокирую...")
                bot.restrict_chat_member(
                    message.chat.id,
                    user.id,
                    until_date=int(time.time()) + 86400,
                    permissions=telebot.types.ChatPermissions(
                        can_send_messages=False,
                        can_send_media_messages=False,
                        can_send_polls=False,
                        can_send_other_messages=False,
                        can_add_web_page_previews=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False
                    )
                )
                
                markup = telebot.types.InlineKeyboardMarkup()
                btn = telebot.types.InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/kf_haron_info")
                markup.add(btn)
                
                bot.send_message(
                    message.chat.id,
                    f"❌ {user.first_name}, доступ закрыт!\n\nПодпишись на канал @kf_haron_info чтобы писать в чат.",
                    reply_markup=markup
                )
                logger.info(f"Заблокирован {user.id}")
                
        except Exception as e:
            logger.error(f"Ошибка для {user.id}: {e}")
            bot.send_message(message.chat.id, f"⚠️ Ошибка проверки для {user.first_name}")

@bot.message_handler(commands=['verify'])
def verify_user(message):
    """Принудительная проверка и разблокировка"""
    if not message.reply_to_message:
        bot.reply_to(message, "Ответь этой командой на сообщение пользователя!")
        return
    
    user = message.reply_to_message.from_user
    try:
        status = bot.get_chat_member("@kf_haron_info", user.id).status
        
        if status in ['member', 'administrator', 'creator']:
            bot.restrict_chat_member(
                message.chat.id, 
                user.id,
                permissions=telebot.types.ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False
                )
            )
            bot.reply_to(message, f"✅ {user.first_name} разблокирован!")
        else:
            bot.reply_to(message, f"❌ {user.first_name} всё ещё не подписан на канал!")
            
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка: {e}")

@bot.message_handler(commands=['check'])
def manual_check(message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        try:
            status = bot.get_chat_member("@kf_haron_info", user.id).status
            if status in ['member', 'administrator', 'creator']:
                bot.reply_to(message, f"✅ {user.first_name} подписан на канал")
            else:
                bot.reply_to(message, f"❌ {user.first_name} НЕ подписан")
        except:
            bot.reply_to(message, "Ошибка проверки")

logger.info("🚀 Бот запущен и готов к работе!")
print("✅ Бот работает 24/7...")

while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        logger.error(f"Ошибка polling: {e}")
        time.sleep(5)
