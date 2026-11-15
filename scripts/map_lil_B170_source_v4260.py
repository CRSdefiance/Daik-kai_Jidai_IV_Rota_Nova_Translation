"""Bind33 clean/current complete preambles and45 commands after the clean-first gloss."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B170_source_v4260')
PRIOR = Path('work/analysis/editorial_handoff_verification_v4259/verified_handoff.json')
HISTORY = Path('work/analysis/lil_B169_source_v4211/all36_clean_current_complete_context.json')
GLOSS = Path('work/analysis/lil_B170_clean_context_v4257/all33_complete_B170_exchange_and_fresh_glosses.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    prior, history, gloss = map(read, [PRIOR, HISTORY, GLOSS])
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    assert sha(lp.read_bytes()) == prior['ledger_sha256']
    known = {historical_key(row) for row in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(known) == 5692
    current, clean = NdsImage.open(prior['candidate']), NdsImage.open('work/clean.nds')
    assert sha(Path(prior['candidate']).read_bytes()) == prior['candidate_sha256']
    arm, original = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    spans = [(0x2425C,0x242C8), (0x242CC,0x24310), (0x24314,0x24330), (0x24334,0x243A0), (0x2A1D8,0x2A600)]
    assert all(arm[a:b] == original[a:b] for a,b in spans)
    source, target = [IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[170] for image in [clean, current]]
    inventory, walker, inventory_source = scoped_inventory()
    old, spoken = inventory(original, source)
    now, translated = inventory(arm, target)
    shape = lambda commands: [(c['offset'],c['word'],c['native_extent'],c['ancestor_0100_offsets']) for c in commands]
    assert shape(old) == shape(now) and gloss['block']['clean_block_sha256'] == sha(source)
    assert old == gloss['block']['complete_native_commands'] and len(old) == 45 and len(spoken) == 33
    glosses = {row['id']: row for row in gloss['block']['records']}
    rows, selectors = [], [2,25]
    for sequence, (a,b) in enumerate(zip(spoken, translated, strict=True)):
        sa, ca = a['offset'] + 5, b['offset'] + 5
        raw = source[sa:source.index(b'\0', sa + 1)]
        value = target[ca:target.index(b'\0', ca + 1)]
        assert value[0] == raw[0] in selectors and source[sa - 5:sa + 1] == target[ca - 5:ca + 1]
        index = source[:sa].count(b'\0')
        row = deepcopy(glosses[f'DK4_MES_B170_R{index:04d}'])
        assert row['source_hex'] == raw.hex()
        row.update(current_record_index=target[:ca].count(b'\0'), current_reference=dict(offset=ca,bytes=len(value),header_offset=ca - 5),
            current_hex=value.hex(), source_presentation_prefix_hex=format(raw[0], '02x'), kind='progressive', source_kind='progressive',
            current_native_extent=b['native_extent'], native_command_extent=a['native_extent'], spoken_sequence_index=sequence,
            current_native_voice_macro_entry_and_context_pending=True, source_prose_or_completion_credit_added=0)
        rows.append(row)
    assert not known & {historical_key(row) for row in rows}
    assert {row['source_selector'] for row in rows} == set(selectors)
    assert current.read_file('/data/EV2.DK4') == clean.read_file('/data/EV2.DK4')
    assert sha(Path(history['actual_historical_snapshot']).read_bytes()) == history['actual_historical_snapshot_sha256']
    macros = {name: sum(bytes.fromhex(row['source_hex']).count(name.encode()) for row in rows) for name in ['FI','FA','FO']}
    assert macros == {'FI':1,'FA':0,'FO':1}
    assert sum(command['word'] in [0x100,0x200,0x300,0x400] for command in old) == 0
    assert not any(command['word'] in [0x2100,0x4100] for command in old)
    group = dict(block=170, clean_block_sha256=sha(source), current_block_sha256=sha(target), source_bytes=len(source), current_bytes=len(target),
        source_header_hex=source[:4].hex(), current_header_hex=target[:4].hex(), all_clean_native_commands=old, all_current_native_commands=now,
        source_native_commands=old, current_native_commands=now, source_current_native_command_shape_exact=True,
        records=rows, choices=[], physical_speeches=33, source_selectors=selectors, source_macro_counts=macros, FE_panels=0, relative_sites=0,
        all_complete_preambles_and_native_command_shapes_equal=True)
    ROOT.mkdir(parents=True)
    save(ROOT / 'all33_clean_current_complete_context.json', dict(format='dk4-editorial-source-context-packet-v1', file_path='/data/SC2.DK4',
        source_ROM='work/clean.nds', source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()), current_ROM=prior['candidate'], current_ROM_sha256=prior['candidate_sha256'],
        current_ARM9_sha256=sha(arm), source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')), current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),
        original_EV2_sha256=sha(current.read_file('/data/EV2.DK4')), actual_historical_snapshot=history['actual_historical_snapshot'],
        actual_historical_snapshot_sha256=history['actual_historical_snapshot_sha256'], historical_snapshot_ROM=history['historical_snapshot_ROM'],
        historical_snapshot_is_Lil_London_not_selected_B170=True, blocks=[group], records=rows, typed_choice_records=[], typed_actor_style_records=[],
        source_macro_counts=macros, total_editorial_objects=33, speech_objects=33, ordinary_source_speeches=33, system_FE_panels=0,
        source_selectors=selectors, source_static_actor_selectors=selectors, source_native_commands=45, source_relative_sites=0, source_predicates=0,
        source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans], source_transcript=gloss['source_transcript'],
        source_transcript_sha256=gloss['source_transcript_sha256'], whole_exchange_context_notes=str(GLOSS), whole_exchange_context_notes_sha256=sha(GLOSS.read_bytes()),
        all33_clean_first_glosses_already_recorded_before_current_comparison=True,
        current_native_voices_macros_entry_controls_fonts_actual_and_release_pending=True,
        no_ROM_registry_ledger_orcredit_change=True, new_emulator_runs=0,
        evidence={str(path):sha(path.read_bytes()) for path in [PRIOR,HISTORY,GLOSS,Path(__file__)]}, full_goal_complete=False))
    print('B170 mapped:33 complete preambles/45 commands/no relative sites,FI1/FO1;all glosses precede predecessor English exposure. No credit.')
