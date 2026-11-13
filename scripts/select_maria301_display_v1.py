"""Select source-ordered display exchanges for the concrete Maria pagination risks."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B0_B32_clean_20261109')
OUT = ROOT/'representative_selection_v1.json'
REBUILT = ROOT/'stored_reconstruction_v1/reconstruction.json'


def main():
    assert not OUT.exists()
    rebuilt = load(REBUILT)
    selected = [4, 8, 14, 18, 24, 29, 30, 32]
    sequence = []
    for g in rebuilt['groups']:
        if g['block'] not in selected:
            continue
        ordinary = {r['new_offset']-5: r for r in g['text_records']}
        compound = {r['new_offset']: r for r in g['native_objects']}
        for command in g['all_target_commands']:
            at = command['offset']
            if at in ordinary:
                sequence.append(dict(speech=ordinary[at]['id']))
            elif at in compound:
                obj = compound[at]
                request = dict(block=g['block'], source_command_offset=obj['old_offset'])
                if command['word'] == 0x4100:
                    request['expected_style'] = 4
                    sequence.append(dict(style=request))
                else:
                    assert command['word'] == 0x2100
                    sequence.append(dict(menu=request))
    assert sum('menu' in x for x in sequence) == sum('style' in x for x in sequence) == 1
    save(OUT, dict(fixtures=[dict(name='maria301_pagination_menu_style', sequence=sequence,
        purpose='Representative reviewed-English display from eight source-ordered exchanges: four two-page speeches, B24 reclaimed page, B14 mixed-I correction, B29 menu/default controller return and complete B32 lookout style object. Original optional conditions and effects are not activated.',
        selected_complete_source_blocks=selected)], selected_blocks=selected,
        unvisited_blocks=[g['block'] for g in rebuilt['groups'] if g['block'] not in selected],
        actual_gameplay_pending=True, natural_activation=False, earned_chronology=False,
        alternative_voice_bodies_not_selected_remain_offline_only=True, new_credit=0,
        evidence={str(p):digest(p) for p in [REBUILT, Path(__file__)]}))
    print('Selected',sum('speech' in x for x in sequence),'ordinary calls plus one menu and one complete style object.')


if __name__ == '__main__':
    main()
