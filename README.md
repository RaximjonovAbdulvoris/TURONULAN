# TURON TAXI bot

Namangan va Toshkent uchun alohida Telegram guruhlari bilan ishlaydigan sodda ariza boti.

- Haydovchi arizasi: hujjat rasmlari va operatorga xabar.
- Brend arizasi: oddiy matn, avtomatik Google Sheets yozuvi yo‘q.
- Operator: **Tayyor**, **Izoh berish**, **Jarayonda**; Tayyor arxiv guruhiga ko‘chiradi.
- Spectre, kanalga a’zolik talabi, ofis manzili va qo‘shimcha ko‘chirish navbatlari yo‘q.

## Ishga tushirish

Python 3.12 bilan `pip install -r requirements.txt` qiling. `.env.example` faylidan `.env` nusxa oling va yangi bot tokenini hamda hududlar uchun aloqa matnlarini faqat serverda kiriting. `.env` GitHubga yuborilmaydi.

```bash
mkdir -p runtime
set -a
source .env
set +a
python -m bot.configure check --scope all
python -m bot.main
```

Guruh IDlari `.env.example` ichida kiritilgan. Botni sakkizala guruhga qo‘shib, arxiv guruhlarida o‘chirish huquqini bering. Namangan va Toshkentdan bir martadan test arizasi yuborib oqimni tekshiring. Ishlab turgan boshqa botning tokeni yoki arizalar bazasini bu loyihaga ko‘chirmang.

Batafsil: [TURON_SETUP.md](TURON_SETUP.md).
