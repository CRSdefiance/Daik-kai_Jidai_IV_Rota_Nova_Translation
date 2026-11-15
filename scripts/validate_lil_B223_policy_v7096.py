"""Challenge exact source/prose,virtual notices,two-page scope and retained QA diagnostics."""
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_B223_profile_v1 import contract,profile_for
from dk4tool.dialogue.lil_B223_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B223_policy_validation_v7096');DOC=Path('translations/lil_B223_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);c=contract();image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[223];clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[223]
    deps=[DOC,Path('translations/lil_B223_native_contract_v1.json'),Path('dk4tool/dialogue/lil_B223_profile_v1.py'),Path('dk4tool/dialogue/lil_B223_layout_v1.py'),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json')];before={str(p):sha(p.read_bytes()) for p in deps};positive=[];negative=[];reasons=[]
    for r in doc['records']:
        b=c['record_bindings'][r['id']];p=profile_for(arm,block,r['id']);assert p==profile_for(arm,clean,r['id']);raw=bytes.fromhex(b['compiler_source_hex']);value=encode_relocatable_dialogue(raw,r['english'],p);q=audit_relocatable_dialogue_record(raw,r['english'],p)
        assert value.encoded.hex()==b['compiled_hex'] and q['native_page_count']==b['native_page_count'] and q['native_rows_per_page']==4 and q['base_QA_issues']==r['all_original_base_QA_issues'] and q['all_original_base_QA_issues_preserved'] and not any(i['severity'] in ['warning','error'] for i in q['issues'])
        for issue in q['issues']:
            if issue['code']=='line-break-count':assert b['row_count_reason'];reasons.append(dict(id=r['id'],reason=b['row_count_reason'],issue=issue))
        positive.append(dict(id=r['id'],compiled_hex=value.encoded.hex(),qa=q))
    assert len(positive)==17 and len(reasons)==6 and sum(len(r['qa']['exact_reviewed_base_warnings']) for r in positive)==2
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negative.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError('Unsafe or unreviewed input accepted:'+label)
    r=doc['records'][0];raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block,r['id'])
    badprofiles=[('wider-window',replace(p,window_width_px=228)),('narrower-window',replace(p,window_width_px=210)),('unscoped-extra-page',replace(p,max_lines=8)),('ASCII-width',replace(p,default_ascii_width=5)),('CP932-width',replace(p,default_multibyte_width=10)),('row-pitch',replace(p,line_height_px=12)),('bare-LF',replace(p,guard_linebreaks=False)),('unsafe-pair-phase',replace(p,pair_phase_safe_breaks=False)),('unreviewed-balance',replace(p,balanced_wrapping=not p.balanced_wrapping)),('literal-policy',replace(p,literal_prefix_policy='forbid')),('new-macro-width',replace(p,macro_widths={**p.macro_widths,'FI':24})),('new-macro-parity',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FI':4})),('missing-D0',replace(p,leading_speaker_bytes=p.leading_speaker_bytes-{208})),('added-FE',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{254})),('unscoped-profile',get_dialogue_profile('lil-opening-editorial-native-v1'))]
    for label,bad in badprofiles:assert bad!=p;reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,r['english'],bad))
    reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,r['id']));reject('changed-source-end',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),r['id']));reject('unrelated-block',lambda:profile_for(arm,b'CS\0\1',r['id']));reject('unreviewed-record',lambda:profile_for(arm,block,'DK4_MES_B223_R0099'))
    for row in doc['records']:
        b=c['record_bindings'][row['id']];source=bytes.fromhex(b['compiler_source_hex']);profile=profile_for(arm,block,row['id']);bad=source[:-1]+bytes([source[-1]^1]);reject('changed-complete-source-'+row['id'],lambda bad=bad,row=row,profile=profile:encode_relocatable_dialogue(bad,row['english'],profile));reject('changed-reviewed-prose-'+row['id'],lambda source=source,row=row,profile=profile:encode_relocatable_dialogue(source,row['english']+' Really.',profile))
        if row['kind']!='progressive':reject('missing-virtual-selector-'+row['id'],lambda source=source,row=row,profile=profile:encode_relocatable_dialogue(source[1:],row['english'],profile))
        if b['native_page_count']==2:
            for label,maximum in [('forced-single-page',4),('unscoped-third-page',12)]:reject(label+'-'+row['id'],lambda source=source,row=row,profile=profile,maximum=maximum:encode_relocatable_dialogue(source,row['english'],replace(profile,max_lines=maximum)))
    for label,text in [('wrong-static',r['english'].replace('{SPEAKER:15}','{SPEAKER:02}')),('wrong-dynamic',r['english'].replace('{SPEAKER:15}','{SPEAKER:D0}')),('manual-LB',r['english']+'{LB}'),('positioned-LB',r['english']+'{LB@3}'),('manual-ALIGN',r['english']+'{ALIGN@2}'),('manual-PAD',r['english']+'{PAD}'),('raw-LF',r['english']+'\n'),('raw-CR',r['english']+'\r'),('authored-leading-space',r['english'].replace('}The','} The')),('trailing-space',r['english']+' '),('invented-FI',r['english']+'{MACRO:FI}')]:
        assert text!=r['english'];reject(label,lambda text=text:encode_relocatable_dialogue(raw,text,p))
    edits=[(31,'approximate-as-exact','Some two hundred','Exactly two hundred'),(31,'lineage-as-generic-legacy',"Mongol Empire's ruling line","Mongol Empire's cultural legacy"),(31,'invented-European-extent','Central to West Asia','Asia to Europe'),(34,'report-as-fact','It says he wore','It is certain he wore'),(34,'chipping-as-blunting','chipped','blunted'),(37,'decades-as-days','Decades later','Days later'),(40,'near-sea-as-arrival','almost within sight of the sea','on the seashore'),(40,'missing-heat','scorching','ordinary'),(40,'death-as-sleep','he died','he fell asleep'),(44,'rumor-as-guaranteed-find',"The armor still hasn't been found.",'You are guaranteed to find the armor.'),(48,'truncated-signature','Ian Dukov','Dukov'),(56,'old-family-only-address',"Ian's","Dukov's"),(67,'conjecture-as-certainty','probably','certainly')]
    for index,label,old,new in edits:
        row=next(v for v in doc['records'] if v.get('source_record_index')==index);assert old in row['english'];text=row['english'].replace(old,new);source=bytes.fromhex(c['record_bindings'][row['id']]['compiler_source_hex']);profile=profile_for(arm,block,row['id']);reject(label,lambda source=source,text=text,profile=profile:encode_relocatable_dialogue(source,text,profile))
    assert len(negative)==len({v['case'] for v in negative})==88 and before=={str(p):sha(p.read_bytes()) for p in deps}
    ROOT.mkdir(parents=True);save(ROOT/'seventeen_positives88_rejections_six_row_reasons_two_exact_waivers.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),positive_paragraph_cases=positive,positive_paragraph_count=17,complete_native_pages=19,negative_cases=negative,negative_count=88,row_count_reasons=reasons,two_exact_record_local_article_waivers_all_base_diagnostics_preserved=True,all_rejections_before_ROM_archive_registry_or_ledger_mutation=True,all_input_contract_profile_formatter_registry_and_ledger_hashes_unchanged=True,exact_prose_guarding_not_automatic_semantic_approval_of_unseen_text=True,virtual_D0_not_stored_and_original8_slot7_body_alias_packing_still_requires_relocation_checks=True,final_stored_English_actual_reference_and_release_pending=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,evidence=before,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('17 positive objects/19 pages,88 distinct unsafe-input rejections.6 row reasons,2 exact waivers,all base diagnostics retained. No ROM or credit.')
