import asyncio
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123:test")
os.environ.setdefault("DRIVER_GROUP_1", "-101")
os.environ.setdefault("DRIVER_GROUP_2", "-102")
os.environ.setdefault("BRAND_GROUP", "-103")

from bot.handlers.start import CONTACT_MAPS, CONTACT_POSTS, OFFICE_IMAGES, show_contact
from bot.regions import NAMANGAN, TASHKENT


class ContactPostTests(unittest.TestCase):
    def test_each_region_has_its_own_image_and_map(self):
        for region in (TASHKENT, NAMANGAN):
            with self.subTest(region=region):
                self.assertTrue((OFFICE_IMAGES / f"office_{region}.png").is_file())
                self.assertIn("@didox_s_wb_bot", CONTACT_POSTS[region])
        self.assertIn("@WBTURONSUPPORT", CONTACT_POSTS[TASHKENT])
        self.assertIn("@WBTURONNAMANGAN", CONTACT_POSTS[NAMANGAN])
        self.assertEqual(len(CONTACT_MAPS[NAMANGAN].inline_keyboard[0]), 2)
        self.assertEqual(len(CONTACT_MAPS[TASHKENT].inline_keyboard[0]), 1)

    def test_contact_sends_photo_caption_and_map_in_one_message(self):
        async def check(region):
            message = SimpleNamespace(reply_photo=AsyncMock())
            update = SimpleNamespace(effective_chat=SimpleNamespace(type="private"),
                                     effective_message=message)
            context = SimpleNamespace(user_data={"region": region})
            await show_contact(update, context)
            message.reply_photo.assert_awaited_once()
            data = message.reply_photo.call_args.kwargs
            self.assertEqual(data["caption"], CONTACT_POSTS[region])
            self.assertIs(data["reply_markup"], CONTACT_MAPS[region])
            self.assertEqual(Path(data["photo"].name).name, f"office_{region}.png")
        asyncio.run(check(TASHKENT))
        asyncio.run(check(NAMANGAN))
