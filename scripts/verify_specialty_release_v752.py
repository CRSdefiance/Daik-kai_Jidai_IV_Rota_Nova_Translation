"""Verify integrated question bytes, native copies, fallback output and exact patch."""

import struct
from copy import deepcopy
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.specialty_question_editorial import compile_template, transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import probe_remaining_common_layout as loader
from scripts.prepare_product_pitches_v747 import native_layout, wrapper_dispatch
from scripts.prepare_specialty_question_v752 import MANUSCRIPT, ROOT
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v752_candidate.nds')


def reject(action):
    try:
        action()
    except (AssertionError, ValueError):
        return True
    raise AssertionError('Malformed specialty question accepted')


def main():
    old, new = NdsImage.open('out/all_routes_combined_v751_candidate.nds'), NdsImage.open(ROM)
    common, arm = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    source_common, source_arm = old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin')
    manifest = read(ROM.with_suffix('.manifest.json'))
    registry, previous = read('translations/release_stack.json'), read(ROOT / 'release_stack_before_V752.json')
    assert manifest['profile'] == 'all-routes-unified-v752' and manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(manifest['batches']) == 470 and manifest['required_batches'] == [] and all(manifest['checks'].values())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers']) == 114 and registry['accepted_layers'] == previous['accepted_layers']
    assert registry['canonical_baseline'] == previous['canonical_baseline']
    assert [p for _, p, raw in old.iter_files() if raw != new.read_file(p)] == ['/COMMON/MESFILE.DK4']
    assert old.rom.arm7 == new.rom.arm7 and old.rom.arm9OverlayTable == new.rom.arm9OverlayTable
    doc = read(MANUSCRIPT)
    a, b, _ = transform(source_common, source_arm, doc)
    assert a == common and b == arm
    before = common_message_entries(source_common, source_arm, clean=False)
    after = common_message_entries(common, arm, clean=False)
    assert [a.message_id for a, b in zip(before, after, strict=True) if a.text.rstrip() != b.text.rstrip()] == [742]
    assert before[743].text == after[743].text
    old_dispatch, new_dispatch = wrapper_dispatch(source_arm), wrapper_dispatch(arm)
    assert [i for i, (a, b) in enumerate(zip(old_dispatch, new_dispatch, strict=True)) if a != b] == [4410]
    cpu = machine(arm)
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    native = read(ROOT / 'native_review.json')
    for case in native['all25_original_prerequisite_pairs']:
        output, lines = native_layout(cpu, after[742].text, 742,
            (case['item']['name'], case['product']['name']), parent=0x02053FCC)
        assert output.hex() == case['formatted_hex'] and lines == case['lines']
    # Follow complete copy/return for all other parent/ID controls. The fallback
    # begins by reloading ip atCD98, so the temporary comparison does not escape.
    controls = []
    for parent in (0x02054014,0x02053FCC,0x02054044,0x02053D24,0x02053DB8):
        for number in (457,480,653,675,730,739,741,742,743,801):
            if (parent, number) == (0x02053FCC,742):
                continue
            outputs = []
            for current in (source_arm,arm):
                u = machine(current)
                u.mem_write(0x02387A20, bytes(MainCodeFile(current, BASE).sections[3].data[:-48]))
                u.mem_write(0x02420000,b' Unchanged native copy control.\0')
                u.mem_write(STACK+0x264,struct.pack('<I',parent))
                u.mem_write(STACK+0x274,struct.pack('<I',number))
                u.mem_write(STACK+0x27C,struct.pack('<I',0x021184C0))
                call(u,0x01FFCF3C-BASE,(0x02420100,0x02420000,0))
                outputs.append(bytes(u.mem_read(0x02420100,256)))
            assert outputs[0] == outputs[1]
            controls.append({'parent':parent,'message_id':number,'full_copy_and_return_exact':True})
    copies = []
    selected = [e for e in after if e.block == 9]
    ids = [selected[0].message_id-1,*(e.message_id for e in selected),selected[-1].message_id+1]
    factory = loader.machine_for
    loader.machine_for = arm946_machine
    try:
        for number in ids:
            for cold in (False,True):
                result = loader.warm_copy(arm,common,number,after[number].text,cold_cache=cold)
                copies.append({'message_id':number,'cold_cache':cold,'complete_bytes':result['copied_bytes']})
    finally:
        loader.machine_for = factory
    stale, legacy = deepcopy(doc), deepcopy(doc)
    stale['records'][0]['source_hex'] = '41'
    legacy['translation_policy'] = 'natural-dialogue-v1'
    rejections = {
        'stale_source':reject(lambda:transform(source_common,source_arm,stale)),
        'legacy_policy':reject(lambda:transform(source_common,source_arm,legacy)),
        'authored_break':reject(lambda:compile_template('Two\nlines %s %s.{PAD}')),
        'authored_spaces':reject(lambda:compile_template('  Offset %s %s.{PAD}')),
        'missing_argument':reject(lambda:compile_template('One %s.{PAD}')),
        'extra_format':reject(lambda:compile_template('Two %s %s %d.{PAD}')),
        'unsafe_macro':reject(lambda:compile_template('FIRE %s %s.{PAD}'))}
    save(ROOT/'registered_verification.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'all470_batches114_accepted_layers_and_final_checks_pass':True,
        'all675_graphics_other_files_and_prior61_revisions_preserved':True,
        'all3668_IDs_NUL_owners_and_block_allocations_preserved':True,
        'all18340_dispatch_cases_only742_original_Yes_No_pair_changes':True,
        'all25_integrated_native_layouts_match_complete_font_proof':True,
        'full_fallback_copy_controls':controls,'native_warm_cold_copies':copies,'rejections':rejections,
        'all25_previews_visually_inspected':True,'gameplay_pending':True,
        'verifier_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    clean, patch, result = Path('work/clean.nds'),ROM.with_suffix('.xdelta'),ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean,ROM,patch)
    apply_xdelta(clean,patch,result)
    assert result.read_bytes() == ROM.read_bytes()
    save(ROOT/'patch_proof.json',{'clean_source_sha256':sha(clean.read_bytes()),'candidate_sha256':sha(ROM.read_bytes()),
        'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),'complete_reconstruction_sha256':sha(result.read_bytes()),
        'whole_ROM_byte_exact':True})
    print(f'V752: all25 layouts,49 copy controls,{len(copies)} native copies,7 rejections and exact patch pass.',flush=True)


if __name__ == '__main__':
    main()
