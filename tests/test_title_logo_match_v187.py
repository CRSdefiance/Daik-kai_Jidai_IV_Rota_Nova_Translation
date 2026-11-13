"""Whole source-gold coverage and mutation detection for opening logo reuse."""

import unittest

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from scripts import title_logo_match_v187 as art


class CompleteLogoTests(unittest.TestCase):
    def test_all_menu_gold_core_pixels_survive_extraction(self):
        menu = PxlImage.from_bytes(art.prior_art.targets()['/_pxl/title/title03.pxl'])
        asset = art.gold_asset()
        core = []
        for y in range(64):
            for x in range(2, 256):
                rgb = menu.palette[menu.indices[(y + 41) * 256 + x - 2]][:3]
                r, g, b = rgb
                if r > g + 6 and g > b + 18 and r > 90:
                    core.append((x, y))
                    self.assertEqual(asset.getpixel((x, y)), rgb + (255,))
        self.assertGreater(len(core), 1000)
        self.assertLess(min(x for x, y in core), 42)  # complete initial R
        self.assertGreater(max(x for x, y in core), 192)  # complete final A
        self.assertEqual(min(y for x, y in core), 10)  # tall N ornament
        self.assertGreater(max(y for x, y in core), 48)  # lower N flourish

    def test_white_border_is_not_part_of_extracted_art(self):
        asset = art.gold_asset()
        for y in range(asset.height):
            for x in range(asset.width):
                r, g, b, a = asset.getpixel((x, y))
                if a:
                    self.assertFalse(min(r, g, b) >= 220 and max(r, g, b) - min(r, g, b) < 12)

    def test_saved_source_batches_pass_preservation(self):
        self.assertTrue(art.check_assets(art.targets())['FLS_records_palette_all_other_movie_bytes_exact'])

    def test_removed_leading_wordmark_pixels_are_rejected(self):
        result = art.targets()
        p = PxlImage.from_bytes(result[art.PXL_PATH])
        for y in range(50, 92):
            p.indices[y * 256 + 40:y * 256 + 60] = bytes([255]) * 20
        result[art.PXL_PATH] = p.to_bytes()
        with self.assertRaisesRegex(AssertionError, 'Complete expected'):
            art.check_assets(result)

    def test_dropped_gold_flourish_is_rejected(self):
        result = art.targets()
        f = FlsArchive(result[art.FLS_PATH])
        t = f.texture(5)
        t.indices[48 * 256:] = bytes(len(t.indices) - 48 * 256)
        result[art.FLS_PATH] = f.to_bytes()
        with self.assertRaisesRegex(AssertionError, 'Complete gold'):
            art.check_assets(result)


if __name__ == '__main__':
    unittest.main()
