"""d2txt 的 round-trip 保证是整套工具的地基，必须逐条钉死。"""

import unittest

from tools import d2txt


class TestRoundTrip(unittest.TestCase):
    def check(self, data: bytes):
        self.assertEqual(d2txt.TxtFile.loads(data).dumps(), data)

    def test_crlf(self):
        self.check(b"a\tb\r\n1\t2\r\n")

    def test_lf(self):
        self.check(b"a\tb\n1\t2\n")

    def test_no_trailing_newline(self):
        self.check(b"a\tb\r\n1\t2")

    def test_short_rows_preserved(self):
        # 行尾缺列是 D2 的正常现象，不能补齐
        self.check(b"a\tb\tc\r\n1\t2\r\n3\r\n")

    def test_trailing_empty_cells(self):
        self.check(b"a\tb\tc\r\n1\t\t\r\n")

    def test_blank_line_at_end(self):
        self.check(b"a\tb\r\n1\t2\r\n\r\n")

    def test_high_bytes(self):
        # latin-1 保证 bytes<->str 一一映射，非 ASCII 字节不能丢也不能被当换行
        self.check(b"a\tb\r\n\xff\x80\t\x85\r\n")

    def test_empty(self):
        self.check(b"")

    def test_only_newline(self):
        self.check(b"\r\n")

    def test_duplicate_headers(self):
        tf = d2txt.TxtFile.loads(b"x\tx\r\n1\t2\r\n")
        self.assertEqual(tf.header, ["x", "x"])
        self.assertEqual(tf.dumps(), b"x\tx\r\n1\t2\r\n")


class TestAccess(unittest.TestCase):
    def setUp(self):
        self.tf = d2txt.TxtFile.loads(b"Id\tResFi(H)\tDesc\r\nskeleton1\t110\thi\r\nzombie\t0\t\r\n")

    def test_find_case_insensitive(self):
        self.assertEqual(self.tf.find("resfi(h)"), 1)

    def test_need_raises(self):
        with self.assertRaises(d2txt.MissingColumn):
            self.tf.need("nope")

    def test_get_past_end_is_empty(self):
        self.assertEqual(self.tf.get(self.tf.rows[1], 9), "")

    def test_put_pads(self):
        row = ["a"]
        self.tf.put(row, 2, "z")
        self.assertEqual(row, ["a", "", "z"])

    def test_cell(self):
        self.assertEqual(self.tf.cell(0, "Id"), "skeleton1")


class TestAppend(unittest.TestCase):
    def test_append_keeps_trailing_newline(self):
        tf = d2txt.TxtFile.loads(b"a\tb\r\n1\t2\r\n")
        tf.append(["3", "4"])
        self.assertEqual(tf.dumps(), b"a\tb\r\n1\t2\r\n3\t4\r\n")

    def test_append_without_trailing_newline(self):
        tf = d2txt.TxtFile.loads(b"a\tb\r\n1\t2")
        tf.append(["3", "4"])
        self.assertEqual(tf.dumps(), b"a\tb\r\n1\t2\r\n3\t4")


class TestNumbers(unittest.TestCase):
    def test_to_number(self):
        self.assertEqual(d2txt.to_number("12"), 12)
        self.assertEqual(d2txt.to_number("-3"), -3)
        self.assertEqual(d2txt.to_number("1.5"), 1.5)
        self.assertIsNone(d2txt.to_number(""))
        self.assertIsNone(d2txt.to_number("-"))
        self.assertIsNone(d2txt.to_number("abc"))

    def test_format_number(self):
        self.assertEqual(d2txt.format_number(12), "12")
        self.assertEqual(d2txt.format_number(12.0), "12")
        self.assertEqual(d2txt.format_number(1.5), "1.5")
        self.assertEqual(d2txt.format_number(0.1 * 3), "0.3")


if __name__ == "__main__":
    unittest.main()
