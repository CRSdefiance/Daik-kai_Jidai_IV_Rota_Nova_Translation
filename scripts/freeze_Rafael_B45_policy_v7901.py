"""Freeze twelve approved logical paragraphs and the exact automatic, zero-safe native planner."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_policy_v7901')
DOC=Path('translations/rafael_B45_editorial_manuscript_v4.json')
NAMES=Path('translations/rafael_B45_speaker_name_review_v2.json')
PLAN=Path('work/analysis/Rafael_B45_layout_v7881b/12_automatic_plans_full_native_width_zero_preamble_separate_body.json')
CURRENT=Path('work/analysis/Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json')
NATIVE=Path('work/analysis/Rafael_B45_native_review_v7883/12_exact_native_pages_rebound_with_individual_row_review.json')
APPROVAL=Path('work/analysis/Rafael_B45_actual_approval_v7898/12_source_context_native_actual_format_approved_policy_release_pending.json')
CONTRACT=Path('translations/rafael_B45_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/rafael_B45_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/rafael_B45_layout_v1.py')
PLANNER=Path('dk4tool/dialogue/rafael_B45_plan_v1.py')
PROFILE_SOURCE='''"""Exact Rafael B45 clean/current records, original progressive/FE consumers and measured runtime."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path("CONTRACT_PATH")
CONTRACT_SHA="CONTRACT_DIGEST"
ARM9_SHA="2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a"
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError("Frozen Rafael-B45 contract changed")
    d=json.loads(raw)
    for p,h in d["dependencies"].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)
    if len(d["record_bindings"])!=12 or d["choice_bindings"] or d["physical_native_rows_per_page"]!=4 or d["complete_native_pages"]!=12:
        raise ValueError("Complete twelve-paragraph/no-menu contract required")
    if d["measured_macro_ascii_lengths"]!={"FI":6,"FA":6,"FO":10} or d["source_macro_counts"]!={"FI":0,"FA":0,"FO":1}:
        raise ValueError("Exact measured Rafael macros required")
    return d
def expected_profile(ident,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Rafael-B45 paragraph")
    r=d["record_bindings"][ident];wanted="FE-paper" if r["source_selector"]==254 else "progressive"
    if consumer is not None and consumer!=wanted:raise ValueError("Original Rafael-B45 consumer required")
    base=get_dialogue_profile("raphael-story-live")
    if base.window_width_px!=216 or base.max_lines!=4 or base.macro_ascii_lengths["FI"]!=7 or base.literal_prefix_policy!="forbid":
        raise ValueError("Original global Rafael profile required")
    return replace(base,name="Rafael-B45-source-bound-v1:"+ident,max_lines=4,
        macro_widths={"FI":36,"FA":36,"FO":60,"I":12},macro_ascii_lengths={"FI":6,"FA":6,"FO":10},
        leading_speaker_bytes=frozenset({254} if wanted=="FE-paper" else {0,6}),
        literal_prefix_policy="native-guard-v255",
        metrics_source="Exact B45/current2b6:216px usable text/four physical rows;original progressive216x64 or FE228x48 logical/228x64 physical. Source00 actor stays in complete native preamble;body NUL guard unchanged. Native FI6/FA6/FO10,complete compiled/stored planes andpaired actual masks verified. No global font,profile,guard orweak-rule change. One-step RNG timing difference retained;future random outcomes not proved equal.")
def profile_for(arm,block,ident,file_path,consumer=None):
    d=contract()
    if ident not in d["record_bindings"]:raise ValueError("Unreviewed Rafael-B45 paragraph")
    r=d["record_bindings"][ident]
    if sha(arm)!=ARM9_SHA or file_path!=r["file_path"] or sha(block) not in r["source_block_hashes"]:
        raise ValueError("Exact file-qualified B45 source/current block and2b6 runtime required")
    return expected_profile(ident,consumer)
def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():
        if sha(image.read_file(path))!=digest:raise ValueError("Exact Rafael-B45 runtime component required:"+path)
    return d
'''
FORMATTER_SOURCE='''"""Exact approved B45 prose; deterministic automatic wrapping and unchanged base QA."""
from copy import deepcopy
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.rafael_B45_profile_v1 import contract,expected_profile
from dk4tool.dialogue.rafael_B45_plan_v1 import plan as frozen_plan
def binding(raw,text,profile):
    prefix="Rafael-B45-source-bound-v1:"
    if not profile.name.startswith(prefix):raise ValueError("Exact per-record Rafael-B45 profile required")
    ident=profile.name[len(prefix):];d=contract()
    if ident not in d["record_bindings"] or profile!=expected_profile(ident):
        raise ValueError("Rafael-B45 font/window/page/selector/guard/macro profile changed")
    r=d["record_bindings"][ident]
    if not isinstance(raw,bytes) or raw.hex()!=r["compiler_source_hex"] or text!=r["planning_record"]["english"] or any(v in text for v in ["{LB","{ALIGN","{PAD","\\n","\\r"]):
        raise ValueError("Exact Rafael-B45 complete source and reviewed logical paragraph required")
    return ident,r
def encode_relocatable_dialogue(raw,text,profile):
    ident,r=binding(raw,text,profile);p=frozen_plan(deepcopy(r["planning_record"]))
    if p["encoded_hex"]!=r["compiled_hex"] or p["lines"]!=r["lines"]:
        raise ValueError("Frozen Rafael-B45 native paragraph changed")
    encoded=bytes.fromhex(p["encoded_hex"])
    if encoded[0]!=r["source_selector"] or b"\\0" in encoded[1:]:
        raise ValueError("Complete original speaker preamble and NUL-free body required")
    return RelocatableDialogueEncoding(p["formatted_markup"],encoded,tuple(DialogueDiagnostic(**v) for v in p["diagnostics"]))
_audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,"encode_relocatable_dialogue":encode_relocatable_dialogue},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
def audit_relocatable_dialogue_record(raw,text,profile):
    ident,r=binding(raw,text,profile);report=_audit(raw,text,profile);issues=report["issues"]
    if issues!=r["base_QA_issues"] or any(i["severity"] in ["warning","error"] for i in issues):
        raise ValueError("Exact Rafael-B45 base QA diagnostics required without waivers")
    report.update(base_QA_issues=list(issues),all_original_base_QA_issues_preserved=True,
        native_rows_per_page=4,native_page_count=1,row_count_reason=r["row_count_reason"],
        reviewed_ordinary_boundaries=r["ordinary_wrap_reasons"],no_warning_removal_orwaivers=True,
        original_consumer=r["consumer"],source00_preamble_separate_from_body=r["source_selector"]==0)
    return report
'''
PLANNER_SOURCE='''"""Exact source-owned automatic B45 planner;00 preamble separate from guarded NUL-free text."""
from pathlib import Path
from scripts.plan_Rafael_B45_layout_v7881b import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("PLAN_PATH")
PLAN_SHA="PLAN_DIGEST"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["source_word_boundary_pairs"]}
exec(compile(read(PLAN)["source_owned_plan_adapter"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
'''
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER,PLANNER])
    doc,names,plan,current,native,approval=map(read,[DOC,NAMES,PLAN,CURRENT,NATIVE,APPROVAL])
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes())
    assert native['plan_sha256']==sha(PLAN.read_bytes()) and not plan['failures']
    assert approval['all24_complete_actual_pages90_complete_holds84_progressive_headers6_FE_absent_headers']
    assert approval['source_whole_exchange_situation_voice_andall_individual_retentions_rechecked_against_actual_panes']
    assert len(approval['directly_viewed_sheets'])==7 and all(s['directly_viewed'] for s in approval['directly_viewed_sheets'])
    image=NdsImage.open(current['current_ROM']);assert sha(Path(current['current_ROM']).read_bytes())==current['current_ROM_sha256']
    bindings={};deps={DOC,NAMES,PLAN,CURRENT,NATIVE,APPROVAL,Path(__file__)}
    for key in ['actual_proof','comparison','RNG_measurement']:
        path=Path(approval[key]);assert sha(path.read_bytes())==approval[key+'_sha256'];deps.add(path)
    for row,p,n in zip(doc['records'],plan['records'],native['records'],strict=True):
        assert row['id']==p['id']==n['id'] and row['english']==p['planning_record']['english']
        assert row['source_hex']==p['source_hex'] and row['compiled_hex']==p['encoded_hex']==n['compiled_hex']
        assert all(row['review'][g] for g in ['source','context','localization','naturalness','formatting'])
        assert len(n['pages'])==p['expected_native_pages']==1 and not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        group=current['groups'][0];source=next(r for r in group['records'] if r['id']==row['id'])
        assert source['source_hex']==row['source_hex'] and source['current_hex']==row['current_hex']
        row_info=any(i['code']=='line-break-count' for i in p['base_QA']['issues'])
        bindings[row['id']]=dict(file_path=row['file_path'],route=0,route_identity='Rafael',block=45,
            source_block_hashes=[group['clean_block_sha256'],group['current_block_sha256']],
            source_header_hex=group['source_header_hex'],current_header_hex=group['current_header_hex'],
            source_reference=row['source_reference'],current_reference=row['current_reference'],
            source_complete_preamble_hex=row['source_complete_preamble_hex'],compiler_source_hex=row['source_hex'],
            predecessor_record_hex=row['current_hex'],source_selector=row['source_selector'],source_kind=row['kind'],
            consumer='FE-paper' if row['source_selector']==254 else 'progressive',
            planning_record={k:p['planning_record'][k] for k in ['id','english','kind','source_hex','source_selector']},
            compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=4,native_page_count=1,
            row_count_reason=row['automatic_row_review'] if row_info else None,
            ordinary_wrap_reasons=[row['automatic_row_review']],base_QA_issues=p['base_QA']['issues'])
        deps.update(Path(pg['native_plane']) for pg in n['pages'])
    assert len(bindings)==12 and sum(b['source_selector']==0 for b in bindings.values())==4
    assert sum(b['source_selector']==254 for b in bindings.values())==1
    row_infos=sum(bool(b['row_count_reason']) for b in bindings.values());assert row_infos==6
    for name in ['profiles.py','codec.py','encoder.py','layout.py','qa.py','review.py']:deps.add(Path('dk4tool/dialogue')/name)
    for name in ['plan_Rafael_B45_layout_v7881b.py','plan_Rafael_B45_layout_v7875b.py',
                 'plan_lil_B234_layout_v7586d.py','plan_lil_B214_layout_v6705b.py','source_locked_derivation_v5118.py']:
        deps.add(Path('scripts')/name)
    for path in [
        'work/analysis/Rafael_B45_FE_boundary_v7880/32_FE_terminal_andbreak_pair_boundary_measurements.json',
        'work/analysis/Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json',
        'work/analysis/Rafael_B45_stored_v7885/all12_stored_bodies28_fresh20_reused_alignments_exact_viewed_planes.json',
        'work/analysis/Rafael_B45_relocated_controls_v7886/12_stored_dispatches25_relocated_relative_cases_predicate25_seeded_ends.json',
        'work/analysis/Rafael_B45_relocation_v7884/one_block12_speeches5_relative_fixups25_cases_exact_full_inverse.json',
        'work/analysis/Rafael_B45_loaders_v7888/343_whole_native_loads_cache_hits686_initial_parent_modes.json',
        'work/analysis/Rafael_B45_reference_census_v7889/all24_commands_five_relative_sites_EV0_entry_shipped_callers.json',
    ]:deps.add(Path(path))
    planner=PLANNER_SOURCE.replace('PLAN_PATH',PLAN.as_posix()).replace('PLAN_DIGEST',sha(PLAN.read_bytes()))
    profile=PROFILE_SOURCE.replace('CONTRACT_PATH',CONTRACT.as_posix())
    for path,text in [(PLANNER,planner),(PROFILE,profile.replace('CONTRACT_DIGEST','0'*64)),(FORMATTER,FORMATTER_SOURCE)]:compile(text,str(path),'exec')
    PLANNER.write_text(planner,encoding='utf8');deps.add(PLANNER)
    runtime={p:sha(image.read_file(p)) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV0.DK4']}
    save(CONTRACT,dict(format='Rafael-B45-source-native-contract-v1',record_bindings=bindings,choice_bindings={},
        source_block_hashes=current['groups'][0]['clean_block_sha256:current_block_sha256'] if False else
            [current['groups'][0]['clean_block_sha256'],current['groups'][0]['current_block_sha256']],
        runtime_component_hashes=runtime,measured_macro_ascii_lengths=dict(FI=6,FA=6,FO=10),source_macro_counts=dict(FI=0,FA=0,FO=1),
        physical_native_rows_per_page=4,physical_progressive_viewport=[216,64],FE_logical_bitmap=[228,48],FE_physical_bitmap=[228,64],
        usable_text_width_px=216,complete_native_pages=12,dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)},
        all12_source_context_native_stored_andactual_checks_bound=True,
        all_original_base_QA_issues_preserved_no_warning_removal_orwaivers=True,individual_row_count_infos=row_infos,
        exact_original_source00_preambles_andbody_NUL_rejection_preserved=True,
        source_English_RNG_one_step_difference_retained_future_outcome_equality_unproved=True,
        frozen_policy_validation_atomic_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    PROFILE.write_text(profile.replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),encoding='utf8')
    FORMATTER.write_text(FORMATTER_SOURCE,encoding='utf8');ROOT.mkdir(parents=True)
    save(ROOT/'prepared12_exact_native_policy.json',dict(
        contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),
        formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),planner=str(PLANNER),planner_sha256=sha(PLANNER.read_bytes()),
        records=12,row_count_infos=row_infos,zero_warning_waivers=True,
        exact_original_planner_andbody_encoder_guards_preserved=True,source00_andFE_consumers_scoped=True,
        all_five_per_record_gates_true_actual_andRNG_limits_bound=True,
        policy_challenges_atomic_production_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('Frozen B45 policy:12 exact paragraphs,six original row-count infos,no warnings/waivers;source00 body guard anddistinct FE216 usable/228bitmap preserved. Meaningful positives/negatives andatomic integration pending.')
