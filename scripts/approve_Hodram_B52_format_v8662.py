"""Approve source-bound B52 display formats with actual and offline limits explicit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.review_Hodram_B52_actual_v8659 import PROOFS as ACTUAL_PROOFS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B52_format_v8662')
OLD = Path('translations/hodram_B52_editorial_manuscript_v4.json')
DOC = Path('translations/hodram_B52_editorial_manuscript_v5.json')
OLD_NAMES = Path('translations/hodram_B52_speaker_name_review_v2.json')
NAMES = Path('translations/hodram_B52_speaker_name_review_v3.json')
PROOFS = {**ACTUAL_PROOFS,
    'actual_review': 'work/analysis/Hodram_B52_actual_review_v8659/qualified_actual_review.json',
    'source_controls': 'work/analysis/Hodram_B52_source_controls_v8620/source_controls.json',
    'source_VM': 'work/analysis/Hodram_B52_source_choice_VM_v8628b/source_menu_provider_andresponse_paths.json',
    'logical': 'work/analysis/Hodram_B52_logical_v8633/logical_paragraphs.json',
    'plan': 'work/analysis/Hodram_B52_layout_v8634/automatic_plans.json',
    'pages': 'work/analysis/Hodram_B52_pages_v8635/compiled_native_pages.json',
    'native_menu': 'work/analysis/Hodram_B52_menu_v8636/menu_provider_and_planes.json',
    'relocation': 'work/analysis/Hodram_B52_relocation_v8642/reconstruction.json',
    'complete_references': 'work/analysis/Hodram_B52_references_v8647/references.json'}

if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists()
    old, names = map(read, [OLD, OLD_NAMES])
    data = {key: read(path) for key, path in PROOFS.items()}
    review = data['actual_review']
    assert review['manuscript']['sha256'] == sha(OLD.read_bytes()) and review['names']['sha256'] == sha(OLD_NAMES.read_bytes())
    assert (review['total_runs'], review['total_frames'], review['total_holds']) == (6, 50406, 138)
    assert review['no_actual_owner_pointer_RAM_VRAM_palette_orunowned_backing_identity_claim']
    assert review['long_withdrawal_later_component_actor_calendar_PRNG_and46_RGB_differences_preserved']
    assert data['stored']['all3_speech_full_first_internal_final_glyphs_bounds_consumption_single_page_andviewed_ink_checks_pass']
    assert data['stored']['compiler_tail_creates_no_blank_oradditional_page'] and data['stored']['whole_current_inmemory_ROM_inverse_byte_exact']
    assert data['relocation']['other324_blocks_byte_exact'] and data['complete_references']['external_references_complete']
    assert len(data['stored']['distinct_seeded_ends']) == 50 and len(data['stored']['stored_dispatches']) == 3
    assert data['native_menu']['even_alignment_provider_cases'] == 4 and data['native_menu']['bridged_modal_return_cases'] == 12
    assert data['menu']['actual_menu_samples'] == 12 and data['menu']['complete_actual_caption_glyph_andbackground_checks'] == 24
    assert not data['plan']['failures']
    issues = [i for row in data['plan']['records'] for i in row['base_QA']['issues']]
    assert len(issues) == 1 and all(i['severity'] == 'info' and i['code'] == 'line-break-count' for i in issues)
    doc, ng = deepcopy(old), deepcopy(names)
    for field, stored_field in [('records', 'records'), ('typed_choice_records', 'typed_choice_records')]:
        refs = {r['id']: r for r in data['stored'][stored_field]}
        for row in doc[field]:
            assert all(row['review'][g] is True for g in ['source', 'context', 'localization', 'naturalness']) and row['review']['formatting'] is False
            ref = refs[row['id']]
            assert row['source_reference'] == ref['source_reference'] and row['current_reference'] == ref['current_reference'] and row['stored_final_reference'] == ref['final_reference']
            row['final_reference'] = deepcopy(ref['final_reference'])
            row['final_hex'] = row['stored_hex'] = ref['stored_hex']
            if field == 'records':
                assert row['compiled_hex'] == ref['compiled_hex']
                row['compiler_owned_parity_space'] = ref['compiler_owned_parity_space']
                reason = row['native_body_review_reason'] + ' Complete stored first/internal/final glyphs, original six-byte preamble, automatic full216px wrapping, exact consumption/bounds/single-page pagination and source/current/final references pass. Both actual initialized Japanese/English selected paths show this speech with its full Port Worker nameplate and portrait. Two compiler-owned stored tails are independently tested; the byte-identical first body explicitly reuses its existing native proof. No authored ordinary breaks, extra page, font/metric change or waiver.'
            else:
                assert row['compiled_choice_label_hex'] == ref['stored_hex']
                reason = row['native_choice_review_reason'] + ' Complete Japanese/English captions, constructor-derived centering and bounds, selected/unselected visible backgrounds and ordinary A/Down selections are verified in existing paired captures. Native two-option count/order/offsets and both distinct response/end kinds remain. Original offline backing bounds are separate; no live RAM/VRAM/palette/backing identity or cancel availability is claimed.'
            row['formatting_approval_reason'] = reason
            row['review']['formatting'] = True
            row['formatting_registered_release_pending'] = True
            row['current_review_status'] = 'all-five-individual-gates-reviewed-policy-validation-production-atomic-registered-pending'
    assert ng['scoped_actor_IDs'] == [113] and ng['mentioned_actor_IDs'] == [34]
    for row in ng['records'] + ng['mentioned_components']:
        assert row['review']['formatting'] is False
        row['review']['formatting'] = True
        row['formatting_approval_scope'] = ('Exact actor113 Port Worker nameplate and portrait in B52 only; complete original/current fields and 138 observed body/name holds. No new name asset or wider-context credit.' if row['actor_ID'] == 113 else 'Hayreddin literal surname component in the complete B52 question; exact approved source/current component and observed complete English body glyphs. No actual actor34 header, full name, catalogue or relationship invention.')
    ng.update(predecessor=dict(path=str(OLD_NAMES), sha256=sha(OLD_NAMES.read_bytes())),
              all207_names_roles_aliases_customnames_andwider_Port_Worker_contexts_still_open=True,
              all_individual_scoped_five_gates_true=True, new_credit=0, full_goal_complete=False)
    ROOT.mkdir(parents=True)
    save(NAMES, ng)
    doc.update(predecessor_manuscript=str(OLD), predecessor_manuscript_sha256=sha(OLD.read_bytes()),
               names_packet=str(NAMES), names_packet_sha256=sha(NAMES.read_bytes()),
               all_four_prose_gates_true_all_formatting_gates_false=False,
               all_five_formatting_gates_still_false=False, all_five_individual_five_gates_true=True,
               source_current_final_references_complete=True,
               reference_ROM=data['reference']['research_ROM'], reference_ROM_sha256=data['reference']['research_ROM_sha256'],
               formatting_evidence={k: dict(path=p, sha256=sha(Path(p).read_bytes())) for k, p in PROOFS.items()},
               measured_limits=deepcopy(review),
               status='all-five-individual-gates-reviewed-policy-validation-production-atomic-registered-pending',
               remaining_required_work='Frozen source-qualified compiler/native policy, genuinely changed-input tests, independent production evidence readers, one whole-NDS atomic commit, registered cumulative release/exact clean patch/own startup, then exactly five once-only completion decisions.',
               no_new_ROM_orregistered_stage_orcompletion_credit=True, new_credit=0, full_goal_complete=False)
    for field in ['records', 'typed_choice_records']:
        for before, after in zip(old[field], doc[field], strict=True):
            for key in ['id', 'english', 'logical_English', 'source_hex', 'source_reference', 'current_hex', 'current_reference', 'decision', 'finding', 'retention_reason']:
                assert before[key] == after[key]
    validate_natural_dialogue_batch(doc)
    validate_natural_dialogue_batch({**doc, 'records': doc['typed_choice_records']})
    save(DOC, doc)
    save(ROOT / 'formatting_approval.json', dict(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()),
         names=str(NAMES), names_sha256=sha(NAMES.read_bytes()), speech_approvals=3, typed_choice_approvals=2,
         scoped_role_approvals=1, mentioned_component_approvals=1, all5_five_gates_true=True,
         all_source_current_final_references_bound=True, all_words_compiled_bytes_source_current_refs_unchanged=True,
         infos=1, warnings=0, waivers=0, measured_limits=review,
         standard_natural_dialogue_v2_speech_andchoice_validation_pass=True,
         policy_validation_production_atomic_registered_patch_startup_credit_pending=True,
         new_native_runs=0, new_emulator_runs=0, new_credit=0, full_goal_complete=False,
         evidence={str(p): sha(Path(p).read_bytes()) for p in [OLD, OLD_NAMES, *PROOFS.values(), __file__]}))
    print('B52 all5 individual formatting gates approved:3 speech pages/2 typed choices, scoped Port Worker/Hayreddin component; exact words/bytes/refs. All actual limits preserved; policy/registered integration pending, zero credit.')
