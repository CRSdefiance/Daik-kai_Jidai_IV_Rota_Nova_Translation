"""Freeze B52 whole-exchange prose, typed choices, original native controls and evidence."""
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Hodram_B52_v8634 as private
from scripts.approve_Hodram_B52_format_v8662b import PROOFS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B52_policy_v8663')
DOC = Path('translations/hodram_B52_editorial_manuscript_v6.json')
NAMES = Path('translations/hodram_B52_speaker_name_review_v4.json')
PLAN = private.ROOT / 'automatic_plans.json'
APPROVAL = Path('work/analysis/Hodram_B52_format_v8662b/formatting_approval.json')
CONTRACT = Path('translations/hodram_B52_native_contract_v1.json')
BASE = Path('dk4tool/dialogue')
OUTPUTS = {name: BASE / ('hodram_B52_' + name + '_v1.py') for name in ['profile', 'layout', 'plan', 'names', 'choices']}

if __name__ == '__main__':
    assert not ROOT.exists() and not CONTRACT.exists() and all(not p.exists() for p in OUTPUTS.values())
    doc, names, plan, approval = map(read, [DOC, NAMES, PLAN, APPROVAL])
    data = {key: read(path) for key, path in PROOFS.items()}
    assert approval['all5_five_gates_true'] and approval['manuscript_sha256'] == sha(DOC.read_bytes()) and approval['names_sha256'] == sha(NAMES.read_bytes())
    assert len(doc['records']) == 3 and len(doc['typed_choice_records']) == 2 and doc['revised'] == 2 and doc['retained'] == 3
    assert all(all(row['review'].values()) for row in doc['records'] + doc['typed_choice_records'] + names['records'] + names['mentioned_components'])
    group = data['relocation']['groups'][0]
    assert group['block'] == 52 and len(group['all_target_commands']) == 14 and len(group['relative_fixups']) == 4
    assert group['source_bytes'] == 228 and group['target_bytes'] == 236 and group['target_tail_bytes'] == 0
    assert data['complete_references']['external_references_complete'] and data['reference']['only_changed_blocks'] == [52]
    bindings = {}
    infos = 0
    for row, p in zip(doc['records'], plan['records'], strict=True):
        assert row['id'] == p['id'] and row['english'] == row['logical_English'] == p['logical_English'] == ' '.join(p['lines'])
        assert row['compiled_hex'] == p['encoded_hex'] and row['planned_English_markup'] == p['planning_record']['english']
        assert p['expected_native_pages'] == 1 and p['max_total_rows'] == 4 and row['qa_waivers'] == row['qa_waiver_scope'] == []
        assert all(i['severity'] == 'info' and i['code'] == 'line-break-count' for i in p['base_QA']['issues'])
        infos += len(p['base_QA']['issues'])
        bindings[row['id']] = dict(file_path='/data/SC1.DK4', route=1, route_identity='Hodram', block=52,
            source_block_hashes=[group['clean_block_sha256'], group['source_block_sha256']],
            source_reference=row['source_reference'], current_reference=row['current_reference'], final_reference=row['final_reference'],
            source_complete_preamble_hex=row['source_complete_preamble_hex'], compiler_source_hex=row['source_hex'],
            predecessor_record_hex=row['current_hex'], source_selector=row['source_selector'], source_kind=row['kind'], consumer='progressive',
            planning_record={k: p['planning_record'][k] for k in ['id', 'english', 'kind', 'source_hex', 'source_selector']},
            compiled_hex=p['encoded_hex'], stored_hex=row['stored_hex'], compiler_owned_parity_space=row['compiler_owned_parity_space'],
            lines=p['lines'], maximum_total_rows=4, native_page_count=1,
            row_count_reason='Use the full original216px width; preserve every reviewed word on one complete native page.',
            ordinary_wrap_reasons=[row['localization_note'], row['native_body_review_reason']], base_QA_issues=p['base_QA']['issues'],
            qa_waivers=[], qa_waiver_reason=None, qa_waiver_scope=[], approved_fields=deepcopy(row))
    assert infos == 1 and {b['source_selector'] for b in bindings.values()} == {113}
    choice_bindings = {r['id']: dict(approved_fields=deepcopy(r), source_reference=r['source_reference'],
                       current_reference=r['current_reference'], final_reference=r['final_reference'], stored_hex=r['stored_hex'])
                       for r in doc['typed_choice_records']}
    assert [r['option_index'] for r in doc['typed_choice_records']] == [0, 1]
    choice_raw = Path(doc['typed_choice_records'][0]['compiled_choice_object']).read_bytes()
    assert len(choice_raw) == 32 and sha(choice_raw) == doc['typed_choice_records'][0]['compiled_choice_object_sha256']
    templates = {name: BASE / ('hodram_B49_' + name + '_v2.py') for name in ['profile', 'choices']}
    templates.update({name: BASE / ('hodram_B51_' + name + '_v1.py') for name in ['layout', 'plan', 'names']})
    texts = {}
    template = templates['profile'].read_text(encoding='utf-8')
    oldmetrics = template.split('metrics_source="', 1)[1].split('")', 1)[0]
    metrics = ('Exact registeredV8609/captain1 runtime, original actor113 six-byte preambles and FI6/FA9/FO15 with zero source macros. '
        'Full216px width, three complete progressive/stored singlepages, one original line-count info, zero warnings/waivers; no authored ordinary breaks. '
        'Fourteen commands/four relatives/zero queries/four opaque controls, two typed choices and distinct preserving/clearing ends are bound. '
        'Six initialized cold boots50406frames/138complete body-name holds/12page occurrences cover all3speeches and both ordinary choices/end kinds. '
        'Twelve actual menus/24captions prove visible glyphs/centering/highlights; backing bounds remain offline, no new live owner/RAM/VRAM/palette/backing identity. '
        'Long withdrawal differs in components/actors/calendar/PRNG and46of93RGBpairs; long opposition matches components/actors but differs inPRNG/13of93RGBpairs. '
        'Focused withdrawal exact input prefix ends after4484: sampled components/actors/seed/calendar and13RGBpairs match, with no following commands. '
        'Preserve all command/menu timing and later differences; no causal explanation, future simulation equivalence, natural event activation/location/earned progress, actual cancel availability, fullroute orhardware claim.')
    texts['profile'] = checked_text(template, {
        'translations/hodram_B49_native_contract_v2.json': CONTRACT.as_posix(),
        '320692ec559ec574dcefd755acdfa918d4ec811809e9159f461dccadec34d422': 'CONTRACT_DIGEST',
        'Hodram-B49': 'Hodram-B52', 'Hodram B49': 'Hodram B52',
        'len(d["record_bindings"])!=14': 'len(d["record_bindings"])!=3',
        'd["complete_native_pages"]!=14': 'd["complete_native_pages"]!=3',
        'Complete14-speech/14-page/two-choice': 'Complete3-speech/3-page/two-choice', oldmetrics: metrics,
    })
    texts['layout'] = checked_text(templates['layout'].read_text(encoding='utf-8'), {
        'hodram_B51_profile_v1': 'hodram_B52_profile_v1', 'hodram_B51_plan_v1': 'hodram_B52_plan_v1', 'Hodram-B51': 'Hodram-B52'})
    texts['plan'] = checked_text(templates['plan'].read_text(encoding='utf-8'), {
        'plan_Hodram_B51_v8562': 'plan_Hodram_B52_v8634',
        'work/analysis/Hodram_B51_layout_v8562/automatic_plans.json': PLAN.as_posix(),
        '3e4e9f12b6d2fb7c5bc8a99ce772b9d15c6a3bc70ac7d1d205a883d0562af24b': sha(PLAN.read_bytes()),
    })
    texts['choices'] = checked_text(templates['choices'].read_text(encoding='utf-8'), {
        'hodram_B49_profile_v2': 'hodram_B52_profile_v1', 'Hodram-B49': 'Hodram-B52'})
    texts['names'] = checked_text(templates['names'].read_text(encoding='utf-8'), {
        'Exact four source-qualified identities': 'Exact actor113 role andmentioned actor34 component',
        'hodram_B51_profile_v1': 'hodram_B52_profile_v1', 'B51 names:': 'B52 names:',
        "[(1,'Hodram Bergstrom'),(16,'Gerhard Adernkatz'),(18,'Charles Rochefort'),(113,'Port Worker')]": "[(113,'Port Worker')]",
        'exact four approved scoped identities required': 'exact scoped Port Worker identity required',
        "for row in review['records']:": "for row in review['records']+review['mentioned_components']:",
        "review['scoped_actor_IDs']!=[1,16,18,113]": "review['scoped_actor_IDs']!=[113] or review['mentioned_actor_IDs']!=[34] or [(r['actor_ID'],r['english']) for r in review['mentioned_components']]!=[(34,'Hayreddin')] or not review['no_actor34_actual_header_catalogue_orfull_name_review_claim']",
    })
    for name, text in texts.items():
        compile(text.replace('CONTRACT_DIGEST', '0' * 64), str(OUTPUTS[name]), 'exec')
    image = NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256']
    deps = {DOC, NAMES, PLAN, APPROVAL, Path(__file__), Path(private.__file__), *templates.values(), *map(Path, PROOFS.values())}
    for packet in [*data.values(), approval]:
        for path, digest in packet.get('evidence', {}).items():
            if isinstance(digest, str) and len(digest) == 64:
                assert sha(Path(path).read_bytes()) == digest, path
                deps.add(Path(path))
    for name, module in list(sys.modules.items()):
        if not (name.startswith('scripts.') or name.startswith('dk4tool.')):
            continue
        path = getattr(module, '__file__', None)
        if path and Path(path).suffix == '.py':
            deps.add(Path(path))
        for value in vars(module).values():
            if isinstance(value, Path) and value.suffix not in ['.nds', '.xdelta'] and value.is_file() and not any(s in value.as_posix() for s in ['editorial_review_current_v1.json', 'release_stack.json', 'rom_retention_pins.json', 'docs/']):
                deps.add(value)
    for sheet in data['actual_review']['directly_viewed_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
        deps.add(Path(sheet['path']))
    for name in ['layout', 'plan', 'names', 'choices']:
        OUTPUTS[name].write_text(texts[name], encoding='utf-8')
        deps.add(OUTPUTS[name])
    normalized = {p.resolve() for p in deps if p.resolve() != Path('scripts/build_integrated_release.py').resolve()}
    assert all(p.is_file() for p in normalized)
    runtime = {p: sha(image.read_file(p)) for p in ['/__arm9__.bin', '/COMMON/MESFILE.DK4', '/GRP/KANJI.FNT', '/data/EV1.DK4']}
    save(CONTRACT, dict(format='Hodram-B52-source-native-contract-v1', record_bindings=bindings, choice_bindings=choice_bindings,
        choice_object_hex=choice_raw.hex(), review_gates=doc['review_gates'],
        batch_binding={k: doc[k] for k in ['translation_policy', 'target_locale', 'encoder', 'review_gates', 'file_path', 'route', 'route_identity', 'blocks']},
        runtime_component_hashes=runtime, measured_macro_ascii_lengths=dict(FI=6, FA=9, FO=15), source_macro_counts=dict(FI=0, FA=0, FO=0),
        physical_native_rows_per_page=4, physical_progressive_viewport=[216, 64], usable_text_width_px=216, complete_native_pages=3,
        source_control_binding=dict(commands=14, complete_preambles=3, relatives=4, queries=0, opaque_controls=4, source_FE_panels=0,
             exact_original_source_commands=data['source_controls']['all_original_source_commands'],
             exact_relative_fixups=group['relative_fixups'], distinct_source_end_hex=['00000000', '00000080']),
        name_review_binding=names, explicit_complete_registered_predecessor=dict(profile='all-routes-unified-v8609',
             candidate=doc['current_ROM'], candidate_sha256=doc['current_ROM_sha256'], ARM9_sha256=runtime['/__arm9__.bin']),
        dependencies={str(p): sha(p.read_bytes()) for p in sorted(normalized)},
        individual_row_count_infos=1, exact_warning_exception_count=0,
        source_current_final_prose_names_controls_native_stored_actual_andall_measured_limits_bound=True,
        observed_actual_speech_IDs=data['actual_review']['unique_speeches'], unvisited_conditional_text_IDs=[],
        measured_limits=deepcopy(data['actual_review']),
        policy_validation_production_atomic_registered_integration_pending=True, new_credit=0, full_goal_complete=False))
    OUTPUTS['profile'].write_text(texts['profile'].replace('CONTRACT_DIGEST', sha(CONTRACT.read_bytes())), encoding='utf-8')
    ROOT.mkdir(parents=True)
    save(ROOT / 'frozen_contract.json', dict(contract=str(CONTRACT), contract_sha256=sha(CONTRACT.read_bytes()),
        manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), modules={str(p): sha(p.read_bytes()) for p in OUTPUTS.values()},
        records=3, typed_choices=2, single_pages=3, scoped_names=1, mentioned_name_components=1, infos=1, warnings=0, waivers=0,
        dependency_count=len(normalized), integrated_builder_not_accidentally_pinned=True,
        source_locked_templates={str(p): sha(p.read_bytes()) for p in templates.values()},
        all_native_high_integer_constants_preserved_in_each_derived_module=True,
        all_prior_artifacts_global_profile_font_QA_guards_andprose_unchanged=True,
        new_credit=0, full_goal_complete=False))
    print('Frozen B52:3 speech pages/2 choices, Port Worker/Hayreddin scoped component;', len(normalized), 'dependencies. One info, no warning/waiver. Policy/production/atomic/registered pending; zero credit.')
