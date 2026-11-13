"""Freeze exact linear tobacco-scene progressive/FE native formatting contracts."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B192_native_tools_v5416')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B192_editorial_manuscript_v1.json');packet=read(doc['source_context'])
    keys=['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation','source_nameplate_consumer_proof']
    deps={doc[k]:doc[k+'_sha256'] for k in keys};hashes=sorted({b[k] for b in packet['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    profile=Path('dk4tool/dialogue/lil_B192_profile.py');assert not profile.exists()
    text='''"""Exact B192 two-actor linear progressive/FE native profile."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
'''
    text+='ARM9_SHA='+repr(packet['current_ARM9_sha256'])+'\nBLOCKS=frozenset('+repr(hashes)+')\nSELECTORS=frozenset({115,153})\nDEPENDENCIES='+repr(deps)+'\nCONTROL='+repr(doc['control_contract'])+'\n\n'
    text+='''def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('Exact B192 source/current block and runtime required')
    for path,digest in DEPENDENCIES.items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('B192 source contract changed:'+path)
    control=json.loads(Path(CONTROL).read_bytes());cases=control['speech_dispatch_cases']
    if len(cases)!=16 or sum(r['source_selector']==254 for r in cases)!=2:raise ValueError('All8 source/current dispatch pairs required')
    if any(r['resolved_actor_ID'] is not None for r in cases if r['source_selector']==254):raise ValueError('FE must remain null actor')
    if control['source_macro_counts']!={'FI':0,'FA':0,'FO':0}:raise ValueError('B192 has no source substitutions')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B192-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';7 original54020 speeches,PortWorker115 voice0/Sailor153 voice4,distinct catalogue Retainer153,four original read-only names. Hex73/99 equal decimal115/153.11 linear commands,A0008,C200396,end398,two source tailzeros. Current V5396 font/guards;fresh native approval required.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B192-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one original24310null actor then5473C:prospective Tobacco/Istanbul notice.228x48logical/228x64physical,conservative216px planning. Commodity33 Tobacco/one Istanbul alias unchanged;no equipment,age,health,earned fashion or earlier location inference;fresh approval required.')
    raise ValueError('Unknown B192 consumer')
'''
    compile(text,str(profile),'exec');profile.write_text(text,encoding='utf-8',newline='\n')
    rows=[derive('dk4tool/dialogue/lil_B190_layout_v1.py','dk4tool/dialogue/lil_B192_layout_v1.py',{'B190':'B192','frozenset({119,159})':'frozenset({115,153})'})]
    rows.append(derive('scripts/plan_lil_B190_layout_v5325.py','scripts/plan_lil_B192_layout_v5417.py',{
        'B190':'B192','layout_v5325':'layout_v5417','editorial_manuscript_v1b':'editorial_manuscript_v1','Plan17':'Plan8','all17':'all8','len(reports)==17':'len(reports)==8','plans=17':'plans=8',
    }))
    rows.append(derive('scripts/verify_lil_B190_fonts_v5326.py','scripts/verify_lil_B192_fonts_v5418.py',{
        'B190':'B192','fonts_v5326':'fonts_v5418','voices_v5315':'voices_v5407','blocks[190]':'blocks[192]','blocks[189]':'blocks[191]',
        '[119,159,254]':'[115,153,254]','159 if selector==119 else 119':'153 if selector==115 else 115',"r['source_selector']==119":"r['source_selector']==115",
        "b'\\x77Japanese','{SPEAKER:77}Hello.'":"b'\\x73Japanese','{SPEAKER:73}Hello.'",'len(cases)==len(qa_reports)==17':'len(cases)==len(qa_reports)==8',
        '136':'64','progressive_alignment_calls=128':'progressive_alignment_calls=56','complete_progressive_planes=16':'complete_progressive_planes=7','all17':'all8','All17':'All8','three sheets need':'one sheet needs',
    }))
    rows.append(derive('scripts/approve_lil_B190_native_v5327.py','scripts/approve_lil_B192_native_v5419.py',{
        'B190':'B192','native_approval_v5327':'native_approval_v5419','fonts_v5326':'fonts_v5418',"len(font['cases'])==17":"len(font['cases'])==8",'136':'64','==(16,1)':'==(7,1)',
        "len(font['review_sheets'])==3":"len(font['review_sheets'])==1",'blocks[190]':'blocks[192]',"{'revise':10,'retain-wording':7}":"{'revise':5,'retain-wording':3}","('progressive',119)":"('progressive',115)",
        'all17':'all8','All17':'All8','viewed17-panel':'viewed8-panel','on_three_sheets':'on_one_sheet','ten_revisions_and_seven_individually_justified_retentions':'five_revisions_and_three_individually_justified_retentions',
        'source_unknown_cause_retail_medicine_reported_one_go_cure_doubt_panacea_reputation_personal_wish_and_tentative_notice_preserved':'source_question_reversal_popularity_hyperbole_stammered_curiosity_offer_hesitant_assent_and_tentative_notice_preserved',
        '10 revisions/7 justified retentions':'5 revisions/3 justified retentions',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_exact_source_native_tools.json',dict(profile=str(profile),profile_sha256=sha(profile.read_bytes()),dependencies=deps,tools=rows,
        source_selectors115_153_linear_commands_and_original_no_macro_scope_guarded=True,no_inherited_R64_boundary_exception=True,
        no_manual_break_or_font_width_metric_guard_change=True,no_credit=True,full_goal_complete=False))
