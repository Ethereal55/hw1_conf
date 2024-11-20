import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from hw1_tar import emu, path, root, input_area, output_area


class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом"""
        global path
        path.clear()
        input_area.delete("1.0", tk.END)
        output_area.delete("1.0", tk.END)
        input_area.insert("1.0", "$ ")

    def get_output(self):
        """Получить содержимое текстового поля вывода"""
        return output_area.get("1.0", tk.END).strip()

    @patch("tarfile.open")
    def test_ls_command(self, mock_tarfile_open):
        """Тест команды ls"""
        mock_tar = MagicMock()
        mock_tar.getmembers.return_value = [
            MagicMock(name="folder/"),
            MagicMock(name="folder/3.txt"),
            MagicMock(name="1.docx"),
            MagicMock(name="sdffdsd.txt"),
        ]
        mock_tarfile_open.return_value = mock_tar

        input_area.insert("1.0", "$ ls")
        emu()
        output = self.get_output()

        self.assertIn("C:/Users/END-PC/archive.tar/:", output)
        self.assertIn("folder", output)
        self.assertIn("1.docx", output)
        self.assertIn("sdffdsd.txt", output)

    @patch("tarfile.open")
    def test_cd_command(self, mock_tarfile_open):
        """Тест команды cd"""
        mock_tar = MagicMock()
        mock_tar.getmembers.return_value = [
            MagicMock(name="folder/"),
            MagicMock(name="folder/3.txt"),
        ]
        mock_tarfile_open.return_value = mock_tar

        input_area.insert("1.0", "$ cd folder")
        emu()
        self.assertEqual(path, ["folder"])

        input_area.insert("1.0", "$ cd ..")
        emu()
        self.assertEqual(path, [])

        input_area.insert("1.0", "$ cd nonexistent")
        emu()
        self.assertIn("cd: nonexistent: No such directory", self.get_output())

    @patch("tarfile.open")
    def test_cat_command(self, mock_tarfile_open):
        """Тест команды cat"""
        mock_tar = MagicMock()
        file_mock = MagicMock()
        file_mock.read.return_value = b"This is a test file"
        mock_tar.getmember.side_effect = lambda name: file_mock if name == "folder/3.txt" else KeyError()
        mock_tar.extractfile.return_value = file_mock
        mock_tarfile_open.return_value = mock_tar

        input_area.insert("1.0", "$ cd folder")
        emu()
        input_area.insert("1.0", "$ cat 3.txt")
        emu()
        self.assertIn("This is a test file", self.get_output())

        input_area.insert("1.0", "$ cat nonexistent.txt")
        emu()
        self.assertIn("cat: nonexistent.txt: No such file", self.get_output())

    @patch("tarfile.open")
    def test_wc_command(self, mock_tarfile_open):
        """Тест команды wc"""
        mock_tar = MagicMock()
        file_mock = MagicMock()
        file_mock.read.return_value = b"Hello world\nAnother line"
        mock_tar.getmember.side_effect = lambda name: file_mock if name == "folder/3.txt" else KeyError()
        mock_tar.extractfile.return_value = file_mock
        mock_tarfile_open.return_value = mock_tar

        input_area.insert("1.0", "$ cd folder")
        emu()
        input_area.insert("1.0", "$ wc 3.txt")
        emu()
        self.assertIn("количество строк: 2", self.get_output())
        self.assertIn("количество слов: 4", self.get_output())
        self.assertIn("количество символов: 25", self.get_output())

    def test_exit_command(self):
        """Тест команды exit"""
        with patch.object(root, "quit") as mock_quit:
            input_area.insert("1.0", "$ exit")
            emu()
            mock_quit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
