"""Freeze the measured nine paragraphs and two typed menus; no formatting/release approval."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_policy_tools_v6618');DOC=Path('translations/lil_B212_editorial_manuscript_v2.json');PLAN=Path('work/analysis/lil_B212_layout_v6608/nine_whole_paragraph_research_plans.json');FONT=Path('work/analysis/lil_B212_question_native_v6609/all9_complete_pages72_alignments8_fresh64_exact_reused.json');MENU=Path('work/analysis/lil_B212_choice_planes_v6607b/all5_labels20_style_planes_complete_and_native_widths.json');VIEW=Path('work/analysis/lil_B212_native_view_v6610/nine_current_pages_full_question_and_five_menu_labels_viewed.json');QA=Path('work/analysis/lil_B212_base_QA_v6613/all9_base_QA_diagnostics_before_any_scoped_classification.json');CONTROL=Path('work/analysis/lil_B212_controls_v6603b/two_three_choices21_return_cases_four_paths_two_effect_pairs_and30_guarded_ends.json');CONTRACT=Path('translations/lil_B212_native_contract_v1.json');PROFILE=Path('dk4tool/dialogue/lil_B212_profile_v1.py');FORMATTER=Path('dk4tool/dialogue/lil_B212_layout_v1.py')
REASONS={32:'The full pleased greeting and favorite-general question use two complete English rows rather than three Japanese rows. The short question is intact on row2; no Japanese staging pause, word loss, extra page or authored wrap.',54:'All107 English characters preserve Changban Bridge, Adou held to the chest, the lone ride, Cao Cao\'s army and enthusiasm. Four guarded rows are required by the complete words; Cao Cao\'s army stays together. Same original216x64 four-row page, without font/window change or fit-driven omission.',58:'All104 English characters retain both rumor qualifications, legendary spear, unspecified nearby peninsula and Zhao Yun attribution. Four guarded rows are required by complete words and pair phase. Same original four-row page; no definite location, shortening or extra page.',78:'All129 English characters retain the consistent Zhuge Liang identity, brilliant strategist description, named memorial, tears and approximate second preference. Four guarded rows preserve every word. The source Kongming alias remains documented; the ordinary Before/the title boundary does not alter source meaning, glyphs or page safety.'}
PROFILE_CODE='''"""Exact B212 source/paragraph/native geometry contract; typed menus remain distinct."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B212_native_contract_v1.json')
CONTRACT_SHA='@HASH@'
ARM9_SHA='aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B212 frozen native contract changed')
    d=json.loads(raw)
    for p,h in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=h:raise ValueError('B212 native dependency changed:'+p)
    if len(d['record_bindings'])!=9 or len(d['choice_bindings'])!=2 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=9:raise ValueError('Complete B212 nine-paragraph/two-menu contract required')
    return d
def expected_profile(ident):
    d=contract()
    if ident not in d['record_bindings']:raise ValueError('Unreviewed B212 paragraph')
    r=d['record_bindings'][ident];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B212-source-bound-v1:'+ident,max_lines=4,leading_speaker_bytes=frozenset({149}),metrics_source=base.metrics_source+'; B212 exact paragraph '+ident+'. Original216x64/four-row page,6px ASCII,16px pitch,original pair phase and guards; actor149 voice0, no FE/macro/role reinterpretation.')
def profile_for(arm,block,ident):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(block) not in d['source_block_hashes']:raise ValueError('Exact B212 source/current block and AA5 runtime required')
    return expected_profile(ident)
'''
FORMATTER_CODE='''"""Frozen B212 automatic paragraphs and original2/3-option table encoding."""
import struct
from copy import deepcopy
from types import FunctionType
from dk4tool.dialogue import qa
from dk4tool.dialogue.encoder import RelocatableDialogueEncoding
from dk4tool.dialogue.layout import DialogueDiagnostic
from dk4tool.dialogue.lil_B212_profile_v1 import contract,expected_profile
from scripts.plan_lil_B212_layout_v6608 import plan as frozen_plan
def binding(raw,text,profile):
    prefix='lil-B212-source-bound-v1:'
    if not profile.name.startswith(prefix):raise ValueError('Exact per-record B212 profile required')
    ident=profile.name[len(prefix):];d=contract()
    if ident not in d['record_bindings'] or profile!=expected_profile(ident):raise ValueError('B212 font/window/page/selector/guard/macro profile changed')
    r=d['record_bindings'][ident]
    if raw.hex()!=r['compiler_source_hex'] or text!=r['planning_record']['english'] or any(v in text for v in ['{LB','{ALIGN','{PAD','\\n','\\r']):raise ValueError('Exact B212 complete source and reviewed logical paragraph required')
    return ident,r
def encode_relocatable_dialogue(raw,text,profile):
    ident,r=binding(raw,text,profile);p=frozen_plan(deepcopy(r['planning_record']))
    if p['encoded_hex']!=r['compiled_hex'] or p['lines']!=r['lines']:raise ValueError('Frozen B212 native paragraph changed')
    return RelocatableDialogueEncoding(p['formatted_markup'],bytes.fromhex(p['encoded_hex']),tuple(DialogueDiagnostic(**v) for v in p['diagnostics']))
_audit=FunctionType(qa.audit_relocatable_dialogue_record.__code__,{**qa.audit_relocatable_dialogue_record.__globals__,'encode_relocatable_dialogue':encode_relocatable_dialogue},argdefs=qa.audit_relocatable_dialogue_record.__defaults__)
def audit_relocatable_dialogue_record(raw,text,profile):
    ident,r=binding(raw,text,profile);report=_audit(raw,text,profile)
    if any(i['severity'] in ['error','warning'] for i in report['issues']):raise ValueError('Unwaived B212 base QA issue')
    report.update(native_rows_per_page=4,native_page_count=1,row_count_reason=r['row_count_reason'],reviewed_ordinary_boundaries=r['ordinary_wrap_reasons'],no_base_QA_issue_removed=True)
    return report
def compile_choice(raw,offset,rows):
    d=contract();key=str(offset)
    if key not in d['choice_bindings']:raise ValueError('Unreviewed B212 menu offset')
    b=d['choice_bindings'][key]
    if raw.hex() not in [b['source_command_hex'],b['current_command_hex']] or len(rows)!=b['count']:raise ValueError('Exact complete B212 choice object/count required')
    if [(r['id'],r['option_index'],r['english']) for r in rows]!=[(r['id'],r['option_index'],r['english']) for r in b['records']]:raise ValueError('Exact B212 source order, identity and wording required')
    offsets=[];chunks=[];cursor=0
    for r in rows:
        value=r['english'].encode('ascii')
        if not value or value.strip()!=value or any(v<32 or v>=127 for v in value):raise ValueError('Plain complete B212 choice label required')
        offsets.append(cursor);part=value+b'\\0';part+=bytes(-len(part)%2);chunks.append(part);cursor+=len(part)
    target=struct.pack('<'+'H'*(b['count']+1),b['word'],*offsets)+b''.join(chunks)
    if target.hex()!=b['target_hex']:raise ValueError('Frozen B212 native table, labels or parity changed')
    return target
'''
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER]);doc,plan,font,menu,view,qa,control=map(read,[DOC,PLAN,FONT,MENU,VIEW,QA,CONTROL]);sourcepath=Path(doc['source_context']);source=read(sourcepath);assert plan['manuscript_sha256']==font['manuscript_sha256']==sha(DOC.read_bytes()) and font['layout_plan_sha256']==sha(PLAN.read_bytes()) and len(font['records'])==9 and menu['complete_current_and_reviewed_label_style_planes']==20 and view['font_proof_sha256']==sha(FONT.read_bytes()) and all(not r['review']['formatting'] for r in doc['records']);native={r['id']:r for r in font['records']};plans={r['id']:r for r in plan['records']};bindings={};different=[]
    for row in doc['records']:
        if row['kind']!='progressive':continue
        r=plans[row['id']];assert row['source_selector']==149 and r['encoded_hex']==native[row['id']]['compiled_hex'] and len(native[row['id']]['pages'])==1;index=row['source_record_index'];diff=bytes.fromhex(row['source_hex']).count(b'\n')!=len(r['lines'])-1;assert diff==(index in REASONS)
        if diff:different.append(index)
        ordinary=[]
        if index==72:ordinary.append(dict(after_word='Magnificent',before_word='Beard?',reason='Unavoidable complete-word soft wrap within the literary epithet keeps all94 characters in three rows rather than an unnecessary fourth; no rank or word change.'))
        if index==78:ordinary.append(dict(after_word='Before',before_word='the',reason='Complete-word soft wrap within the named memorial preserves all129 characters in the original four-row page; no glyph, bounds or pagination waiver.'))
        bindings[row['id']]=dict(source_selector=149,source_kind='progressive',source_reference=row['source_reference'],current_reference=row['current_reference'],compiler_source_hex=row['source_hex'],planning_record={k:row[k] for k in ['id','english','kind','source_hex','source_selector']},compiled_hex=r['encoded_hex'],lines=r['lines'],maximum_total_rows=4,native_page_count=1,row_count_reason=REASONS.get(index),ordinary_wrap_reasons=ordinary)
    assert different==[32,54,58,78];choices={}
    for m in control['menus']:
        offset=m['command_offset'];s=next(v for v in source['blocks'][0]['choices'] if v['command_offset']==offset);rows=sorted([r for r in doc['records'] if r.get('command_offset')==offset],key=lambda r:r['option_index']);assert [r['english'] for r in rows]==m['versions'][-1]['labels'];choices[str(offset)]=dict(word=m['word'],count=m['count'],source_command_hex=s['source_command']['whole_command_hex'],current_command_hex=s['current_command']['whole_command_hex'],target_hex=m['target_object_hex'],records=[{k:r[k] for k in ['id','option_index','english','source_reference','current_reference','source_hex','current_hex']} for r in rows])
    assert len(bindings)==9 and sum(c['count'] for c in choices.values())==5 and not [i for r in qa['records'] for i in r['base_QA']['issues'] if i['severity'] in ['error','warning']]
    deps=[DOC,PLAN,FONT,MENU,VIEW,QA,CONTROL,sourcepath,Path(doc['current_consumer_proof']),Path(doc['speaker_name_review']),Path(doc['current_strict_native_input']),Path('scripts/plan_lil_B212_layout_v6608.py'),Path('scripts/Al_Ferid_exact_native_context_v6520.py'),Path('scripts/Al_Ferid_font_oracles_v6520.py'),Path(__file__),*[Path('dk4tool/dialogue')/n for n in ['profiles.py','codec.py','encoder.py','layout.py','qa.py','review.py']]]
    save(CONTRACT,dict(format='B212-current-native-source-contract-v1',source_block_hashes=[source['blocks'][0]['clean_block_sha256'],source['blocks'][0]['current_block_sha256']],physical_native_rows_per_page=4,physical_viewport=[216,64],complete_native_pages=9,record_bindings=bindings,choice_bindings=choices,dependencies={str(p):sha(p.read_bytes()) for p in deps},no_base_QA_issue_removed_or_warning_waiver=True,four_individual_rowcount_reasons=True,all14_formatting_approval_actual_reference_and_release_still_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False));profile=PROFILE_CODE.replace('@HASH@',sha(CONTRACT.read_bytes()));compile(profile,str(PROFILE),'exec');compile(FORMATTER_CODE,str(FORMATTER),'exec');PROFILE.write_text(profile,'utf-8');FORMATTER.write_text(FORMATTER_CODE,'utf-8');ROOT.mkdir(parents=True);save(ROOT/'prepared_native_policy.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),nine_positive_paragraph_five_choice_label_cases_and_meaningful_rejections_pending=True,no_ROM_registry_ledger_formatting_approval_or_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Exact B212 nine-paragraph/two-menu native policy prepared; four rowcount reasons, zero removed QA issues. Positive/rejection checks next; no release approval.')
