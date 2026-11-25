"""Approve the exact Stockholm map and successor prose without repeating gameplay."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.lil_stockholm_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Stockholm_approval_v1873')
OLD = 'translations/lil_Stockholm_encounter_editorial_manuscript_v2.json'
NEW = 'translations/lil_Stockholm_encounter_editorial_manuscript_v3.json'
MAP = 'translations/lil_stockholm_editorial_relocation_map_v1.json'
SOURCE = 'work/analysis/lil_Stockholm_source_v1848b/all51_clean_current_native_source_context.json'
RELOC = 'work/analysis/lil_Stockholm_relocation_v1861/nested_source_relocation_research.json'
CENSUS = 'work/analysis/lil_Stockholm_reference_census_v1866/all102_commands24_relative_sites_and_shipped_entry_census.json'
ACTUAL = 'work/analysis/lil_Stockholm_revised_audit_v1867c/revised_Stockholm36_branch_and_three_fixture_audit.json'

if __name__ == '__main__':
    assert not ROOT.exists() and not Path(NEW).exists() and not Path(MAP).exists()
    doc, packet, relocation, census, actual = map(read, (OLD, SOURCE, RELOC, CENSUS, ACTUAL))
    block = relocation['blocks'][0]
    assert len(doc['records']) == 51 and sum(r['editorial_decision']=='revise' for r in doc['records']) == 38
    assert len(census['mapped_commands']) == 102 and len(block['relative_skip_fixups']) == 24
    assert census['all102_commands_reexecuted_clean_current_and_target']
    assert census['all24_typed_span_sites_and120_target_native_cases_preserve_destinations']
    assert census['all_original_opaque_commands_and_complete_speech_preambles_preserved']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert census['only_original24070_interpreter_call_no_literal_alias']
    assert actual['all36_activated_revised_speeches72_holds_complete_native_independent_actual_glyphs']
    assert actual['same75_original_commands_results_and_event_transitions']
    assert actual['normal_discovery_docking_B27_entry_and_terminal_return_not_injected']
    assert actual['all_inputs_capture_hashes4MiB_snapshots_and_three_coordinate_footprints_verified']
    assert actual['all_readonly_observer_boundaries_and_host_restoration_pass']
    observed = {r['id'] for r in actual['revised_speech_observations']}
    unseen = set(actual['unvisited_original_speech_IDs'])
    assert len(observed) == 36 and len(unseen) == 15 and not observed & unseen
    assert observed | unseen == {r['id'] for r in doc['records']}
    files = {OLD, SOURCE, RELOC, CENSUS, ACTUAL, doc['native_font_proof'], doc['visual_review'],
             doc['scoped_control_proof'], doc['scoped_profile_module'], __file__}
    # Verify inherited proof dependencies, rather than treating old approvals as
    # permission to use changed evidence. This does not rerun finished emulator work.
    pending = list(files)
    checked = set()
    while pending:
        name = pending.pop()
        if name in checked:
            continue
        checked.add(name)
        p = Path(name)
        assert p.exists(), name
        if p.suffix != '.json':
            continue
        data = read(p)
        if not isinstance(data, dict):
            continue
        for dep, digest in data.get('evidence', {}).items():
            assert sha(Path(dep).read_bytes()) == digest, dep
            files.add(dep)
            pending.append(dep)
    fonts = read(doc['native_font_proof'])
    for sheet in read(doc['visual_review'])['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
        files.add(sheet['path'])
    for row in fonts['cases']:
        files.add(row['preview'])
    files.update(actual['contact_sheets'])
    parent = NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256']
    original = IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks[27]
    profile = profile_for(parent.read_file('/__arm9__.bin'), original)
    by_id = {r['id']:r for r in block['text_records']}
    successor = deepcopy(doc)
    successor.update(encoder='dialogue-relocatable-v1', status='approved-for-guarded-registered-integration',
        predecessor_manuscript=OLD, predecessor_manuscript_sha256=sha(Path(OLD).read_bytes()),
        actual_visual_review=ACTUAL, actual_visual_review_sha256=sha(Path(ACTUAL).read_bytes()),
        approved_reference_map=MAP, fixed_encoder_is_allocation_probe_only_until_complete_reference_map=False,
        scope='All51 contextual Japanese-source/prose/native reviews;36 actual speeches72 holds,15 conditional speeches offline. Final registered ROM and startup/patch gates pending.')
    for row in successor['records']:
        row['english'] = row['english'].removesuffix('{PAD}')
        encoded = encode_relocatable_dialogue(bytes.fromhex(row['source_hex']), row['english'], profile).encoded
        assert encoded.hex() == row['compiled_hex']
        ref = by_id[row['id']]
        if ref['parity_space_added']:
            encoded += b' '
        assert encoded.hex() == ref['target_hex']
        row['context'] = ('Lil SC2B27 Stockholm encounter. Complete51-speech clean Japanese exchange and conditional Gerhard conversation reread with speakers,relationships,situation and emotional progression. Lil confronts Hodram;Camille returns to apologize;Hodram recognizes his ability. '+
            ('This exact revised speech has two actual native-independent-pixel holds in V1867c.' if row['id'] in observed else
             'This conditional speech was not individually activated;all native/font/macro checks pass. Gerhard0x10 is source/runtime scoped and proven by original Hodram control gameplay.'))
        row['contextual_review_v1873'] = dict(source_and_entire_exchange_reread=True,
            wording_retained_from_reviewed_v2=True, reason=row['localization_note'],
            individually_observed_in_revised_gameplay=row['id'] in observed)
    validate_natural_dialogue_batch(successor)
    mapping = dict(format='dk4-lil-stockholm-source-relocation-map-v1', block=27,
        source_block_sha256=block['source_block_sha256'], clean_block_sha256=packet['clean_block_sha256'],
        target_block_sha256=block['research_block_sha256'], entry_point_offset=8,
        external_references_complete=True, preserve_record_parity=True,
        all102_original_commands_and24_typed_spans_approved=True,
        representative_actual36_and_offline51_scope_approved=True,
        records=block['text_records'], commands=census['mapped_commands'],
        relative_skip_fixups=block['relative_skip_fixups'],
        actual_record_IDs=sorted(observed), offline_only_conditional_record_IDs=sorted(unseen),
        conditional_risk_assessment='No distinct unresolved presentation risk:all51 exact native/font/macros,all102 native commands,24 typed spans120 relocated cases,whole loader,scoped Gerhard selector with actual portrait/name/dismissal proof.15 conditions do not require individual visits under V1870.',
        evidence={p:sha(Path(p).read_bytes()) for p in sorted(files)},
        approval_does_not_claim_registered_ROM_or_complete_route_playthrough=True)
    ROOT.mkdir(parents=True)
    save(NEW, successor)
    save(MAP, mapping)
    save(ROOT/'source_context_and_final_map_approval.json', dict(
        manuscript=NEW, manuscript_sha256=sha(Path(NEW).read_bytes()),
        reference_map=MAP, reference_map_sha256=sha(Path(MAP).read_bytes()),
        all51_Japanese_speeches_reread_as_complete_exchange=True,
        approved_revisions=38, justified_retentions=13,
        no_prose_changes_from_native_and_actual_tested_v2=True,
        inherited_visual_and_actual_evidence_verified_by_hash=True,
        prior_visual_approvals_inherited_not_new_image_view_claims=True,
        actual_speeches=36, offline_only_conditional_speeches=15,
        no_repeated_emulator_test_no_ROM_no_completion_credit=True, full_goal_complete=False))
    print({'approved_records':51,'actual':36,'offline_conditional':15,'map':MAP})
