"""Approach developed Karibib after its original encounter scene, without battle flags."""

from PIL import Image

from scripts import run_village_development_v665 as original
from scripts.run_village_visits_v664 import CAP
from scripts.verify_plaque_release_v247 import find_mask


class KaribibController(original.Controller):
    def navigate(self):
        assert self.village == 9
        yield from super().navigate()
        reference = Image.open(CAP / 'village_development_v665_09_story/frame_016580_navigation.png').convert('RGB')
        footer = reference.crop((0, 366, 256, 384)).tobytes()
        for _ in range(12):
            if self.image().crop((0, 366, 256, 384)).tobytes() == footer:
                break
            yield self.command(buttons=['A'], frames=400)
        else:
            raise AssertionError('Original encounter did not return to ordinary Sea controls')
        self.phases['post_story_coordinate_approach'] = self.frame
        yield {'until': self.frame + 400, 'location_town': 9}
        self.phases['post_story_docking_prompt'] = self.frame
        yield self.command(buttons=['A'], frames=400)
        # A full exact title mask prevents credit for a later unrelated port.
        find_mask(self.font, 'Karibib', self.image(), (0, 10, 256, 40))
        self.phases['developed_town_return'] = self.frame


if __name__ == '__main__':
    original.Controller = KaribibController
    original.main()
