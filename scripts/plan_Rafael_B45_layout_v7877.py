"""Keep native selector00 in its preamble; ordinary NUL-free body formatter retains its full guard."""
import inspect
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Rafael_B45_layout_v7875b as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_layout_v7877')
MANUSCRIPT=Path('translations/rafael_B45_editorial_manuscript_v2.json')
LOGICAL=Path('work/analysis/Rafael_B45_logical_refined_v7876b/12_refined_logical_bindings44_reused4_fresh_alignments.json')
ADAPTER=checked_text(previous.ADAPTER,{
    "    def formatted(text,p):assert text==row['english'] and p==profile;return markup\n    encode=FunctionType(encoder.encode_relocatable_dialogue.__code__,{**encoder.encode_relocatable_dialogue.__globals__,'format_markup':formatted},argdefs=encoder.encode_relocatable_dialogue.__defaults__);encoded=encode(bytes.fromhex(row['source_hex']),row['english'],profile)":
    """    source_raw=bytes.fromhex(row['source_hex']);zero=row['source_selector']==0
    assert source_raw[0]==row['source_selector'] and b'\\0' not in source_raw[1:]
    if zero:
        assert row['kind']=='progressive' and prefix=='{SPEAKER:00}' and source_raw in BOUND_ZERO_SOURCE_BODIES
        body_profile=replace(profile,leading_speaker_bytes=frozenset())
        def formatted(text,p):
            assert text==body and p==body_profile
            return markup.removeprefix('{SPEAKER:00}')
    else:
        body_profile=profile
        def formatted(text,p):
            assert text==row['english'] and p==profile
            return markup
    encode=FunctionType(encoder.encode_relocatable_dialogue.__code__,{**encoder.encode_relocatable_dialogue.__globals__,'format_markup':formatted},argdefs=encoder.encode_relocatable_dialogue.__defaults__)
    temporary=encode(source_raw[1:] if zero else source_raw,body if zero else row['english'],body_profile)
    assert b'\\0' not in temporary.encoded
    encoded=replace(temporary,formatted_markup=markup,encoded=b'\\0'+temporary.encoded) if zero else temporary""",
    "if not final and False and (norm(words[stop-1]),norm(words[stop]))==('papal','states'):continue":
    """if not final and (norm(words[stop-1]),norm(words[stop]))==("governor's",'office'):continue""",
})
CURRENT=Path('work/analysis/Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json')
bound=read(CURRENT)
BOUND_ZERO_SOURCE_BODIES=frozenset(bytes.fromhex(r['source_hex']) for r in bound['records'] if r['source_selector']==0)
assert len(BOUND_ZERO_SOURCE_BODIES)==4
ENV={**previous.ENV,'BOUND_ZERO_SOURCE_BODIES':BOUND_ZERO_SOURCE_BODIES}
exec(compile(ADAPTER,__file__+'::source-bound-zero-preamble-separate-body-formatter','exec'),ENV)
plan=ENV['plan']
if __name__=='__main__':
    assert not ROOT.exists();doc,logical=map(read,[MANUSCRIPT,LOGICAL])
    assert logical['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and logical['total_bound_alignment_cases']==48
    rows=[];failures=[]
    for row in doc['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row);body=row['english']
            for token in ['FI','FA','FO']:body=body.replace(token,'{MACRO:'+token+'}')
            planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body
            p=plan(planning);assert ' '.join(p['lines'])==body
            encoded=bytes.fromhex(p['encoded_hex'])
            assert encoded[0]==row['source_selector'] and b'\0' not in encoded[1:]
            p.update(file_path=doc['file_path'],block=row['block'],source_record_index=row['source_record_index'],
                source_selector=row['source_selector'],kind=row['kind'],logical_English=row['english'],planning_record=planning,
                base_QA=previous.base_qa(planning,p),original_consumer_width_px=228 if row['kind']=='system-FE' else 216,
                source00_actor_byte_owned_by_native_preamble_not_NUL_body_formatter=row['source_selector']==0)
            rows.append(p)
        except (ValueError,AssertionError) as exc:
            failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True);save(ROOT/'12_automatic_plans_full_native_width_zero_preamble_separate_body.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),
        records=rows,failures=failures,source_owned_plan_adapter=ADAPTER,
        original_body_encoder_NUL_rejection_preserved_without_exception=True,exact_four_clean00_records_only=True,
        source_current_packet=str(CURRENT),source_current_packet_sha256=sha(CURRENT.read_bytes()),
        source_owned_measured_profile=inspect.getsource(previous.get_profile),
        source_word_boundary_pairs=sorted(ENV['PAIRS']),Governor_Office_natural_name_unit_kept_together=True,
        progressive_viewport=[216,64],FE_logical_viewport=[228,48],FE_physical_viewport=[228,64],
        full_original_consumer_widths_no_global_font_profile_guard_orweak_rule_change=True,
        no_manual_break_padding_alignment_orprose_abbreviation_authored=True,
        all_original_QA_issues_preserved_no_waivers=True,all12_formatting_gates_remain_false=True,
        native_fonts_bounds_pagination_controls_stored_actual_andrelease_pending=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,LOGICAL,CURRENT,Path(previous.__file__),Path(__file__)]},full_goal_complete=False))
    for r in rows:print(r['id'],r['lines'],r['line_lengths'],'QA',[(i['code'],i['severity']) for i in r['base_QA']['issues']])
    print('FAILURES',failures)
    if failures:raise SystemExit(1)
