"""Advance Karibib's actual arrival story until the original Town screen is visible."""

from PIL import Image

from scripts import run_village_development_v665 as original
from scripts.run_village_visits_v664 import CAP


class StoryController(original.Controller):
    def navigate(self):
        assert self.village == 9
        yield from super().navigate()
        reference = Image.open(CAP / 'village_development_v665_01_first/frame_012300_final.png').convert('RGB')
        corners = ((0, 0, 12, 24), (244, 0, 256, 24), (0, 176, 12, 192))
        # These fixed border anchors only guide ordinary input. The independent
        # verifier subsequently reconstructs the entire actual Town scene.
        for _ in range(32):
            image = self.image()
            if all(image.crop(b).tobytes() == reference.crop(b).tobytes() for b in corners):
                self.phases['developed_town_return'] = self.frame
                return
            self.phases.setdefault('first_Karibib_arrival_story', self.frame)
            yield self.command(buttons=['A'], frames=400)
        raise AssertionError('Karibib arrival story did not reach the Town screen within32 ordinary advances')


if __name__ == '__main__':
    original.Controller = StoryController
    original.main()
