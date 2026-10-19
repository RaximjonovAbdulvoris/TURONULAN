from pathlib import Path
from uuid import uuid4

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from bot.regions import NAMANGAN, TASHKENT, REGION_NAMES, clear_application, get_region, region_name

MENU_DRIVER = "📝 Haydovchi arizasi"
MENU_BRAND = "🎨 Brend arizasi"
MENU_CONTACT = "📞 Aloqa uchun"
MENU_REGION = "🔄 Hududni almashtirish"
OFFICE_IMAGES = Path(__file__).resolve().parent.parent / "templates"

CONTACT_POSTS = {
    TASHKENT: (
        "📍 <b>TURON TAXI · TOSHKENT</b>\n\n"
        "📞 <b>Bog‘lanish:</b>\n"
        "+998 95 078 97 99\n+"
        "+998 95 059 97 99\n\n"
        "💬 <b>Telegram:</b> @WBTURONSUPPORT\n"
        "💳 <b>Pul yechish boti:</b> @didox_s_wb_bot\n\n"
        "🗺 <b>Ofis manzili:</b> Yashnobod tumani, Qorasuv ko‘chasi, "
        "Dodo Pizza qarshisida."
    ),
    NAMANGAN: (
        "📍 <b>TURON TAXI · NAMANGAN</b>\n\n"
        "📞 <b>Bog‘lanish:</b>\n"
        "+998 95 078 97 99\n"
        "+998 95 059 97 99\n\n"
        "💬 <b>Telegram:</b> @WBTURONNAMANGAN\n"
        "💳 <b>Pul yechish boti:</b> @didox_s_wb_bot\n\n"
        "📍 <b>Bosh ofis:</b> 6-mikrorayon, IIB ro‘parasida.\n"
        "📍 <b>2-ofis:</b> Lola ko‘chasi, Boburshoh ko‘chasi, "
        "11-maktab ro‘parasida."
    ),
}

CONTACT_MAPS = {
    TASHKENT: InlineKeyboardMarkup([[
        InlineKeyboardButton("🗺 Xaritada ochish", url="https://yandex.uz/maps/-/CXF9VLP6"),
    ]]),
    NAMANGAN: InlineKeyboardMarkup([[
        InlineKeyboardButton("📍 Bosh ofis", url="https://yandex.uz/maps/-/CXF9bYPx"),
        InlineKeyboardButton("📍 2-ofis", url="https://yandex.uz/maps/-/CXF9fQ0S"),
    ]]),
}


def main_keyboard(region: str) -> ReplyKeyboardMarkup:
    rows = [[MENU_DRIVER], [MENU_BRAND], [MENU_CONTACT], [MENU_REGION]]
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


# Compatibility for imports outside the regional flows.
MAIN_KEYBOARD = main_keyboard(NAMANGAN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.effective_chat.type != "private":
        return ConversationHandler.END
    context.user_data.clear()
    if update.effective_user:
        context.bot_data.get("pending_user_replies", {}).pop(update.effective_user.id, None)
    nonce = uuid4().hex[:10]
    context.user_data["region_choice_nonce"] = nonce
    await update.effective_message.reply_text(
        "🚕 <b>TURON TAXI</b>ga xush kelibsiz!\n\n"
        "Haydovchilik yoki avtomobilni brendlash uchun ariza qoldirishingiz mumkin.\n\n"
        "Avval ishlamoqchi bo‘lgan hududingizni tanlang.",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )
    await update.effective_message.reply_text(
        "Qaysi hududda ishlamoqchisiz?",
        reply_markup=_region_choices(nonce),
    )
    return ConversationHandler.END


def _region_choices(nonce: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(name, callback_data=f"region:pick:{region}:{nonce}")]
        for region, name in REGION_NAMES.items()
    ])


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    region = get_region(context)
    if not region:
        return await start(update, context)
    details = (
        "📝 <b>Haydovchi arizasi</b> — parkka ulanish uchun.\n"
        "🎨 <b>Brend arizasi</b> — avtomobilni brendlash uchun.\n"
        "📞 <b>Aloqa uchun</b> — bog‘lanish ma’lumotlari."
    )
    await update.effective_message.reply_text(
        f"📍 <b>{region_name(region)}</b>\n\n"
        "Arizangiz tanlangan shahardagi operatorlarga yuboriladi.\n\n"
        f"{details}\n\nKerakli bo‘limni tanlang:",
        parse_mode="HTML", reply_markup=main_keyboard(region),
    )
    return ConversationHandler.END


async def on_region_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if not query or update.effective_chat.type != "private":
        return ConversationHandler.END
    parts = (query.data or "").split(":")
    if (len(parts) != 4 or parts[2] not in REGION_NAMES
            or parts[3] != context.user_data.get("region_choice_nonce")):
        await query.answer("Bu tanlov eskirgan. Hududni almashtirish uchun /start bosing.", show_alert=True)
        return ConversationHandler.END
    _, action, region, nonce = parts
    if action == "pick":
        context.user_data["pending_region"] = region
        await query.answer()
        await query.edit_message_text(
            f"📍 <b>{region_name(region)}</b>\n\n"
            f"Siz <b>{region_name(region)}</b> uchun ariza yubormoqchisiz.\n"
            "Arizangiz faqat shu shahardagi operatorlarga boradi.\n\n"
            "Tanlovingizni tasdiqlaysizmi?",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"region:confirm:{region}:{nonce}")],
                [InlineKeyboardButton("⬅️ Ortga", callback_data=f"region:back:{region}:{nonce}")],
            ]),
        )
    elif action == "back":
        context.user_data.pop("pending_region", None)
        await query.answer()
        await query.edit_message_text(
            "Qaysi hududda ishlamoqchisiz?", reply_markup=_region_choices(nonce),
        )
    elif action == "confirm" and context.user_data.get("pending_region") == region:
        context.user_data.clear()
        context.user_data["region"] = region
        await query.answer()
        await query.edit_message_text(f"✅ Tanlandi: {region_name(region)}")
        await show_menu(update, context)
    else:
        await query.answer("Avval hududni qayta tanlang.", show_alert=True)
    return ConversationHandler.END


def build_region_handler() -> CallbackQueryHandler:
    return CallbackQueryHandler(on_region_choice, pattern=r"^region:")


async def require_region(update: Update, context: ContextTypes.DEFAULT_TYPE, allowed_regions=None) -> bool:
    if not update.effective_chat or update.effective_chat.type != "private":
        return False
    region = get_region(context)
    if not region:
        if update.callback_query:
            await update.callback_query.answer()
        await start(update, context)
        return False
    if allowed_regions is not None and region not in allowed_regions:
        await update.effective_message.reply_text(
            "Bu bo‘lim tanlangan shaharda mavjud emas. Quyidagi menyudan tanlang.",
            reply_markup=main_keyboard(region),
        )
        return False
    return True


async def show_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not await require_region(update, context):
        return ConversationHandler.END
    clear_application(context)
    region = get_region(context)
    image_path = OFFICE_IMAGES / f"office_{region}.png"
    with image_path.open("rb") as photo:
        await update.effective_message.reply_photo(
            photo=photo,
            caption=CONTACT_POSTS[region],
            parse_mode="HTML",
            reply_markup=CONTACT_MAPS[region],
        )
    return ConversationHandler.END


def build_contact_handler() -> MessageHandler:
    return MessageHandler(filters.ChatType.PRIVATE & filters.Regex(r"^(?:📞 Aloqa uchun|Bog['‘]lanish uchun)$"), show_contact)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    clear_application(context)
    if update.effective_user:
        context.bot_data.get("pending_user_replies", {}).pop(update.effective_user.id, None)
    await update.effective_message.reply_text("Ariza to‘ldirish bekor qilindi.")
    return await show_menu(update, context)
