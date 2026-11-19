import unittest
from check_ios_minimum import check_minos


class MinimumOSTest(unittest.TestCase):
    def test_ios15(self):
        check_minos(' platform IOS\n minos 15.0\n sdk 27.1\n', 'Runner')

    def test_newer_embedded_slice_rejected(self):
        with self.assertRaises(ValueError):
            check_minos(' minos 14.0\n minos 16.0\n', 'framework')

    def test_missing_command_rejected(self):
        with self.assertRaises(ValueError):
            check_minos(' sdk 27.1\n', 'framework')

    def test_linker_version_is_not_minimum_os(self):
        check_minos(' cmd LC_BUILD_VERSION\n minos 15.0\n tool LD\n version 27037.1\n', 'Runner')

    def test_legacy_minimum(self):
        check_minos(' cmd LC_VERSION_MIN_IPHONEOS\n cmdsize 16\n version 12.1\n sdk 15.0\n', 'FFmpeg')
        with self.assertRaises(ValueError):
            check_minos(' cmd LC_VERSION_MIN_IPHONEOS\n cmdsize 16\n version 16.0\n', 'framework')
