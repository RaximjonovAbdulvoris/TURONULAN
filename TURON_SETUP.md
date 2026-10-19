# TURON TAXI — yangi botni sozlash

Bot ikki hudud uchun: Toshkent va Namangan. Har birida haydovchi, Brend va
arxiv guruhlari mustaqil. Haydovchi arizasi operatorga rasm albomi va ma'lumot
xabarini yuboradi. Tugmalar: Tayyor, Izoh berish, Jarayonda. Brend arizasi
guruhga oddiy matn sifatida yuboriladi.

Yangi token va alohida doimiy `PERSIST_DIR` ishlating. Eski HUMO botining
`.env`, `bot_routes.json` yoki `bot_persistence.pkl` fayllarini ko'chirmang.
Telegram guruh IDlari `.env.example` ichida tayyor. Uni serverda `.env`
fayliga nusxalab, yangi tokenni kiriting:

- Namangan: `DRIVER_GROUP_1`, `DRIVER_GROUP_2`, `BRAND_GROUP`, `ARCHIVE_GROUP`.
- Toshkent: `TASHKENT_DRIVER_GROUP_1`, `TASHKENT_DRIVER_GROUP_2`,
  `TASHKENT_BRAND_GROUP`, `TASHKENT_ARCHIVE_GROUP`.

Aloqa bo‘limida har bir hududning ofis rasmi, manzili, telefonlari va xarita
tugmalari ko‘rsatiladi. Ularni yangilash uchun `bot/handlers/start.py` va
`bot/templates/office_<hudud>.png` fayllarini tahrirlang.

`python -m bot.configure check --scope all` bilan Toshkent guruhlari va bot
huquqlarini tekshiring. Namangan guruhlari uchun ham botning administrator va
xabarlarni o'chirish huquqi borligini alohida tekshiring. Har ikkala hududdan
sinov arizasi yuborib, manzil va arxiv oqimini tasdiqlang.
