"""Validate20 exact paragraphs and reject source/voice/page/font/control/fidelity damage without mutation."""
from pathlib import Path
from dataclasses import replace
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.lil_B209_profile_v1 import profile_for,contract
from dk4tool.dialogue.lil_B209_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_policy_validation_v6479b')
DOC=Path('translations/lil_B209_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);c=contract();image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[209];clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[209];before={str(p):sha(p.read_bytes()) for p in [DOC,Path('translations/release_stack.json'),Path('translations/lil_B209_native_contract_v1.json'),Path('dk4tool/dialogue/lil_B209_profile_v1.py'),Path('dk4tool/dialogue/lil_B209_layout_v1.py')]};positive=[];negatives=[];rowcounts=[]
    for row in doc['records']:
        ident=row['id'];bound=c['record_bindings'][ident];raw=bytes.fromhex(bound['compiler_source_hex']);p=profile_for(arm,block,ident);assert p==profile_for(arm,clean,ident);value=encode_relocatable_dialogue(raw,row['english'],p);qa=audit_relocatable_dialogue_record(raw,row['english'],p)
        assert value.encoded.hex()==bound['compiled_hex'] and qa['native_page_count']==bound['native_page_count']
        issues=[]
        for issue in qa['issues']:
            if issue['code']=='line-break-count' and bound['row_count_reason']:rowcounts.append(dict(id=ident,issue=issue,reason=bound['row_count_reason']))
            elif issue['severity'] in ['error','warning']:issues.append(issue)
        assert not issues,(ident,issues);positive.append(dict(id=ident,compiled_hex=value.encoded.hex(),profile=p.name,qa=qa,exact_words_source_controls_singleton_selector_and_page_contract=True))
    assert len(positive)==20 and len(rowcounts)==6 and sum(p['qa']['native_page_count'] for p in positive)==22
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negatives.append(dict(case=label,error=str(e),rejected=True))
        else:raise AssertionError('Unreviewed or unsafe change accepted:'+label)
    long=doc['records'][0];ident=long['id'];raw=bytes.fromhex(c['record_bindings'][ident]['compiler_source_hex']);p=profile_for(arm,block,ident)
    for label,bad in [('viewport',replace(p,window_width_px=228)),('unreviewed-total-rows',replace(p,max_lines=7)),('clipped-four-total-rows',replace(p,max_lines=4)),('ASCII-width',replace(p,default_ascii_width=5)),('CP932-width',replace(p,default_multibyte_width=10)),('line-pitch',replace(p,line_height_px=12)),('guard',replace(p,guard_linebreaks=False)),('pair-phase',replace(p,pair_phase_safe_breaks=False)),('balanced-opt-in',replace(p,balanced_wrapping=False)),('literal-prefix-guard',replace(p,literal_prefix_policy='forbid')),('macro-width',replace(p,macro_widths={**p.macro_widths,'FI':24})),('macro-parity',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FI':4})),('invented-FE-selector',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{254})),('unscoped-base-profile',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,long['english'],bad))
    reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block,ident));reject('changed-block',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1]),ident));reject('unrelated-source-block',lambda:profile_for(arm,b'CS\0\1',ident));reject('unreviewed-record',lambda:profile_for(arm,block,'DK4_MES_B210_R0001'))
    for row in doc['records']:
        ident=row['id'];source=bytes.fromhex(c['record_bindings'][ident]['compiler_source_hex']);profile=profile_for(arm,block,ident);bad=source[:-1]+bytes([source[-1]^1]);reject('mutated-complete-source-'+ident,lambda bad=bad,row=row,profile=profile:encode_relocatable_dialogue(bad,row['english'],profile))
    ident=long['id'];p=profile_for(arm,block,ident)
    for label,target in [('wrong-speaker',long['english'].replace('{SPEAKER:0C}','{SPEAKER:0B}')),('manual-LB',long['english'].replace('Word ','Word{LB} ',1)),('raw-LF',long['english'].replace('Word ','Word\n',1)),('positioned-layout',long['english']+'{ALIGN@2}'),('padding',long['english']+'{PAD}'),('extra-leading-space',long['english'].replace('}Word','} Word')),('extra-trailing-space',long['english']+' '),('lost-hearsay',long['english'].replace('are said to be','are')),('invented-Tokugawa-intent',long['english']+' Tokugawa ordered it.'),('invented-substitution',long['english']+'{MACRO:FI}')]:reject(label,lambda target=target:encode_relocatable_dialogue(raw,target,p))
    r=next(r for r in doc['records'] if r['id']=='DK4_MES_B209_R0030');p=profile_for(arm,block,r['id']);src=bytes.fromhex(c['record_bindings'][r['id']]['compiler_source_hex']);reject('concealment-uncertainty-erased',lambda:encode_relocatable_dialogue(src,r['english'].replace('It appears that a clan','A clan'),p))
    r=next(r for r in doc['records'] if r['id']=='DK4_MES_B209_R0033');p=profile_for(arm,block,r['id']);src=bytes.fromhex(c['record_bindings'][r['id']]['compiler_source_hex']);reject('full-signature-field-lost',lambda:encode_relocatable_dialogue(src,r['english'].replace('Yukihisa Genjo Shiraki','Yukihisa Shiraki'),p))
    r=next(r for r in doc['records'] if r['id']=='DK4_MES_B209_R0071');p=profile_for(arm,block,r['id']);src=bytes.fromhex(c['record_bindings'][r['id']]['compiler_source_hex']);reject('tentative-interest-made-promise',lambda:encode_relocatable_dialogue(src,r['english'].replace("Maybe I'll look for it.","Let's look for it."),p));reject('ordinary-speech-gains-two-page-profile',lambda:encode_relocatable_dialogue(src,r['english'],replace(p,max_lines=8)))
    r=next(r for r in doc['records'] if r['kind']!='progressive');p=profile_for(arm,block,r['id']);src=bytes.fromhex(c['record_bindings'][r['id']]['compiler_source_hex']);reject('typed-virtual-selector-omitted',lambda:encode_relocatable_dialogue(src[1:],r['english'],p));reject('typed-selector-reassigned',lambda:encode_relocatable_dialogue(bytes([12])+src[1:],r['english'],p))
    assert len(negatives)==54
    for path,digest in before.items():assert sha(Path(path).read_bytes())==digest
    ROOT.mkdir(parents=True);save(ROOT/'twenty_positive_QA_cases54_rejections_six_rowcount_reasons.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),positive_cases=positive,negative_cases=negatives,positive_count=20,negative_count=len(negatives),all_rejections_before_ROM_or_archive_mutation=True,row_count_reasons=rowcounts,no_unwaived_warning_or_error=True,source_bound_ordinary_boundary_rules_not_global_waivers=True,all_first_last_glyphs_bounds_pages_and_runtime_substitutions_bound_by_native_proofs=True,all_input_policy_prose_registry_files_unchanged=True,no_shared_helper_runtime_ROM_ledger_orcredit_mutation=True,evidence=before,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('20 exact paragraph QA cases/54 damage rejections/six individual rowcount reasons pass. Native128px viewport is never introduced;two native64px pages remain exact. No credit.')
