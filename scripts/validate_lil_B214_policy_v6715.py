"""Challenge exact source/prose, virtual voice selectors, native geometry and signature identity."""
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_B214_profile_v1 import contract,profile_for
from dk4tool.dialogue.lil_B214_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B214_policy_validation_v6715');DOC=Path('translations/lil_B214_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);c=contract();image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[214];clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[214]
    paths=[DOC,Path('translations/lil_B214_native_contract_v1.json'),Path('dk4tool/dialogue/lil_B214_profile_v1.py'),Path('dk4tool/dialogue/lil_B214_layout_v1.py'),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json')];before={str(p):sha(p.read_bytes()) for p in paths};positive=[];negative=[];reasons=[]
    for row in doc['records']:
        b=c['record_bindings'][row['id']];p=profile_for(arm,block,row['id']);assert p==profile_for(arm,clean,row['id']);raw=bytes.fromhex(b['compiler_source_hex']);encoded=encode_relocatable_dialogue(raw,row['english'],p);qa=audit_relocatable_dialogue_record(raw,row['english'],p)
        assert encoded.encoded.hex()==b['compiled_hex'] and qa['native_page_count']==1 and qa['native_rows_per_page']==4 and qa['no_base_QA_issue_removed'] and not [i for i in qa['issues'] if i['severity'] in ['warning','error']]
        for issue in qa['issues']:
            if issue['code']=='line-break-count':assert b['row_count_reason'];reasons.append(dict(id=row['id'],reason=b['row_count_reason'],issue=issue))
        positive.append(dict(id=row['id'],compiled_hex=encoded.encoded.hex(),qa=qa))
    assert len(positive)==17 and len(reasons)==11
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negative.append(dict(case=label,rejected=True,error=str(e)))
        else:raise RuntimeError('Unsafe or unreviewed B214 input accepted:'+label)
    row=doc['records'][0];raw=bytes.fromhex(row['source_hex']);p=profile_for(arm,block,row['id'])
    badprofiles=[('wider-window',replace(p,window_width_px=228)),('narrower-window',replace(p,window_width_px=210)),('extra-page',replace(p,max_lines=8)),('ASCII-width',replace(p,default_ascii_width=5)),('CP932-width',replace(p,default_multibyte_width=10)),('row-pitch',replace(p,line_height_px=12)),('unsafe-LF',replace(p,guard_linebreaks=False)),('unsafe-pair-phase',replace(p,pair_phase_safe_breaks=False)),('unreviewed-balance',replace(p,balanced_wrapping=not p.balanced_wrapping)),('literal-policy',replace(p,literal_prefix_policy='forbid')),('new-macro-width',replace(p,macro_widths={**p.macro_widths,'FI':24})),('new-macro-parity',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FI':4})),('missing-dynamic-selector',replace(p,leading_speaker_bytes=p.leading_speaker_bytes-{208})),('FE-selector',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{254})),('unscoped-profile',get_dialogue_profile('lil-opening-editorial-native-v1'))]
    for label,bad in badprofiles:assert bad!=p;reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,row['english'],bad))
    reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,row['id']));reject('changed-source-tail',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),row['id']));reject('unrelated-block',lambda:profile_for(arm,b'CS\0\1',row['id']));reject('unreviewed-record',lambda:profile_for(arm,block,'DK4_MES_B214_R0035'))
    for r in doc['records']:
        source=bytes.fromhex(c['record_bindings'][r['id']]['compiler_source_hex']);bad=source[:-1]+bytes([source[-1]^1]);profile=profile_for(arm,block,r['id']);reject('changed-complete-source-'+r['id'],lambda bad=bad,r=r,profile=profile:encode_relocatable_dialogue(bad,r['english'],profile))
        reject('changed-complete-prose-'+r['id'],lambda source=source,r=r,profile=profile:encode_relocatable_dialogue(source,r['english']+' Really.',profile))
        if r['kind']!='progressive':reject('missing-virtual-selector-'+r['id'],lambda source=source,r=r,profile=profile:encode_relocatable_dialogue(source[1:],r['english'],profile))
    for label,text in [('wrong-static',row['english'].replace('{SPEAKER:04}','{SPEAKER:02}')),('dynamic-speaker',row['english'].replace('{SPEAKER:04}','{SPEAKER:D0}')),('manual-LB',row['english']+'{LB}'),('positioned-LB',row['english']+'{LB@3}'),('ALIGN',row['english']+'{ALIGN@2}'),('PAD',row['english']+'{PAD}'),('raw-LF',row['english']+'\n'),('raw-CR',row['english']+'\r'),('leading-space',row['english'].replace('}Admiral','} Admiral')),('trailing-space',row['english']+' '),('new-substitution',row['english']+'{MACRO:FI}')]:
        assert text!=row['english'];reject(label,lambda text=text:encode_relocatable_dialogue(raw,text,p))
    edits=[(34,'invented-road-name',lambda s:s.replace('a road leading to Rome','the Appian Way in Rome')),(44,'hearsay-to-fact',lambda s:s.replace('They say a sword','A sword')),(44,'invented-burial-site',lambda s:s.replace('a place connected to him','his grave in Jerusalem')),(48,'real-curse',lambda s:s+' The sword is cursed.'),(51,'guaranteed-find',lambda s:s.replace("I think it's worth looking for","you are sure to find it")),(62,'new-clerical-rank',lambda s:s.replace('Manuel','Father Manuel')),(68,'old-inconsistent-signature',lambda s:s.replace('Janus Pasar','Janus Pasha')),(75,'invented-relationship',lambda s:s.replace('Janus','Uncle Janus')),(87,'deferral-to-firm-refusal',lambda s:s.replace("I'm not entirely opposed","I forbid it"))]
    for index,label,edit in edits:
        r=next(r for r in doc['records'] if r.get('source_record_index')==index);text=edit(r['english']);assert text!=r['english'];source=bytes.fromhex(c['record_bindings'][r['id']]['compiler_source_hex']);profile=profile_for(arm,block,r['id']);reject(label,lambda source=source,text=text,profile=profile:encode_relocatable_dialogue(source,text,profile))
    assert len(negative)==len({r['case'] for r in negative}) and len(negative)>=70 and all(r['rejected'] for r in negative)
    for path,h in before.items():assert sha(Path(path).read_bytes())==h
    ROOT.mkdir(parents=True);save(ROOT/'seventeen_positives_all_rejections_eleven_rowcount_reasons.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),positive_paragraph_cases=positive,positive_paragraph_count=17,complete_native_pages=17,negative_cases=negative,negative_count=len(negative),row_count_reasons=reasons,six_exact_ordinary_boundaries_no_global_waiver=True,all_rejections_before_ROM_archive_registry_or_ledger_mutation=True,no_base_QA_warning_error_removed_or_waived=True,all_input_contract_profile_formatter_registry_and_ledger_hashes_unchanged=True,final_stored_English_actual_reference_and_release_pending=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,evidence=before,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(positives=17,native_pages=17,negative_count=len(negative),rowcount_reasons=11,credit=0))
