# -*- coding: utf8 -*-
from unittest import main, TestCase
import gzip
import tempfile

import unicodecsv

from spectrify.utils.s3 import S3GZipCSVReader


class FakeS3Config(object):
    def __init__(self, fileobj):
        self.fileobj = fileobj

    def fs_open(self, *args, **kwargs):
        self.fileobj.seek(0)
        return self.fileobj


class TestUtilsS3CSVReader(TestCase):
    def test_s3_gzip_csv_reader(self):
        encoded_csv_lines = [
            ['name', 'age', 'sex'],
            ['Nir', '31', 'M'],
            ['ניר', '31', 'M'],
            ["Martin von Löwis", '31', 'M'],
            ["Marc André Lemburg", '31', 'M'],
            ["François Pinard", '31', 'M']
        ]
        gzip_csv = tempfile.TemporaryFile()
        with gzip.GzipFile(fileobj=gzip_csv, mode="wb") as _gzip:
            w = unicodecsv.writer(_gzip, encoding="utf-8")
            w.writerows(encoded_csv_lines)

        fake_s3_config = FakeS3Config(gzip_csv)
        with S3GZipCSVReader(fake_s3_config, "") as s3_gzip_csv_reader:
            self.assertEqual(encoded_csv_lines, list(s3_gzip_csv_reader))


if __name__ == "__main__":
    main()
