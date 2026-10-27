"""Create the V144 clean-ROM patch and verify its exact reconstruction."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta


def main():
    clean = Path('work/clean.nds')
    candidate = Path('out/all_routes_combined_v144_candidate.nds')
    proof = json.loads(Path('work/analysis/options_narrow_v144_saved_rom_proof.json').read_text(encoding='utf-8'))
    digest = sha(candidate.read_bytes())
    if proof['candidate_sha256'] != digest:
        raise ValueError('Saved-ROM proof does not match V144')
    clean_digest = sha(clean.read_bytes())
    if clean_digest != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Clean patch source differs')
    patch = candidate.with_suffix('.xdelta')
    reconstructed = Path('work/analysis/options_narrow_v144_patch_roundtrip.nds')
    make_xdelta(clean, candidate, patch)
    apply_xdelta(clean, patch, reconstructed)
    if reconstructed.read_bytes() != candidate.read_bytes():
        raise ValueError('V144 patch reconstruction differs')
    result = {'status': 'pass-byte-exact', 'candidate_sha256': digest,
              'clean_sha256': clean_digest, 'patch_sha256': sha(patch.read_bytes()),
              'patch_bytes': patch.stat().st_size, 'gameplay_accepted': False}
    Path('work/analysis/options_narrow_v144_patch_roundtrip.json').write_text(
        json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
