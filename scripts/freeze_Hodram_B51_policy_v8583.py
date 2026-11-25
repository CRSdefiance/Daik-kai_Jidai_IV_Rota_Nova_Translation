"""Freeze exact B51 prose, names, native controls and immutable compiler evidence."""
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Hodram_B51_v8562 as private
from scripts.approve_Hodram_B51_format_v8582 import PROOFS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_policy_v8583')
DOC = Path('translations/hodram_B51_editorial_manuscript_v5.json')
NAMES = Path('translations/hodram_B51_speaker_name_review_v2.json')
PLAN = private.ROOT / 'automatic_plans.json'
APPROVAL = Path('work/analysis/Hodram_B51_format_v8582b/formatting_approval.json')
CONTRACT = Path('translations/hodram_B51_native_contract_v1.json')
PROFILE = Path('dk4tool/dialogue/hodram_B51_profile_v1.py')
FORMATTER = Path('dk4tool/dialogue/hodram_B51_layout_v1.py')
PLANNER = Path('dk4tool/dialogue/hodram_B51_plan_v1.py')
NAME_POLICY = Path('dk4tool/dialogue/hodram_B51_names_v1.py')

if __name__ == '__main__':
    outputs = [CONTRACT, PROFILE, FORMATTER, PLANNER, NAME_POLICY]
    assert not ROOT.exists() and all(not path.exists() for path in outputs)
    doc, names, plan, approval = map(read, [DOC, NAMES, PLAN, APPROVAL])
    data = {key: read(path) for key, path in PROOFS.items()}
    group = data['relocation']['groups'][0]
    assert approval['manuscript_sha256'] == sha(DOC.read_bytes()) and approval['names_sha256'] == sha(NAMES.read_bytes()) and approval['all5_five_gates_true']
    assert len(doc['records']) == 5 and doc['typed_choice_objects'] == doc['source_FE_panels'] == 0 and doc['revised'] == 4 and doc['retained'] == 1
    assert all(all(row['review'].values()) for row in doc['records'] + names['records'])
    assert approval['actual_frames'] == 20002 and approval['complete_holds'] == 56 and approval['unvisited_conditional_text_IDs'] == ['DK4_MES_B51_R0032']
    assert group['block'] == 51 and len(group['all_target_commands']) == 20 and len(group['relative_fixups']) == 8
    assert data['reference']['only_changed_blocks'] == [51] and data['references']['external_references_complete']
    assert not plan['failures'] and len(plan['records']) == 5 and doc['source_current_final_references_complete']
    image = NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256']
    bindings, infos = {}, 0
    for row, p in zip(doc['records'], plan['records'], strict=True):
        assert row['id'] == p['id'] and row['english'] == row['logical_English'] == p['logical_English'] == ' '.join(p['lines'])
        assert row['compiled_hex'] == p['encoded_hex'] and row['planned_English_markup'] == p['planning_record']['english']
        assert p['expected_native_pages'] == 1 and p['max_total_rows'] == 4 and row['qa_waivers'] == row['qa_waiver_scope'] == []
        assert all(i['severity'] == 'info' and i['code'] == 'line-break-count' for i in p['base_QA']['issues'])
        infos += len(p['base_QA']['issues'])
        bindings[row['id']] = dict(file_path='/data/SC1.DK4', route=1, route_identity='Hodram', block=51,
            source_block_hashes=[group['clean_block_sha256'], group['source_block_sha256']], source_reference=row['source_reference'], current_reference=row['current_reference'],
            final_reference=row['final_reference'], source_complete_preamble_hex=row['source_complete_preamble_hex'], compiler_source_hex=row['source_hex'],
            predecessor_record_hex=row['current_hex'], source_selector=row['source_selector'], source_kind=row['kind'], consumer='progressive',
            planning_record={k: p['planning_record'][k] for k in ['id', 'english', 'kind', 'source_hex', 'source_selector']},
            compiled_hex=p['encoded_hex'], lines=p['lines'], maximum_total_rows=4, native_page_count=1,
            row_count_reason='Use the original full216px usable width and preserve every reviewed word on one complete native page.',
            ordinary_wrap_reasons=[row['localization_note'], row['native_body_review_reason']], base_QA_issues=p['base_QA']['issues'],
            qa_waivers=[], qa_waiver_reason=None, qa_waiver_scope=[], approved_fields=deepcopy(row))
    assert infos == 2 and {b['source_selector'] for b in bindings.values()} == {1, 16, 18, 113}
    templates = {key: Path(f'dk4tool/dialogue/hodram_B50_{key}_v2.py') for key in ['profile', 'layout', 'plan', 'names']}
    template = templates['profile'].read_text('utf-8')
    oldmetrics = template.split('metrics_source="', 1)[1].split('")', 1)[0]
    metrics = ('Exact registeredV8543/captain1 code/COMMON/font/whole actors and source71/01/12/10 six-byte preambles. '
        'Full216px usable width, five progressive native/stored singlepages, FI6/FA9/FO15, zero source macros, two line-count infos, zero warnings/waivers. '
        'Original twenty commands/eight relatives/two queries/four opaque controls/full end and fifty result-channel fragment cases are bound. '
        'Actual20002frames/two complete initialized entry fixtures show four speeches per language and56 complete body/name holds; Charles R32 is offline-tested and unvisited. '
        'Normal ends4736/4734 carry[0,0]; two one-frame duration differences, no measured boundary RNG/UI request differences, final seeds2294662370/3116913577 differ; three of89 laterRGB pairs differ. '
        'Five sampled components/whole actors/captain1 match; raw calendar remains uninterpreted. No natural activation, original location, earned inventory, custom names, fullroute, hardware, every-frame causality or future simulation equivalence claim.')
    profile = checked_text(template, {
        'translations/hodram_B50_native_contract_v2.json': CONTRACT.as_posix(),
        'd3474383619494eeba1e4f6c1c5d7a89bb73a83b3e2b8bdb8f0add24acaddce0': 'CONTRACT_DIGEST',
        'Hodram-B50': 'Hodram-B51', 'Hodram B50': 'Hodram B51',
        'len(d["record_bindings"])!=3': 'len(d["record_bindings"])!=5',
        'd["complete_native_pages"]!=3': 'd["complete_native_pages"]!=5',
        'three-paragraph/three-page': 'five-paragraph/five-page',
        'leading_speaker_bytes=frozenset({254} if wanted=="FE-paper" else {2})': 'leading_speaker_bytes=frozenset({r["source_selector"]})',
        oldmetrics: metrics,
    })
    layout = checked_text(templates['layout'].read_text('utf-8'), {
        'hodram_B50_profile_v2': 'hodram_B51_profile_v1', 'hodram_B50_plan_v2': 'hodram_B51_plan_v1', 'Hodram-B50': 'Hodram-B51'})
    planner = checked_text(templates['plan'].read_text('utf-8'), {
        'plan_Hodram_B50_v8491b': 'plan_Hodram_B51_v8562',
        'work/analysis/Hodram_B50_layout_v8491b/automatic_plans.json': PLAN.as_posix(),
        '2782f3c92071b4d485f8ea14e5d83eb8c4b190e28eed8f40fd7d9d0275cf787a': sha(PLAN.read_bytes()),
    })
    name_policy = checked_text(templates['names'].read_text('utf-8'), {
        'Exact scoped Lil identity': 'Exact four source-qualified identities', 'hodram_B50_profile_v2': 'hodram_B51_profile_v1', 'B50 names:': 'B51 names:',
        "[(r['actor_ID'],r['current']) for r in review['records']]!=[(2,'Lil Argot')]":
            "[(r['actor_ID'],r['speaker']) for r in review['records']]!=[(1,'Hodram Bergstrom'),(16,'Gerhard Adernkatz'),(18,'Charles Rochefort'),(113,'Port Worker')]",
        'exact scoped approved Lil identity required': 'exact four approved scoped identities required',
        "not review['no_FE_personal_actor_name']": "not review['no_new_name_asset_orall207_name_review_credit'] or review['scoped_actor_IDs']!=[1,16,18,113]",
        'original FE hasno personal actor254 name orvoice': 'exact scoped name preservation andno duplicate all207 credit required',
    })
    for path, text in [(PROFILE, profile.replace('CONTRACT_DIGEST', '0' * 64)), (FORMATTER, layout), (PLANNER, planner), (NAME_POLICY, name_policy)]:
        compile(text, str(path), 'exec')
    deps = {DOC, NAMES, PLAN, APPROVAL, Path(__file__), Path(private.__file__), *templates.values(), *map(Path, PROOFS.values())}
    for name, module in list(sys.modules.items()):
        if not (name.startswith('scripts.') or name.startswith('dk4tool.')):
            continue
        path = getattr(module, '__file__', None)
        if path and Path(path).suffix == '.py':
            deps.add(Path(path))
        for value in vars(module).values():
            if isinstance(value, Path) and value.suffix not in ['.nds', '.xdelta'] and value.is_file() and not any(s in value.as_posix() for s in ['editorial_review_current_v1.json', 'release_stack.json', 'rom_retention_pins.json', 'docs/']):
                deps.add(value)
    for version in data['models']['native_models'].values():
        for row in version:
            for page in row['pages']:
                path = Path(page['native_plane'])
                assert sha(path.read_bytes()) == page['native_plane_sha256']
                deps.add(path)
    for row in data['models']['name_planes']:
        path = Path(row['native_plane'])
        assert sha(path.read_bytes()) == row['native_plane_sha256']
        deps.add(path)
    for sheet in data['whole_view']['directly_viewed_sheets']:
        path = Path(sheet['path'])
        assert sha(path.read_bytes()) == sheet['sha256']
        deps.add(path)
    for path, text in [(FORMATTER, layout), (PLANNER, planner), (NAME_POLICY, name_policy)]:
        path.write_text(text, encoding='utf-8')
        deps.add(path)
    normalized = {path.resolve() for path in deps if path.resolve() != Path('scripts/build_integrated_release.py').resolve()}
    assert all(path.is_file() for path in normalized)
    runtime = {p: sha(image.read_file(p)) for p in ['/__arm9__.bin', '/COMMON/MESFILE.DK4', '/GRP/KANJI.FNT', '/data/EV1.DK4']}
    save(CONTRACT, dict(format='Hodram-B51-source-native-contract-v1', record_bindings=bindings, choice_bindings={}, review_gates=doc['review_gates'],
        batch_binding={k: doc[k] for k in ['translation_policy', 'target_locale', 'encoder', 'review_gates', 'file_path', 'route', 'route_identity', 'blocks']},
        runtime_component_hashes=runtime, measured_macro_ascii_lengths=dict(FI=6, FA=9, FO=15), source_macro_counts=dict(FI=0, FA=0, FO=0),
        physical_native_rows_per_page=4, physical_progressive_viewport=[216, 64], usable_text_width_px=216, complete_native_pages=5,
        source_control_binding=dict(commands=20, complete_preambles=5, relatives=8, queries=2, opaque_controls=4, source_FE_panels=0,
            exact_original_source_commands=data['source_controls']['all_original_source_commands'], exact_relative_fixups=group['relative_fixups']),
        name_review_binding=names, explicit_complete_registered_predecessor=dict(profile='all-routes-unified-v8543', candidate=doc['current_ROM'],
            candidate_sha256=doc['current_ROM_sha256'], ARM9_sha256=runtime['/__arm9__.bin'],
            Gerhard_correction='translations/gerhard_surname_editorial_release_v2.json', B49_correction='translations/hodram_B49_editorial_release_v4.json',
            B50_correction='translations/hodram_B50_editorial_release_v1.json'),
        dependencies={str(path): sha(path.read_bytes()) for path in sorted(normalized)}, individual_row_count_infos=2, exact_warning_exception_count=0,
        exact_source_current_final_context_prose_names_native_stored_representative_actual_andmeasured_scope_bound=True,
        observed_actual_speech_IDs=approval['observed_speech_IDs'], unvisited_conditional_text_IDs=['DK4_MES_B51_R0032'],
        policy_validation_independent_production_atomic_registered_integration_pending=True, new_credit=0, full_goal_complete=False))
    PROFILE.write_text(profile.replace('CONTRACT_DIGEST', sha(CONTRACT.read_bytes())), encoding='utf-8')
    ROOT.mkdir(parents=True)
    save(ROOT / 'frozen_contract.json', dict(contract=str(CONTRACT), contract_sha256=sha(CONTRACT.read_bytes()), manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()),
        modules={str(p): sha(p.read_bytes()) for p in [PROFILE, FORMATTER, PLANNER, NAME_POLICY]}, records=5, typed_choices=0, single_pages=5, scoped_names=4,
        source_FE=0, source_macro_counts=dict(FI=0, FA=0, FO=0), infos=2, warnings=0, waivers=0, dependency_count=len(normalized),
        integrated_builder_not_accidentally_pinned=True, source_locked_templates={str(p): sha(p.read_bytes()) for p in templates.values()},
        all_native_high_integer_constants_preserved_in_each_derived_module=True, all_prior_artifacts_preserved_no_global_profile_font_QA_guard_orprose_change=True,
        new_credit=0, full_goal_complete=False))
    print(f'Frozen B51: five pages, four scoped names, two infos, zero warnings/waivers; {len(normalized)} immutable dependencies. Policy validation and production/atomic/registered integration pending; zero credit.')
