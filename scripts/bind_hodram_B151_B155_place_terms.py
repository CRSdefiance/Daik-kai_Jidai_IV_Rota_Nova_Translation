"""Read two existing native city labels without exposing earlier dialogue."""
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import string
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B151_B170_clean_20261102')


if __name__ == '__main__':
    out = ROOT / 'B151_B155_place_terms.json'
    assert not out.exists()
    bound = load(ROOT / 'native_identity_and_item_checkpoint_v1.json')
    runtime = bound['runtime']
    rom = Path(runtime['candidate'])
    assert sha(rom.read_bytes()) == runtime['candidate_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    current = NdsImage.open(rom).read_file('/__arm9__.bin')
    raw = Path(runtime['snapshot']['path']).read_bytes()
    assert sha(raw) == runtime['snapshot']['sha256']
    rows = []
    for at, ja, en in [(1199308, 'アブハーズ', 'Abhaz'), (1192116, 'アレキサンドリア', 'Alexandria')]:
        source_pointer = struct.unpack_from('<I', clean, at)[0]
        current_pointer = struct.unpack_from('<I', current, at)[0]
        source = string(clean, source_pointer)
        start = current_pointer - 0x02000000
        end = raw.index(0, start)
        target = raw[start:end]
        assert source['text'] == ja and target.decode('cp932') == en
        rows.append(dict(pointer_field_offset=at, clean_pointer_hex=clean[at:at + 4].hex(),
                         current_pointer_hex=current[at:at + 4].hex(), source=source,
                         current_pointer=current_pointer, complete_current_name_hex=target.hex(), english=en,
                         retain_established_place_label_for_dialogue=True,
                         no_new_global_place_name_localization_orUI_approval=True))
    save(out, dict(runtime=runtime, records=rows, prior_dialogue_unconsulted_by_this_binding=True,
                   full_goal_place_name_review_remains_open=True, new_credit=0,
                   evidence={str(p):sha(p.read_bytes()) for p in [ROOT/'native_identity_and_item_checkpoint_v1.json', Path(__file__)]}))
    print('Two existing place labels bound:Abhaz/Alexandria; no new place-name orUI approval.')
