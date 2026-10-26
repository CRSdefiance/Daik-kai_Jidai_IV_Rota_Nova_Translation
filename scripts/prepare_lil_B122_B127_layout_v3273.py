"""Create a source-bound successor planner and plan 155 speeches/four labels."""
from copy import deepcopy
from pathlib import Path
import importlib
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B122_B127_layout_v3273')
SOURCE=Path('work/analysis/lil_B122_B127_source_v3260c/complete159_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_B122_B127_controls_v3266/all155_source_current_dispatch_FE_null_actor_and14_predicates.json')
VOICE=Path('work/analysis/lil_B122_B127_voices_v3264/current_eight_static_names_voices_and207_catalog_rebind.json')
WAIT=Path('work/analysis/lil_B122_original2000_waits_v3265/original2000_actual_rule_and_current_source_binding.json')
TERMS=Path('work/analysis/lil_B122_B127_terms_v3267/clean_current_items_Spirit_static_actors_and_related_terms.json')
CATALOG=Path('work/analysis/lil_B122_B127_controls_v3266/current_registered_name_catalog_binding.json')
PROFILE=Path('dk4tool/dialogue/lil_B122_B127_profile.py')
FORMATTER=Path('dk4tool/dialogue/lil_B122_B127_layout_v1.py')
OLD=Path('dk4tool/dialogue/lil_B111_B119_layout_v2.py')
INPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v1.json'),Path('translations/lil_B122_B127_choice_manuscript_v1.json')]
OUTPUTS=[Path(str(p).replace('_v1.json','_v2.json')) for p in INPUTS]

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,PROFILE,FORMATTER,*OUTPUTS])
    source=read(SOURCE);deps={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,VOICE,WAIT,TERMS,CATALOG]}
    hashes=sorted({r[k] for r in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    text='''"""Six exact clean/current blocks; static actors, FE and original UI pauses."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_REPLACE
BLOCKS=frozenset(BLOCK_REPLACE)
SELECTORS=frozenset({2,6,9,20,26,92,95,151})
DEPENDENCIES=DEP_REPLACE
CONTROL=Path(CONTROL_REPLACE)
VOICE=Path(VOICE_REPLACE)
WAIT=Path(WAIT_REPLACE)

def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('B122-B127 requires exact six clean/current blocks and runtime')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B122-B127 source contract changed:'+path)
    control=json.loads(CONTROL.read_text(encoding='utf-8'))
    voice=json.loads(VOICE.read_text(encoding='utf-8'))
    wait=json.loads(WAIT.read_text(encoding='utf-8'))
    if (len(control['speech_dispatch_cases'])!=310 or len(control['current_original_predicate_cases'])!=14
        or control['original_event_queries'] or control['source_macro_counts']!={'FI':12,'FA':0,'FO':0}
        or not control['all20_FE_cases_dispatch5473C_and24310_null_actor_before_dynamic_fallback']
        or len(voice['fresh_eight_actor_names'])!=8
        or not voice['source_97_is_static_retainer151_not_dynamic_D0_fallback']
        or not wait['current_zero_argument_wait_contract_bound_by_exact_original_code_and_actual_Lil_pause_evidence']):
        raise ValueError('Complete original speech/FE/actor/predicate/UI2000 source contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B122-B127-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';145 progressive static actor speeches. Static97 is Retainer151. No dynamic selector or4100 body. Preserve original2000 pauses and2100 choices separately.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B122-B127-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';10 unlabeled FE panels;original24310 null actor before5473C/fallback208.228x48 logical/228x64 physical paper;conservative216px planning. Seven Japanese leading-LF staging cases are not authored English blank rows. No invented name/caption;source FI exact.')
    raise ValueError('Unknown B122-B127 consumer')
'''
    for old,new in [('ARM_REPLACE',repr(source['current_ARM9_sha256'])),('BLOCK_REPLACE',repr(hashes)),('DEP_REPLACE',repr(deps)),('CONTROL_REPLACE',repr(str(CONTROL))),('VOICE_REPLACE',repr(str(VOICE))),('WAIT_REPLACE',repr(str(WAIT)))]:
        assert old in text;text=text.replace(old,new)
    compile(text,str(PROFILE),'exec');PROFILE.write_text(text,encoding='utf-8')
    text=OLD.read_text(encoding='utf-8').replace('B111-B119','B122-B127')
    old="frozenset({2,4,9,14,19,20,104,137,163,170,179,198,207,208,209,214,215,220})"
    assert old in text;text=text.replace(old,'frozenset({2,6,9,20,26,92,95,151})')
    old="PROTECTED_BOUNDARIES=frozenset({";assert old in text
    text=text.replace(old,"PROTECTED_BOUNDARIES=frozenset({('guiding','staff'),('snow-silk','robe'),('old','maid'),")
    compile(text,str(FORMATTER),'exec');FORMATTER.write_text(text,encoding='utf-8')
    profile_for=importlib.import_module('dk4tool.dialogue.lil_B122_B127_profile').profile_for
    planner=importlib.import_module('dk4tool.dialogue.lil_B122_B127_layout_v1')
    image=NdsImage.open(source['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    docs=[deepcopy(read(p)) for p in INPUTS];reports=[];failures=[];notes=[]
    for doc in docs:
        for row in doc['records']:
            if row['kind']=='typed-choice-label':
                value=row['english'].encode('ascii');assert value and value.strip()==value and len(value)<=36 and all(32<=c<127 for c in value)
                row['compiled_hex']=value.hex();reports.append(dict(id=row['id'],kind=row['kind'],label_hex=value.hex(),selection_geometry_native_gates_pending=True));continue
            raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[row['block']],'FE-paper' if row['kind']=='system-FE' else 'progressive')
            try:
                result=planner.encode_relocatable_dialogue(raw,row['english'],profile)
                qa=planner.audit_relocatable_dialogue_record(raw,row['english'],profile)
            except (ValueError,AssertionError) as error:
                failures.append(dict(id=row['id'],error=str(error),english=row['english']));continue
            warnings=[d.code for d in result.diagnostics if d.severity=='warning']
            if 'line-break-count' in warnings:
                reason='Source Japanese wrapping and leading FE staging are not English dramatic breaks. Complete meaning and punctuation remain in one logical paragraph;the calibrated formatter owns balanced pair-safe wrapping. Only row-count differences are accepted. No orphan,weak-ending,glyph,bounds,pagination,control,macro,choice orblank-page exemption is granted.'
                row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);row['localization_note']+=' '+reason;notes.append(dict(id=row['id'],reason=reason))
            issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]))]
            unwaived=[v for v in warnings if v not in row.get('qa_waivers',[])]
            if issues or unwaived:failures.append(dict(id=row['id'],issues=issues,unwaived=unwaived,english=row['english']))
            row['compiled_hex']=result.encoded.hex()
            reports.append(dict(id=row['id'],kind=row['kind'],encoded_hex=result.encoded.hex(),formatted_markup=result.formatted_markup,qa=qa,encoder_warning_codes=warnings))
    ROOT.mkdir(parents=True);proof=ROOT/'all159_paragraph_and_label_layout_QA.json'
    save(proof,dict(manuscripts={str(p):sha(p.read_bytes()) for p in INPUTS},scoped_profile=str(PROFILE),scoped_profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),previous_formatter=str(OLD),previous_formatter_sha256=sha(OLD.read_bytes()),records=reports,failures=failures,row_count_notes=notes,formatting_approval_not_granted=True,no_ROM_registry_ledger_or_editorial_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    if failures:
        print(dict(plans=len(reports),notes=len(notes),unresolved=failures),flush=True);raise SystemExit(1)
    assert len(reports)==159
    for doc,old,new in zip(docs,INPUTS,OUTPUTS,strict=True):
        doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),dialogue_profile='lil-opening-editorial-native-v1',scoped_profile_module=str(PROFILE),scoped_profile_module_sha256=sha(PROFILE.read_bytes()),native_formatter_module=str(FORMATTER),native_formatter_module_sha256=sha(FORMATTER.read_bytes()),layout_QA_proof=str(proof),layout_QA_proof_sha256=sha(proof.read_bytes()),status='source-prose-layout-planned;native-font-choice-reference-release-pending')
        save(new,doc)
    print(dict(plans=159,row_count_notes=len(notes),unresolved=0,credit=0),flush=True)
