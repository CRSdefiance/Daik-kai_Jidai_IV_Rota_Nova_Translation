"""Select complete display commands, split at block boundaries before the proven QA capacity."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B311_B324_formatting_v1 import ROOT

OUT = ROOT/'bounded_selection_v1.json'
CAPACITY = Path('work/Hodram_B301_B310_clean_20261107/native_QA_capacity_v1.json')

def main():
    assert not OUT.exists()
    reconstruction = ROOT/'reconstruction_v1/reconstruction.json'
    rebuilt = load(reconstruction)
    doc = load(rebuilt['manuscript'])
    capacity = load(CAPACITY)
    image = NdsImage.open(rebuilt['research_ROM'])
    arm = image.read_file('/__arm9__.bin')
    assert digest(rebuilt['research_ROM']) == rebuilt['research_ROM_sha256']
    from dk4tool.patch.grand_race_menu_release import sha
    assert sha(arm) == capacity['registered_ARM9_sha256']
    assert capacity['source_current_consumer_code_exact'] and capacity['safe_QA_block_limit'] == 9216
    assert len(rebuilt['groups']) == 14 and max(g['target_bytes'] for g in rebuilt['groups']) <= 9216
    bank = IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
    inventory, _, _ = scoped_inventory()
    opening, speeches = inventory(arm, bank[42])
    first = speeches[0]['offset']
    assert first == 42 and [c['word'] for c in opening[-2:]] == [0xC200, 0]
    exit_bytes = sum(len(bytes.fromhex(c['whole_command_hex'])) for c in opening[-2:])
    assert exit_bytes == 6
    chunks, pending, pending_bytes, total_bytes = [], [], 0, 0
    for group in rebuilt['groups']:
        block = group['block']
        ordinary = {r['new_offset']-5: r for r in group['text_records']}
        compound = {r['new_offset']: r for r in group['native_objects']}
        actions, used = [], []
        for command in group['all_target_commands']:
            at = command['offset']
            if at in ordinary:
                row = ordinary[at]
                assert command['word'] == 0x4000
                action = dict(speech=row['id'])
            elif at in compound:
                obj = compound[at]
                assert obj['word'] == command['word']
                request = dict(block=block, source_command_offset=obj['old_offset'])
                action = {'style' if obj['word'] == 0x4100 else 'menu': request}
                if obj['word'] == 0x4100:
                    action['style']['expected_style'] = 4
                else:
                    assert obj['word'] in [0x2100, 0x2200]
            else:
                continue
            actions.append(action)
            used.append(command)
        assert len(actions) == len(ordinary) + len(compound)
        size = sum(len(bytes.fromhex(c['whole_command_hex'])) for c in used)
        padded = lambda n: (first + n + exit_bytes + 3)//4*4
        assert padded(size) <= 9216, (block, padded(size))
        if pending and padded(pending_bytes + size) > 9216:
            chunks.append((pending, pending_bytes))
            pending, pending_bytes = [], 0
        pending.append(dict(block=block, actions=actions, copied_command_bytes=size))
        pending_bytes += size
        total_bytes += size
    if pending:
        chunks.append((pending, pending_bytes))
    fixtures = []
    for index, (groups, size) in enumerate(chunks, 1):
        blocks = [g['block'] for g in groups]
        fixtures.append(dict(name=f'hodram_B311_B324_part{index}',
            purpose='Disclosed English display QA: complete ordinary speeches, full native personality commands and menus from source blocks '+','.join(map(str, blocks))+'. Original optional-event chronology, branches, rewards and outcomes are not activated.',
            sequence=[action for g in groups for action in g['actions']],
            selected_complete_source_blocks=blocks, estimated_padded_QA_block_bytes=padded(size)))
    all_actions = [a for f in fixtures for a in f['sequence']]
    counts = {key: sum(key in a for a in all_actions) for key in ['speech','style','menu']}
    assert counts == dict(speech=151, style=38, menu=6)
    assert [b for f in fixtures for b in f['selected_complete_source_blocks']] == list(range(311,325))
    save(OUT, dict(fixtures=fixtures, selection_counts=counts, selected_utterances=189, expected_body_pages=191,
        all151_ordinary_speeches_selected=True, all38_whole_style_commands_selected_at_original_voice4=True,
        all_six_menus_selected=True, remaining198_physical_style_variants_offline_only=True,
        original_source_order_preserved_within_andacross_disjoint_fixtures=True,
        complete_block_boundary_splits_only=True, safe_QA_block_limit=9216,
        total_copied_display_command_bytes=total_bytes,
        current_production_blocks_inside_same_conservative_bound=True,
        current_production_max_target_block_bytes=max(g['target_bytes'] for g in rebuilt['groups']),
        no_source_branch_stat_orconditional_activation_claim=True, no_new_credit=True,
        evidence={str(p): digest(p) for p in [reconstruction, Path(rebuilt['manuscript']), CAPACITY, Path(__file__)]}))
    print(dict(fixtures=len(fixtures), selection_counts=counts,
        bounded_bytes=[f['estimated_padded_QA_block_bytes'] for f in fixtures],
        blocks=[f['selected_complete_source_blocks'] for f in fixtures], new_credit=0))

if __name__ == '__main__':
    main()
