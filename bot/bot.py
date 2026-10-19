import telebot

# 1. Tu Token de @BotFather
TOKEN = "8600067491:AAGYxxFeWLHs4t7vNGjYvfxOBmUMvZKe-wc"

# 2. Tu ID de canal configurado
CANAL_ID = -1004466695655 

# 3. Palabra clave requerida
PALABRA_CLAVE = "LOLIKAWAI"

# Límite máximo de personas
LIMITE_CUPOS = 20

bot = telebot.TeleBot(TOKEN)

# Variables para controlar el enlace único y el contador
enlace_unico = None
contador_usos = 0
usuarios_registrados = set()  # Para evitar que el mismo usuario gaste varios cupos

@bot.message_handler(commands=['start'])
def inicio(message):
    bot.reply_to(
        message, 
        "👋 ¡Hola! Escribe la palabra clave para recibir el enlace de acceso al canal."
    )

@bot.message_handler(func=lambda message: True)
def verificar_palabra(message):
    global enlace_unico, contador_usos
    texto = message.text.strip().upper()
    user_id = message.from_user.id

    if texto == PALABRA_CLAVE:
        # Verificar si ya se agotaron los cupos
        if contador_usos >= LIMITE_CUPOS:
            bot.reply_to(
                message, 
                "🚫 **¡Lo sentimos! Los 20 cupos disponibles para esta promoción ya se han agotado.**"
            )
            return

        try:
            # Crear el enlace por única vez
            if enlace_unico is None:
                nuevo_link = bot.create_chat_invite_link(
                    chat_id=CANAL_ID,
                    member_limit=LIMITE_CUPOS
                )
                enlace_unico = nuevo_link.invite_link

            # Incrementar el contador solo si es la primera vez que este usuario pide el link
            if user_id not in usuarios_registrados:
                usuarios_registrados.add(user_id)
                contador_usos += 1

            cupos_restantes = LIMITE_CUPOS - contador_usos

            bot.reply_to(
                message, 
                f"✅ ¡Palabra clave correcta!\n\n"
                f"Aquí tienes el enlace de acceso exclusivo:\n"
                f"{enlace_unico}\n\n"
                f"⏳ Cupos entregados: {contador_usos} de {LIMITE_CUPOS} "
                f"(Quedan {cupos_restantes} disponibles)"
            )

        except Exception as e:
            bot.reply_to(
                message, 
                f"⚠️ Error de Telegram: {e}"
            )
    else:
        bot.reply_to(message, "❌ Palabra clave incorrecta.")

print("Bot iniciado correctamente...")
bot.infinity_polling()