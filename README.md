# TURON TAXI bot

Toshkent, Farg‘ona va Namangan uchun alohida Telegram guruhlari bilan ishlaydigan sodda ariza boti.

- Haydovchi arizasi: hujjat rasmlari va operatorga xabar.
- Brend arizasi: oddiy matn, avtomatik Google Sheets yozuvi yo‘q.
- Operator: **Tayyor**, **Izoh berish**, **Jarayonda**; Tayyor arxiv guruhiga ko‘chiradi.
- Spectre, kanalga a’zolik talabi, ofis manzili va qo‘shimcha ko‘chirish navbatlari yo‘q.

## Ishga tushirish

Python 3.12 bilan `pip install -r requirements.txt` qiling. `.env.example` faylidan `.env` nusxa oling va yangi bot tokenini faqat serverda kiriting. Aloqa bo‘limi uchun hududga mos ofis rasmi, telefonlar va xarita tugmalari kodda tayyor. `.env` GitHubga yuborilmaydi.

```bash
mkdir -p runtime
set -a
source .env
set +a
python -m bot.configure check --scope all
python -m bot.main
```

Uchala hududning IDlari `.env.example` ichida kiritilgan. Ishlab turgan serverda `.env` fayli saqlanadi: Farg‘ona haydovchi 01/02, brend va arxiv guruhlarini `python -m bot.configure fargona` orqali sozlang, botni guruhlarga administrator qiling va `python -m bot.configure check --scope fargona` bilan tekshiring. Farg‘ona IDlari sozlanmaguncha arizalar boshqa hududga yuborilmaydi. Har bir hududdan alohida test arizasi yuboring. Farg‘ona aloqa ma’lumotlari va ofis rasmi berilmaguncha aloqa bo‘limida faqat tasdiqlangan pul yechish boti ko‘rsatiladi. Ishlab turgan boshqa botning tokeni yoki arizalar bazasini bu loyihaga ko‘chirmang.

Batafsil: [TURON_SETUP.md](TURON_SETUP.md).
