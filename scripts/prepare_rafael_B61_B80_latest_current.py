"""Qualify exact dependency reuse and expose only the newly sealed remaining342."""
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_rafael_B61_B80_source_context import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT = Path('work/analysis/Rafael_B61_B80_clean_20261104')
RUNTIME = Path('work/analysis/Rafael_B61_B80_latest_runtime_20261104')
NEW = Path('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')
OLD = Path('work/analysis/Shared_tutorial_name_data_release_verified_20261104/registered_release_verification.json')
CURRENT197 = Path('work/analysis/Rafael_B61_B64_current_20261104/current_effective.json')

if __name__ == '__main__':
    assert not RUNTIME.exists()
    outputs = [ROOT/name for name in ['B65_B80_all342_sealed_drafts_v1.json',
        'B65_B80_selected_source_packet_v1.json', 'B65_B80_current_binding_source_v1.json',
        'B61_B80_all539_individually_source_first_drafts_v1.json']]
    assert not any(p.exists() for p in outputs)
    sealed, selected, target, all539 = outputs
    identity_path = ROOT/'source_identity_event_andterm_checkpoint_v1.json'
    identity = load(identity_path)
    old = RegisteredRuntime(OLD, OLD.with_name('own_registered_startup_verification.json'), captain=0)
    new = RegisteredRuntime(NEW, NEW.with_name('own_registered_startup_verification.json'), captain=0)
    assert old.receipt() == identity['runtime']
    release = load(NEW)
    assert release['parent_sha256'] == old.release['candidate_sha256']
    assert release['only_reviewed_SC0_ten_blocks_andone_owned_name_field_changed']
    inverse = bytearray(new.arm)
    spans = new.startup['Fernan_name_field_inverse']['fields']
    assert len(spans) == 1 and spans[0]['actor'] == 35 and 35 not in identity['actors']
    for span in spans:
        at, size = span['physical_offset'], span['owned_bytes']
        assert inverse[at:at+size].hex() == span['new_hex']
        inverse[at:at+size] = bytes.fromhex(span['old_hex'])
    assert bytes(inverse) == old.arm
    assert new.common == old.common and new.actor_root == old.actor_root and new.actor_bytes == old.actor_bytes
    resources = ['/COMMON/HELP.DK4', '/GRP/KANJI.FNT', '/data/EV0.DK4']
    assert all(new.image.read_file(p) == old.image.read_file(p) for p in resources)
    assert sha(new.image.read_file('/data/EV0.DK4')) == identity['source_EV0_sha256']
    old_archive, new_archive = [ctx.image.read_file('/data/SC0.DK4') for ctx in [old, new]]
    old_bank, new_bank = [IlnkContainer.parse(raw).blocks for raw in [old_archive, new_archive]]
    assert len(old_bank) == len(new_bank) == 343
    changed = [i for i, (a,b) in enumerate(zip(old_bank, new_bank, strict=True)) if a != b]
    assert changed == list(range(51,61))
    block_reuse = []
    for number in range(61,81):
        assert old_bank[number] == new_bank[number]
        block_reuse.append(dict(block=number, sha256=sha(new_bank[number]), byte_exact=True))
    fields = []
    for actor in identity['name_bindings']:
        for field in actor['source_andcurrent_fields']:
            at, pointer = field['current_field'], field['current_pointer']
            assert old.arm[at:at+4] == new.arm[at:at+4] == struct.pack('<I', pointer)
            before, after = string(old.raw, pointer), string(new.raw, pointer)
            assert before == after and after.hex() == field['current_hex']
            fields.append(dict(actor=actor['actor_ID'], column=field['column'], pointer=pointer,
                field_offset=at, text_hex=after.hex(), exact=True))
    assert len(fields) == 66
    draft_paths = [ROOT/name for name in [
        'B65_B67_92_logical_English_drafts_v2.json', 'B69_B70_108_logical_English_drafts_v1.json',
        'B71_B75_116_logical_English_drafts_v2.json', 'B76_B80_26_logical_English_drafts_v1.json']]
    rows = [r for p in draft_paths for r in load(p)['records']]
    assert len(rows) == 342 and len({r['id'] for r in rows}) == 342
    assert all(r['earlier_English_unconsulted'] and r['current_English_comparison_pending']
               and not r['review']['formatting'] for r in rows)
    prior197_path = ROOT/'B61_B64_all197_sealed_drafts_v1.json'
    prior197 = load(prior197_path)
    assert {r['id'] for r in rows+prior197['records']} == {r['id'] for r in identity['records']}
    RUNTIME.mkdir(parents=True)
    qualification_path = RUNTIME/'dependency_qualification.json'
    save(qualification_path, dict(runtime=new.receipt(), previous_runtime=old.receipt(),
        complete_ARM9_inverse_exact_to_parent=True, sole_excluded_field=spans[0],
        all_unowned_ARM9_instructions_allocations_tables_andpointers_exact=True,
        complete_actor_array_androot_exact=True, all22_actor_three_fields_exact=fields,
        all20_SC0_blocks_exact=block_reuse, only_changed_SC0_blocks=changed,
        COMMON_HELP_font_andEV0_exact={p:sha(new.image.read_file(p)) for p in ['/COMMON/MESFILE.DK4']+resources},
        native_name_consumers_anddefault_Rafael_macro_dependencies_compatible=True,
        source_event_context_andfive_Charlotte_FE_presentations_preserved=True,
        prior_native_proofs_reused_not_new_getter_orpage_executions=True,
        latest_own_snapshot_not_old_RAM_relabelled=True, no_new_gameplay_orROM_orcredit=True,
        evidence={str(p):sha(p.read_bytes()) for p in [identity_path, OLD, NEW, CURRENT197, Path(__file__)]},
        new_credit=0, guide_photos=False))
    current = load(CURRENT197)
    assert current['current_ROM_sha256'] == old.release['candidate_sha256'] and current['runtime'] == old.receipt()
    for group in current['groups']:
        assert bytes.fromhex(group['current_block_hex']) == new_bank[group['block']]
        assert group['current_block_sha256'] == sha(new_bank[group['block']])
    rebound = deepcopy(current)
    rebound.update(current_ROM=str(new.rompath), current_ROM_sha256=new.release['candidate_sha256'],
        current_archive_sha256=sha(new_archive), runtime=new.receipt(),
        exact_reuse_of_prior_native_catalogue_bindings=str(CURRENT197),
        exact_reuse_of_prior_native_catalogue_bindings_sha256=sha(CURRENT197.read_bytes()),
        dependency_qualification=str(qualification_path), dependency_qualification_sha256=sha(qualification_path.read_bytes()),
        original197_native_lookups_not_reexecuted=True, no_new_gameplay=True,
        rebinding_producer_sha256=sha(Path(__file__).read_bytes()))
    save(RUNTIME/'B61_B64_current197_exact_rebound_v1.json', rebound)
    save(sealed, dict(format='dk4-source-first-logical-English-drafts-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', file_path='/data/SC0.DK4', blocks=list(range(65,81)), records=rows,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        constituent_drafts={str(p):sha(p.read_bytes()) for p in draft_paths},
        earlier197_comparisons_disclosed_andnot_part_of_this342_exposure_gate=True,
        all_fifth_formatting_gates_pending=True, new_credit=0, guide_photos=False))
    packet_path = ROOT/'clean_source_packet.json'
    packet = load(packet_path)
    subset = deepcopy(packet)
    subset['groups'] = [g for g in packet['groups'] if g['block'] in range(65,81)]
    subset.update(records=342, selected_from=str(packet_path), selected_from_sha256=sha(packet_path.read_bytes()))
    save(selected, subset)
    meanings = [deepcopy(r) for r in identity['records'] if r['block'] in range(65,81)]
    assert len(meanings) == 342
    for row in meanings:
        row['current_ROM_English_unconsulted'] = True
    save(target, dict(source_packet=str(selected), source_packet_sha256=sha(selected.read_bytes()),
        records=meanings, meanings=342, all_drafts_sealed=str(sealed), all_drafts_sha256=sha(sealed.read_bytes()),
        no_blanket_prior_English_exposure_claim=True, complete_gloss=str(identity_path),
        complete_gloss_sha256=sha(identity_path.read_bytes()),
        prior197_already_compared_andnot_in_this_source_selection=True,
        latest_runtime_dependency_qualification=str(qualification_path),
        latest_runtime_dependency_qualification_sha256=sha(qualification_path.read_bytes()),
        new_credit=0, guide_photos=False, producer_sha256=sha(Path(__file__).read_bytes())))
    save(all539, dict(format='dk4-individually-source-first-draft-assembly-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', records=prior197['records']+rows, logical_drafts_saved=539,
        constituent_drafts={str(p):sha(p.read_bytes()) for p in [prior197_path]+draft_paths},
        each_constituent_sealed_before_its_own_current_English_extraction=True,
        prior197_current_English_already_compared_before_assembling_this_file=True,
        no_blanket_all539_still_unexposed_claim=True, B68_zero_speech_commands_preserved_in_source_packet=True,
        all_fifth_formatting_gates_pending=True, new_credit=0, guide_photos=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Latest eb62870b dependency reuse passes: 20 blocks/66 name fields/code/font/COMMON/events/actor array. All539 individually source-first drafts saved; remaining342 ready for current extraction.', flush=True)
