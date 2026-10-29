import asyncio
import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123:test")
os.environ.setdefault("DRIVER_GROUP_1", "-101")
os.environ.setdefault("BRAND_GROUP", "-102")

from bot import regions
from bot.handlers import start
from bot.route_settings import FARGONA_KEYS, destination, save_settings


class FargonaTests(unittest.TestCase):
    def test_choice_order_and_isolated_routes(self):
        self.assertEqual(list(regions.REGION_NAMES), ["tashkent", "fargona", "namangan"])
        labels = [row[0].text for row in start._region_choices("nonce").inline_keyboard]
        self.assertEqual(labels, list(regions.REGION_NAMES.values()))
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {"PERSIST_DIR": folder}, clear=False):
            self.assertEqual(regions.driver_groups("fargona"), [])
            self.assertEqual(regions.application_group("fargona", "brand"), "")
            self.assertEqual(regions.archive_group("fargona"), "")
            save_settings({key: f"-{200 + i}" for i, key in enumerate(FARGONA_KEYS.values())})
            self.assertEqual(regions.driver_groups("fargona"), ["-200", "-201"])
            self.assertEqual(regions.application_group("fargona", "brand"), "-202")
            self.assertEqual(regions.archive_group("fargona"), "-203")
            self.assertEqual(destination("TASHKENT_DRIVER_GROUP_1"), os.environ.get("TASHKENT_DRIVER_GROUP_1", ""))

    def test_contact_without_invented_office(self):
        message = SimpleNamespace(reply_text=AsyncMock(), reply_photo=AsyncMock())
        update = SimpleNamespace(effective_chat=SimpleNamespace(type="private"), effective_message=message)
        context = SimpleNamespace(user_data={"region": "fargona"})
        asyncio.run(start.show_contact(update, context))
        message.reply_text.assert_awaited_once()
        message.reply_photo.assert_not_awaited()
        self.assertIn("hali kiritilmagan", message.reply_text.call_args.args[0])
