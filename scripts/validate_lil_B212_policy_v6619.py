"""Challenge exact paragraph, font, source and typed-menu bindings before any ROM write."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_B212_profile_v1 import contract,profile_for
from dk4tool.dialogue.lil_B212_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record,compile_choice
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_policy_validation_v6619');DOC=Path('translations/lil_B212_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);c=contract();image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[212];clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[212];paths=[DOC,Path('translations/lil_B212_native_contract_v1.json'),Path('dk4tool/dialogue/lil_B212_profile_v1.py'),Path('dk4tool/dialogue/lil_B212_layout_v1.py'),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json')];before={str(p):sha(p.read_bytes()) for p in paths};positive=[];menu_positive=[];negative=[];reasons=[]
    for row in doc['records']:
        if row['kind']!='progressive':continue
        b=c['record_bindings'][row['id']];p=profile_for(arm,block,row['id']);assert p==profile_for(arm,clean,row['id']);encoded=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],p);qa=audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],p);assert encoded.encoded.hex()==b['compiled_hex'] and qa['native_page_count']==1 and qa['native_rows_per_page']==4 and qa['no_base_QA_issue_removed'] and not [i for i in qa['issues'] if i['severity'] in ['warning','error']]
        for issue in qa['issues']:
            if issue['code']=='line-break-count':assert b['row_count_reason'];reasons.append(dict(id=row['id'],reason=b['row_count_reason'],issue=issue))
        positive.append(dict(id=row['id'],compiled_hex=encoded.encoded.hex(),qa=qa))
    for key,b in c['choice_bindings'].items():
        rows=sorted([r for r in doc['records'] if r.get('command_offset')==int(key)],key=lambda r:r['option_index'])
        for side in ['source_command_hex','current_command_hex']:
            target=compile_choice(bytes.fromhex(b[side]),int(key),rows);assert target.hex()==b['target_hex'];menu_positive.append(dict(offset=int(key),version=side,count=b['count'],target_hex=target.hex(),all_complete_source_ordered_labels=True))
    assert len(positive)==9 and len(menu_positive)==4 and len(reasons)==4
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negative.append(dict(case=label,rejected=True,error=str(e)))
        else:raise RuntimeError('Unsafe or unreviewed B212 input accepted:'+label)
    row=doc['records'][0];raw=bytes.fromhex(row['source_hex']);p=profile_for(arm,block,row['id'])
    badprofiles=[('wider-window',replace(p,window_width_px=228)),('narrower-window',replace(p,window_width_px=210)),('taller-page',replace(p,max_lines=8)),('clipped-page',replace(p,max_lines=1)),('ASCII-width',replace(p,default_ascii_width=5)),('CP932-width',replace(p,default_multibyte_width=10)),('row-pitch',replace(p,line_height_px=12)),('unsafe-LF',replace(p,guard_linebreaks=False)),('unsafe-pair-phase',replace(p,pair_phase_safe_breaks=False)),('unreviewed-balance',replace(p,balanced_wrapping=not p.balanced_wrapping)),('literal-policy',replace(p,literal_prefix_policy='forbid')),('new-macro-width',replace(p,macro_widths={**p.macro_widths,'FI':24})),('new-macro-parity',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FI':4})),('dynamic-selector',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208})),('FE-selector',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{254})),('unscoped-profile',get_dialogue_profile('lil-opening-editorial-native-v1'))]
    for label,bad in badprofiles:assert bad!=p;reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,row['english'],bad))
    reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,row['id']));reject('changed-source-tail',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),row['id']));reject('unrelated-block',lambda:profile_for(arm,b'CS\0\1',row['id']));reject('typed-label-as-paragraph',lambda:profile_for(arm,block,'DK4_CHOICE_B212_C64_O0'))
    for r in doc['records']:
        if r['kind']!='progressive':continue
        source=bytes.fromhex(r['source_hex']);bad=source[:-1]+bytes([source[-1]^1]);profile=profile_for(arm,block,r['id']);reject('changed-complete-source-'+r['id'],lambda bad=bad,r=r,profile=profile:encode_relocatable_dialogue(bad,r['english'],profile))
    badtexts=[('wrong-static',row['english'].replace('{SPEAKER:95}','{SPEAKER:02}')),('dynamic-speaker',row['english'].replace('{SPEAKER:95}','{SPEAKER:D0}')),('manual-LB',row['english']+'{LB}'),('positioned-LB',row['english']+'{LB@3}'),('ALIGN',row['english']+'{ALIGN@2}'),('PAD',row['english']+'{PAD}'),('raw-LF',row['english']+'\n'),('raw-CR',row['english']+'\r'),('leading-space',row['english'].replace('}Hello','} Hello')),('trailing-space',row['english']+' '),('new-substitution',row['english']+'{MACRO:FI}')]
    for label,text in badtexts:assert text!=row['english'];reject(label,lambda text=text:encode_relocatable_dialogue(raw,text,p))
    fidelity=[(32,'invented-kinship',lambda s:s+' My niece!'),(54,'lost-Changban',lambda s:s.replace('at Changban Bridge ','')),(54,'lost-chest',lambda s:s.replace(' to his chest','')),(54,'lost-lone-ride',lambda s:s.replace(' alone','')),(58,'rumor-made-fact',lambda s:s.replace('I heard a rumor about','I know of')),(58,'definite-location',lambda s:s.replace('a peninsula around here','the peninsula')),(58,'lost-attribution-qualification',lambda s:s.replace('They say ','')),(62,'guaranteed-find',lambda s:s.replace('I thought you might have better luck.',"You'll find it.")),(72,'lost-epithet',lambda s:s.replace(', Lord of the Magnificent Beard','')),(78,'lost-approximation',lambda s:s.replace('probably ','')),(78,'wrong-memorial-genre',lambda s:s.replace('Memorial Before the Expedition','poem'))]
    for index,label,edit in fidelity:
        r=next(r for r in doc['records'] if r.get('source_record_index')==index and r['kind']=='progressive');text=edit(r['english']);assert text!=r['english'];source=bytes.fromhex(r['source_hex']);profile=profile_for(arm,block,r['id']);reject(label,lambda text=text,source=source,profile=profile:encode_relocatable_dialogue(source,text,profile))
    for key,b in c['choice_bindings'].items():
        offset=int(key);rows=sorted([deepcopy(r) for r in doc['records'] if r.get('command_offset')==offset],key=lambda r:r['option_index']);source=bytes.fromhex(b['current_command_hex']);badraw=bytes([source[0]^1])+source[1:];reject(f'menu{key}-opcode',lambda badraw=badraw,offset=offset,rows=rows:compile_choice(badraw,offset,rows));reject(f'menu{key}-unknown-offset',lambda source=source,offset=offset,rows=rows:compile_choice(source,offset+2,rows));reject(f'menu{key}-missing-option',lambda source=source,offset=offset,rows=rows:compile_choice(source,offset,rows[:-1]));reject(f'menu{key}-reversed-options',lambda source=source,offset=offset,rows=rows:compile_choice(source,offset,list(reversed(rows))))
        for label,value in [('abbreviated-or-unreviewed',rows[0]['english'][:1]),('manual-break',rows[0]['english']+'{LB}'),('trailing-padding',rows[0]['english']+' ')]:
            bad=deepcopy(rows);bad[0]['english']=value;assert bad!=rows;reject(f'menu{key}-{label}',lambda source=source,offset=offset,bad=bad:compile_choice(source,offset,bad))
    expected=len(badprofiles)+4+9+len(badtexts)+len(fidelity)+2*7;assert len(negative)==expected and len({n['case'] for n in negative})==expected and all(n['rejected'] for n in negative)
    for path,h in before.items():assert sha(Path(path).read_bytes())==h
    ROOT.mkdir(parents=True);save(ROOT/'nine_paragraph_four_menu_source_cases_all_rejections_four_rowcount_reasons.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),positive_paragraph_cases=positive,positive_paragraph_count=9,positive_choice_object_versions=menu_positive,choice_objects=2,choice_labels=5,negative_cases=negative,negative_count=expected,row_count_reasons=reasons,all_rejections_before_any_ROM_archive_or_registry_mutation=True,no_base_QA_warning_error_removed_or_waived=True,all_input_prose_contract_profile_formatter_registry_and_ledger_hashes_unchanged=True,native_geometry_bound_but_actual_backing_English_reference_and_release_still_pending=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,evidence=before,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(paragraphs=9,choice_objects=2,choice_labels=5,negative_count=expected,rowcount_reasons=4,credit=0))
