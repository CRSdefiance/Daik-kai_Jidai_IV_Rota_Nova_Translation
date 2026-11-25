"""Current resident ranges, arena bounds and conservative cross-patch references."""

import json
from pathlib import Path
import re
import struct

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.audit_common_word_wrap_itcm_refs import references
from scripts.probe_common_itcm_arena_reservation import initialize, bounds

ROOT = Path('work/patch_interaction_audit_20261027')
ROM = Path('out/font_v2_square_scratch_fix_20261027_test.nds')


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def address_leaves(value, key=''):
    result = []
    if isinstance(value, dict):
        for name, item in value.items():
            result.extend(address_leaves(item, key + '/' + name))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            result.extend(address_leaves(item, key + '/' + str(index)))
    elif isinstance(value, int) and not isinstance(value, bool) and 0x01FF0000 <= value <= 0x02800000:
        result.append(dict(field=key, address=value))
    elif isinstance(value, str) and re.fullmatch(r'0x[0-9a-fA-F]{7,8}', value):
        address = int(value, 16)
        if 0x01FF0000 <= address <= 0x02800000:
            result.append(dict(field=key, address=address))
    return result


def main():
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    manifest = json.loads(ROM.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    stack = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    assert sha(ROM.read_bytes()) == json.loads((ROOT / 'target.json').read_text())['sha256']
    profile = stack['profiles'][manifest['profile']]
    sections = MainCodeFile(arm, 0x02000000).sections
    units = [('section' + str(i), s.ramAddress, bytes(s.data)) for i, s in enumerate(sections)]
    overlays = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.files[fid])
    units += [('overlay' + str(i), s.ramAddress, bytes(s.data)) for i, s in overlays.items()]
    section_ranges = [dict(index=i, address=s.ramAddress, end=s.ramAddress+len(s.data),
        bytes=len(s.data), bss=s.bssSize, sha256=sha(bytes(s.data))) for i,s in enumerate(sections)]
    collisions = []
    for i, a in enumerate(section_ranges):
        for b in section_ranges[i+1:]:
            if max(a['address'], b['address']) < min(a['end'], b['end']):
                collisions.append([a['index'], b['index']])
    assert not collisions
    # The two ITCM virtual addresses must also remain disjoint after hardware mirroring.
    itcm = [(s.ramAddress & 0x7FFF, (s.ramAddress & 0x7FFF)+len(s.data)) for s in sections if s.ramAddress < 0x02000000]
    assert all(max(a[0],b[0]) >= min(a[1],b[1]) for i,a in enumerate(itcm) for b in itcm[i+1:])
    arena = initialize(arm)
    getters = bounds(arm)
    cache = cache_plan(arm)
    save('resident_and_arena_proof.json', dict(ROM_sha256=sha(ROM.read_bytes()), sections=section_ranges,
        ITCM_mirrored_ranges=itcm, resident_sections_disjoint=True, native_arena=arena,
        native_ITCM_arena_getters=getters, main_copy_cache_contract=cache,
        overlay_ranges=[dict(name=n, address=b, end=b+len(raw)) for n,b,raw in units if n.startswith('overlay')],
        limitation='Overlay windows are not assumed simultaneous; staged storage may be reused after the startup copy.'))
    refs = []
    for name, base, raw in units:
        for row in references(raw, base, 0x01FFC000, 0x01FFD000):
            refs.append(dict(component=name, **row))
    save('current_ITCM_reference_census.json', dict(units=len(units), references=refs,
        method='All aligned absolute words, ARM branch candidates and Thumb BL/BLX pairs; data aliases are retained as leads.'))
    stages = {}
    configs = {}
    dependencies = set()
    for name, value in profile.items():
        if isinstance(value, str) and value.endswith('.json') and Path(value).exists():
            config = json.loads(Path(value).read_text(encoding='utf-8'))
            leaves = address_leaves(config)
            stages[name] = dict(config=value, config_sha256=sha(Path(value).read_bytes()), address_fields=leaves)
            configs[name] = config
            if isinstance(config.get('dependencies'), dict):
                dependencies.update(p for p in config['dependencies'] if p.endswith(('.py','.asm')) and Path(p).exists())
    save('registered_memory_declarations.json', stages)
    source_leads = []
    for file in sorted(dependencies):
        for line, text in enumerate(Path(file).read_text(encoding='utf-8').splitlines(), 1):
            if re.search(r'(zero|blank|unused|scratch|buffer|reserv|owned|SLOT|START|END|POOL|STAGE)', text, re.I):
                source_leads.append(dict(file=file,line=line,text=text))
    save('registered_source_ownership_leads.json', dict(dependencies=len(dependencies), rows=source_leads))
    print('Five resident sections and mirrored ITCM spans disjoint; native arena/copy checks pass;',len(refs),'ITCM reference leads;',len(stages),'registered config declarations;',len(dependencies),'source dependencies.')


if __name__ == '__main__':
    main()
