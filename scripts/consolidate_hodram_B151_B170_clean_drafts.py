"""Seal all642 logical drafts before exposing current-ROM dialogue for comparison."""
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import string
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B151_B170_clean_20261102')
PARTS = ['B151_B155_42', 'B156_86', 'B157_B158_73', 'B159_61', 'B160_69', 'B161_B166_101', 'B167_B168_115', 'B169_B170_87']


if __name__ == '__main__':
    target = ROOT / 'all642_clean_English_drafts_v1.json'
    assert not target.exists()
    ordinary_meanings = ROOT / 'all634_clean_meanings_before_English_v1.json'
    meanings = load(ordinary_meanings)
    paths = [ROOT / (p + '_clean_English_drafts_v1.json') for p in PARTS]
    captions = ROOT / 'eight_clean_caption_English_drafts_v1.json'
    ordinary = [r for p in paths for r in load(p)['records']]
    menu = load(captions)['records']
    rows = ordinary + menu
    assert len(rows) == len({r['id'] for r in rows}) == 642 and len(ordinary) == 634 and len(menu) == 8
    assert {r['id'] for r in ordinary} == {r['id'] for r in meanings['records']}
    assert all(r['review']['formatting'] is False and r['new_credit'] == 0 for r in rows)
    assert all(all(r['review'][k] is True for k in ['source','context','localization','naturalness']) for r in rows)
    assert len([r for r in ordinary if r['source_selector'] == 254]) == 32
    assert len([r for r in ordinary if r['source_selector'] == 0]) == 9
    assert sum(bool(r.get('incidental_legacy_line_exposure')) for r in rows) == 1
    runtime = load(ROOT / 'native_identity_and_item_checkpoint_v1.json')['runtime']
    candidate = Path(runtime['candidate'])
    assert sha(candidate.read_bytes()) == runtime['candidate_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    current = NdsImage.open(candidate).read_file('/__arm9__.bin')
    raw = Path(runtime['snapshot']['path']).read_bytes()
    assert sha(raw) == runtime['snapshot']['sha256']
    room_rows = []
    for field, ja, en in [(1123868,'海兵詰所','Quarters'),(1123876,'武装砲台','Battery'),
                          (1123884,'物資倉庫','Supplies'),(1123892,'積荷倉庫','Cargo')]:
        source = string(clean, struct.unpack_from('<I',clean,field)[0])
        pointer = struct.unpack_from('<I',current,field)[0]
        start = pointer - 0x02000000
        end = raw.index(0,start)
        text = raw[start:end]
        assert source['text'] == ja and text.decode('cp932') == en
        room_rows.append(dict(source=source, current_pointer_field_offset=field,
                              current_pointer_hex=current[field:field+4].hex(), current_pointer=pointer,
                              complete_current_name_hex=text.hex(), current_UI_label=en,
                              dialogue_explanation_does_not_rename_UI=True))
    rooms = ROOT / 'four_ship_room_terms_current_bindings.json'
    assert not rooms.exists()
    save(rooms,dict(runtime=runtime,records=room_rows,new_credit=0,new_native_calls=0,earlier_dialogue_not_read=True))
    dependencies = [*paths,captions,ordinary_meanings,ROOT/'eight_clean_caption_meanings_before_English.json',
                    ROOT/'native_identity_and_item_checkpoint_v1.json',ROOT/'B151_B155_place_terms.json',
                    ROOT/'remaining_role_ship_and_Venice_terms_v1.json',rooms,Path(__file__)]
    save(target,dict(format='dk4-complete-source-first-logical-English-drafts-v1', translation_policy='natural-dialogue-v2',
                     target_locale='en-US',review_gates=['source','context','localization','naturalness','formatting'],
                     file_path='/data/SC1.DK4',blocks=list(range(151,171)),records=rows,
                     ordinary_speeches=634,typed_captions=8,choice_objects=4,total_editorial_objects=642,
                     complete_clean_meanings_precede_any_legacy_exposure=True,
                     all642_drafts_saved_before_current_ROM_dialogue_extraction=True,
                     incidental_one_legacy_generator_line_disclosed=True,
                     current_English_conversation_comparison_pending=True,
                     no_authored_ordinary_linebreaks_alignment_orpadding=True,
                     B156_cinematic_native_geometry_still_pending=True,
                     separate_Elysion_native_code_literal_still_Japanese_pending_scope=True,
                     individual_source_first_draft_prose_gates_not_final_current_comparison=True,
                     source_draft_checks_not_formatting_stored_visual_gameplay_orrelease_approval=True,
                     new_credit=0,new_ROMs=0,new_emulator_runs=0,full_goal_complete=False,
                     evidence={str(p):sha(p.read_bytes()) for p in dependencies}))
    # Compatibility input: exact immutable clean meanings, not the English manuscript.
    binding_input = ROOT / 'ordinary_meanings_for_current_binding.json'
    assert not binding_input.exists()
    assert all(r['earlier_English_unconsulted'] for r in meanings['records'])
    save(binding_input,dict(**meanings,meanings=634,all642_drafts_sealed=str(target),
                           all642_drafts_sha256=sha(target.read_bytes()),
                           meanings_flags_describe_clean_reading_before_incidental_legacy_line=True))
    empty = ROOT / 'clean_no_style_objects.json'
    assert not empty.exists()
    packet = load(ROOT / 'clean_source_packet.json')
    assert not any(c['word'] == 0x4100 for g in packet['groups'] for c in g['all_source_commands'])
    save(empty,dict(records=[],style_objects=0,source_packet=str(ROOT/'clean_source_packet.json'),
                    source_packet_sha256=sha((ROOT/'clean_source_packet.json').read_bytes()),new_credit=0))
    print('Sealed all642 logical English drafts:634 speeches/8 captions,20 whole blocks;four room labels bound. Comparison/formatting remain open.')
