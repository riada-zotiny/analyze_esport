import unittest
from unittest.mock import patch, MagicMock
import recordMouseKeyboardMovement as rmkm

class TestRecordMouseKeyboardMovement(unittest.TestCase):

    @patch("recordMouseKeyboardMovement.pyautogui.size", return_value=(1920, 1080))
    def test_get_next_filename(self, mock_size):
        # Simule un dossier temporaire
        import tempfile, os
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = rmkm.get_next_filename(base_dir=tmpdir, base_name="testfile")
            self.assertTrue(filename.startswith("testfile_"))
            self.assertTrue(filename.endswith("_num1.json"))
            # Crée un fichier pour tester l'incrémentation
            open(os.path.join(tmpdir, filename), "w").close()
            filename2 = rmkm.get_next_filename(base_dir=tmpdir, base_name="testfile")
            self.assertNotEqual(filename, filename2)

    @patch("recordMouseKeyboardMovement.ctypes.windll.user32.SetCursorPos")
    def test_set_cursor_pos(self, mock_set_cursor):
        rmkm.set_cursor_pos(100, 200)
        mock_set_cursor.assert_called_with(100, 200)

    @patch("recordMouseKeyboardMovement.time.sleep")
    @patch("recordMouseKeyboardMovement.tk.Tk")
    def test_count_down_animation_config(self, mock_tk, mock_sleep):
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        rmkm.count_down_animation_config("record")
        mock_tk.assert_called_once()
        mock_root.withdraw.assert_called_once()

    def test_on_move_action_format(self):
        # Teste la structure d'une action move
        actions = []
        time_diff_container = [0.1]
        screen_width, screen_height = 1920, 1080
        x, y = 100, 200
        def on_move(x, y):
            if 0 <= x < screen_width and 0 <= y < screen_height:
                actions.append({
                    "action": "move",
                    "position": (x, y),
                    "time_diff": time_diff_container[0],
                    "timestamp": "fake"
                })
        on_move(x, y)
        self.assertEqual(actions[0]["action"], "move")
        self.assertEqual(actions[0]["position"], (100, 200))
        self.assertEqual(actions[0]["time_diff"], 0.1)
        self.assertEqual(actions[0]["timestamp"], "fake")
    def test_on_click_action_format(self):
        # Teste la structure d'une action click
        actions = []
        time_diff_container = [0.1]
        screen_width, screen_height = 1920, 1080
        x, y = 100, 200
        def on_click(x, y, button, pressed):
            if 0 <= x < screen_width and 0 <= y < screen_height:
                actions.append({
                    "action": "click",
                    "position": (x, y),
                    "button": button,
                    "pressed": pressed,
                    "time_diff": time_diff_container[0],
                    "timestamp": "fake"
                })
        on_click(x, y, "left", True)
        self.assertEqual(actions[0]["action"], "click")
        self.assertEqual(actions[0]["position"], (100, 200))
        self.assertEqual(actions[0]["button"], "left")
        self.assertTrue(actions[0]["pressed"])
        self.assertEqual(actions[0]["time_diff"], 0.1)
        self.assertEqual(actions[0]["timestamp"], "fake")

    def test_on_type_action_format(self):
        # Teste la structure d'une action type
        actions = []
        time_diff_container = [0.1]
        screen_width, screen_height = 1920, 1080
        x, y = 100, 200
        def on_type(key):
            actions.append({
                "action": "type",
                "key": key,
                "time_diff": time_diff_container[0],
                "timestamp": "fake"
            })
        on_type("a")
        self.assertEqual(actions[0]["action"], "type")
        self.assertEqual(actions[0]["key"], "a")
        self.assertEqual(actions[0]["time_diff"], 0.1)
        self.assertEqual(actions[0]["timestamp"], "fake")    


if __name__ == "__main__":
    unittest.main()