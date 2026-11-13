"""Snapshot every source/current given name and concrete older-fidelity leads."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.residual_character_name_release import TARGET
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.prepare_residual_character_names import loaded

LEADS = {
    131: 'Unnecessary abbreviation: clean 総督 identifies a governor.',
    134: 'Rank qualifier lost: clean 高僧 identifies a senior monk.',
    136: 'Rank qualifier lost: clean 高僧 identifies a senior monk.',
    137: 'Rank qualifier lost: clean 高僧 identifies a senior monk.',
    164: 'Source marks the male half of a couple; current Young Man adds age and omits relationship. Review scene context.',
    165: 'Source marks the female half of a couple; current Young Woman adds age and omits relationship. Review scene context.',
    169: 'Enchantress may imply magic; clean 妖艶な女 describes an alluring woman. Review context.',
    170: 'Mystery qualifier omitted from clean 謎の老人.',
    172: 'Castaway implies a nautical situation; clean 行き倒れ identifies someone collapsed. Review scene context.',
    173: 'Suspicious qualifier omitted from clean 怪しい人.',
    185: 'Dundee does not match the source phonetic label ダンディー (Dandy); verify character context.',
    203: 'Cherry translates the meaning of さくら instead of preserving its likely proper-name reading Sakura; verify context/glossary.',
}


def main():
    image = NdsImage.open('out/all_routes_combined_v150_candidate.nds')
    current = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    if sha(current) != TARGET or sha(clean) != '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731':
        raise ValueError('Exact saved V150 and clean source required')
    machine = loaded(current)
    rows = []
    for index in range(207):
        field = 0x120B80 + index * 32
        source_pointer = struct.unpack_from('<I', clean, field)[0]
        source_text = clean[source_pointer - 0x02000000:].split(b'\0', 1)[0].decode('cp932')
        pointer = ordinary_getter(current, index, machine)
        expected = struct.unpack_from('<I', current, field)[0]
        if pointer != expected:
            raise ValueError('Current native getter and table owner differ')
        raw = bytes(machine.mem_read(pointer, 128)).split(b'\0', 1)[0]
        text = raw.decode('cp932')
        rows.append({'index': index, 'table_field': field, 'clean_japanese': source_text,
                     'source_pointer': source_pointer, 'runtime_pointer': pointer,
                     'current_english': text, 'current_hex': raw.hex(),
                     'native_getter_verified': True,
                     'fidelity_followup': LEADS.get(index),
                     'inherited_full_width_latin': any('\uff21' <= c <= '\uff5a' for c in text)})
    proof = {'status': 'complete-table-inventory-fidelity-review-open',
             'candidate_sha256': sha(Path('out/all_routes_combined_v150_candidate.nds').read_bytes()),
             'arm9_sha256': TARGET, 'clean_arm9_sha256': sha(clean), 'rows': rows,
             'source_fidelity_lead_indices': sorted(LEADS),
             'inherited_full_width_latin_indices': [r['index'] for r in rows if r['inherited_full_width_latin']],
             'limits': ['Flags are source comparison leads requiring context review, not automatically approved replacement prose.',
                        'Unflagged rows have not passed exhaustive semantic/localization review.',
                        'Native character type/scene eligibility and physical gameplay remain fixtures/unverified.']}
    Path('work/analysis/given_name_fidelity_v150.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'All 207 saved ordinary names/source labels inventoried; {len(LEADS)} concrete fidelity leads and five inherited full-width Latin names recorded.')


if __name__ == '__main__':
    main()
