import tempfile
import unittest
from pathlib import Path
from main import Store

class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / "test.db")
    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()
    def test_chat_round_trip(self):
        cid = self.store.create_chat("Test")
        self.store.add_message(cid, "user", "Hello")
        self.store.add_message(cid, "assistant", "Hi")
        self.assertEqual(self.store.messages(cid), [("user", "Hello"), ("assistant", "Hi")])
    def test_delete_removes_messages(self):
        cid = self.store.create_chat("Delete me")
        self.store.add_message(cid, "user", "Temporary")
        self.store.delete(cid)
        self.assertEqual(self.store.chats(), [])
        self.assertEqual(self.store.messages(cid), [])
    def test_settings_round_trip(self):
        self.assertEqual(self.store.get("model", "default"), "default")
        self.store.set("model", "qwen2.5:3b")
        self.assertEqual(self.store.get("model", "default"), "qwen2.5:3b")
if __name__ == "__main__": unittest.main()
