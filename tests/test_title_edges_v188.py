"""Source coverage, scene contamination and smooth native-edge regressions."""

import unittest

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from scripts import title_edges_v188 as art


class SoftTitleEdgeTests(unittest.TestCase):
    def test_background_speckles_are_transparent(self):
        gold = art.gold_asset()
        for xy in ((137, 55), (137, 56), (139, 55), (141, 54), (138, 56), (134, 57)):
            self.assertEqual(gold.getpixel(xy)[3], 0, xy)

    def test_gold_has_soft_edges(self):
        gold = art.gold_asset()
        fractional = sum(0 < gold.getpixel((x, y))[3] < 255 for y in range(64) for x in range(256))
        self.assertGreater(fractional, 500)

    def test_all_menu_gold_core_pixels_survive(self):
        menu, _bg, _lat, _water = art.matte.assets()
        gold = art.gold_asset()
        points = []
        for y in range(64):
            for x in range(2, 256):
                rgb = menu.palette[menu.indices[(y + 41) * 256 + x - 2]][:3]
                r, g, b = rgb
                if r > g + 6 and g > b + 18 and r > 90:
                    points.append((x, y))
                    self.assertEqual(gold.getpixel((x, y)), rgb + (255,))
        self.assertEqual(len(points), 1221)
        self.assertEqual((min(x for x, y in points), max(x for x, y in points)), (38, 199))
        self.assertEqual((min(y for x, y in points), max(y for x, y in points)), (10, 57))

    def test_blue_faces_use_approved_menu_raster(self):
        menu = art.matte.assets()[0]
        source, _ = art.prior_art.wordmark()
        blue = art.menu_wordmark()
        for y in range(source.height):
            for x in range(source.width):
                if source.getpixel((x, y))[3] >= 96:
                    rgb = menu.palette[menu.indices[(y + 8) * 256 + x + 40]][:3]
                    self.assertEqual(blue.getpixel((x, y)), rgb + (255,))

    def test_native_partial_blue_edges_are_lighter_than_black_matte(self):
        base, _ = art.prior_art.sources()
        palette = PxlImage.from_bytes(base.read_file(art.PXL_PATH)).palette
        word = art.menu_wordmark()
        new = art.project_wordmark(palette, 248, 49)
        brighter = 0
        for y in range(word.height):
            for x in range(word.width):
                r, g, b, alpha = word.getpixel((x, y))
                if 8 <= alpha < 96:
                    old_rgb = tuple(round(c * alpha / 255) for c in (r, g, b))
                    old = palette[art.nearest(palette, old_rgb)][:3]
                    current = palette[new[y * 248 + x + 36]][:3]
                    brighter += sum(current) > sum(old)
        self.assertGreater(brighter, 200)

    def test_saved_native_assets_preserve_movie_and_metadata(self):
        self.assertTrue(art.check_assets(art.targets())['FLS_records_palette_all_other_movie_bytes_exact'])

    def test_clipped_leading_blue_letters_are_rejected(self):
        result = art.targets()
        pxl = PxlImage.from_bytes(result[art.PXL_PATH])
        for y in range(50, 92):
            pxl.indices[y * 256 + 40:y * 256 + 60] = bytes([255]) * 20
        result[art.PXL_PATH] = pxl.to_bytes()
        with self.assertRaisesRegex(AssertionError, 'Complete expected'):
            art.check_assets(result)

    def test_clipped_gold_flourish_is_rejected(self):
        result = art.targets()
        archive = FlsArchive(result[art.FLS_PATH])
        texture = archive.texture(5)
        texture.indices[48 * 256:] = bytes(len(texture.indices) - 48 * 256)
        result[art.FLS_PATH] = archive.to_bytes()
        with self.assertRaisesRegex(AssertionError, 'Complete gold'):
            art.check_assets(result)


if __name__ == '__main__':
    unittest.main()
