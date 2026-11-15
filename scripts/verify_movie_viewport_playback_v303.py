"""All five complete current movie cards after native-width correction."""

from scripts.prepare_movie_viewport_release_v303 import ROOT
from scripts.verify_movie_playback_v302 import CARDS, main
from scripts.verify_movie_viewport_release_v303 import ROM, read

if __name__ == '__main__':
    cards = [(path, index, name,
              ['Looks like a foreign merchant ship!', 'Admiral, your orders?']
              if path.endswith('M24.fls') and index == 4 else lines)
             for path, index, name, lines in CARDS]
    digest = read(ROOT / 'release_proof.json')['candidate_sha256']
    main(rom=ROM, root=ROOT, digest=digest, capture_prefix='movie_viewport_v303', cards=cards)
