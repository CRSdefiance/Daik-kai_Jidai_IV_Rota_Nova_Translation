"""Check every menu binding while reusing exact repeated complete menu objects."""
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
import subprocess
import sys
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from dk4tool.patch.grand_race_menu_release import sha

MANUSCRIPT = Path('work/analysis/Hodram_B191_B210_formatting_20261104/formatting_input.json')
ROOT = Path('work/analysis/Hodram_B191_B210_menus_20261104')
RELEASE = Path('work/analysis/Hodram_B171_B190_release_verified_20261104/registered_release_verification.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    doc = load(MANUSCRIPT)
    groups = defaultdict(list)
    for row in doc['records']:
        if row['kind'] == 'typed-choice-label':
            groups[(row['block'], row['source_command_offset'])].append(row)
    assert len(groups) == 10 and sum(map(len, groups.values())) == 21
    ROOT.mkdir()
    cache, objects = {}, []
    alignments = bridged = planes = 0
    for (block, offset), rows in groups.items():
        count = len(rows)
        assert count in [2, 3] and [r['source_index'] for r in rows] == list(range(count))
        source, current = map(bytes.fromhex, [rows[0]['source_choice_object_hex'], rows[0]['current_choice_object_hex']])
        target = compile_choices(source, current, rows, require_formatting=False)
        identity = (source.hex(), current.hex(), target.hex(), tuple(r['english'] for r in rows))
        reused = identity in cache
        if not reused:
            subset = deepcopy(doc)
            subset.update(records=rows, blocks=[block], total_editorial_objects=count, physical_speech_objects=0,
                ordinary_speech_objects=0, typed_choice_objects=count, typed_choice_commands=1,
                personality_alternatives=0, personality_alias_slots=0,
                subset_of=str(MANUSCRIPT), subset_of_sha256=sha(MANUSCRIPT.read_bytes()))
            path = ROOT / f'B{block}_C{offset}_manuscript.json'
            save(path, subset)
            out = ROOT / f'B{block}_C{offset}'
            checker = 'scripts/check_editorial_two_choice_display.py' if count == 2 else 'scripts/check_editorial_three_choice_single.py'
            subprocess.run([sys.executable, checker, '--manuscript', str(path), '--release', str(RELEASE),
                '--startup', str(RELEASE.with_name('own_registered_startup_verification.json')), '--out', str(out)], check=True)
            proof_path = out / 'menu_provider_and_planes.json'
            proof = load(proof_path)
            compiled = out / ('compiled_choice_object.bin' if count == 2 else f'B{block}_C{offset}_compiled_choice_object.bin')
            assert compiled.read_bytes() == target
            assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
            alignments += proof['native_provider_alignments']
            bridged += proof['bridged_modal_returns']
            planes += proof['complete_English_caption_style_planes']
            cache[identity] = dict(receipt=str(proof_path), receipt_sha256=sha(proof_path.read_bytes()),
                compiled_path=str(compiled), compiled_sha256=sha(target),
                review_sheets=[proof['review_sheet']] if count == 2 else proof['review_sheets'])
        record = dict(block=block, source_command_offset=offset, record_ids=[r['id'] for r in rows], count=count,
            source_object_hex=source.hex(), current_object_hex=current.hex(), target_object_hex=target.hex(),
            source_current_andreviewed_complete_object_identity=(sha(source), sha(current), sha(target)),
            exact_complete_object_andcode_dependencies_reused=reused, **cache[identity])
        objects.append(record)
        print('Menu', block, offset, 'exact reuse' if reused else 'fresh native checks', flush=True)
    save(ROOT / 'complete_choice_objects.json', dict(manuscript=str(MANUSCRIPT), manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        objects=objects, physical_caption_records=21, fresh_distinct_menus=len(cache), exact_complete_menu_reuses=10-len(cache),
        fresh_native_provider_alignments=alignments, fresh_bridged_modal_returns=bridged, fresh_complete_caption_style_planes=planes,
        every_caption_source_current_target_bound=True, all_checks_pass=True, direct_view_pending=True,
        actual_gameplay=False, stored_integration_andactual_controller_still_pending=True, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [MANUSCRIPT, RELEASE, Path(__file__)]}))
    print('All 21 captions bound; fresh menus', len(cache), 'exact repeated menus reused', 10-len(cache), flush=True)
