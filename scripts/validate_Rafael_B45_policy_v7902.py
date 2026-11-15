"""Twelve replayed native policy positives and actual-changing expected-guard challenges."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.rafael_B45_profile_v1 import contract,profile_for,validate_runtime
from dk4tool.dialogue.rafael_B45_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_policy_validation_v7902')
DOC=Path('translations/rafael_B45_editorial_manuscript_v4.json')
SEMANTIC=[
    ('invented-kinship',5,'Julio','Grandpa'),
    ('lost-conditional-cargo',18,'If you have anything you bought in Lisbon','Sell everything we bought in Lisbon'),
    ('wrong-contract',21,'contract','sales receipt'),
    ('wrong-fee-recipient',29,'local ruler','shopkeeper'),
    ('wrong-office',29,"Palace or Governor's Office",'Market'),
    ('invented-bribe',29,'contract fee','bribe'),
    ('invented-universal-right',29,'right to trade there','permanent right to trade anywhere'),
    ('lost-early-qualification',33,"When you're just starting out",'From now on'),
    ('invented-share-guarantee',33,'minimum fee should be enough','minimum fee always guarantees a 20 percent share'),
    ('wrong-responsibility',37,"I've already taken care","You've already taken care"),
    ('wrong-city',37,'Ceuta','Lisbon'),
    ('invented-family-address',37,'next ones yourself','next one, son'),
    ('wrong-share-value',52,'20 percent','30 percent'),
    ('invented-sales-volume-cap',52,'you can buy','you can sell'),
    ('lost-optional-sale',58,"If there's anything you want to sell",'Sell all of your cargo now'),
    ('invented-completed-profit',61,'All right.',"I've sold it all at a profit."),
]
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);c=contract();assert doc['translation_policy']=='natural-dialogue-v2'
    validate_natural_dialogue_batch(doc)
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    blocks=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    cleanblock=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file(doc['file_path'])).blocks[45]
    target=Path('work/analysis/Rafael_B45_relocation_v7884/SC0_block45_RESEARCH_ONLY.bin').read_bytes()
    paths={DOC,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),
        Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),
        *[Path('dk4tool/dialogue')/n for n in ['rafael_B45_profile_v1.py','rafael_B45_layout_v1.py','rafael_B45_plan_v1.py']],
        Path('translations/rafael_B45_native_contract_v1.json')}
    before={str(p):sha(p.read_bytes()) for p in paths};positive=[];negative=[];profiles={}
    validate_runtime(image)
    for row in doc['records']:
        b=c['record_bindings'][row['id']]
        consumer='FE-paper' if row['source_selector']==254 else 'progressive'
        p=profile_for(arm,blocks[45],row['id'],row['file_path'],consumer)
        assert profile_for(arm,cleanblock,row['id'],row['file_path'],consumer)==p
        profiles[row['id']]=p;raw=bytes.fromhex(row['source_hex'])
        encoded=encode_relocatable_dialogue(raw,row['english'],p);qa=audit_relocatable_dialogue_record(raw,row['english'],p)
        assert encoded.encoded.hex()==row['compiled_hex']==b['compiled_hex']
        assert encoded.encoded[0]==row['source_selector'] and b'\0' not in encoded.encoded[1:]
        assert qa['base_QA_issues']==b['base_QA_issues'] and qa['native_page_count']==1
        assert qa['all_original_base_QA_issues_preserved'] and not any(i['severity'] in ['warning','error'] for i in qa['issues'])
        positive.append(dict(id=row['id'],source_selector=row['source_selector'],consumer=consumer,
            compiled_hex=encoded.encoded.hex(),clean_andcurrent_profile_equal=True,qa=qa))
    def reject(label,fn,expected):
        try:fn()
        except ValueError as error:
            assert expected in str(error),(label,str(error))
            negative.append(dict(case=label,rejected=True,error=str(error),expected_guard=expected))
        else:raise AssertionError('Unsafe input accepted:'+label)
    body_guard='complete source and reviewed logical paragraph required'
    profile_guard='font/window/page/selector/guard/macro profile changed'
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);p=profiles[row['id']];text=row['english']
        bad=raw[:-1]+bytes([raw[-1]^1]);assert bad!=raw
        reject('changed-source-'+row['id'],lambda bad=bad,p=p,text=text:encode_relocatable_dialogue(bad,text,p),body_guard)
        reject('changed-prose-'+row['id'],lambda raw=raw,p=p,text=text:encode_relocatable_dialogue(raw,text+'!',p),body_guard)
        for gate in ['source','context','localization','naturalness','formatting']:
            altered=deepcopy(doc);next(r for r in altered['records'] if r['id']==row['id'])['review'][gate]=False
            assert altered!=doc
            reject('missing-'+gate+'-'+row['id'],lambda altered=altered:validate_natural_dialogue_batch(altered),'gate is not approved')
    for row in [doc['records'][0],next(r for r in doc['records'] if r['source_selector']==254)]:
        p=profiles[row['id']];raw=bytes.fromhex(row['source_hex']);text=row['english']
        changes=[
            ('ASCII-width',replace(p,default_ascii_width=5)),('viewport228',replace(p,window_width_px=228)),
            ('row-pitch',replace(p,line_height_px=12)),('extra-page-capacity',replace(p,max_lines=8)),
            ('lost-page-capacity',replace(p,max_lines=2)),('pair-phase-disabled',replace(p,pair_phase_safe_breaks=False)),
            ('guard-disabled',replace(p,guard_linebreaks=False)),('wrong-balance-policy',replace(p,balanced_wrapping=not p.balanced_wrapping)),
            ('fallback208',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{208})),
            ('literal-policy',replace(p,literal_prefix_policy='forbid')),
            ('FI-stale-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FI':7})),
            ('FI-stale-width',replace(p,macro_widths={**p.macro_widths,'FI':42})),
            ('FO-invented-width',replace(p,macro_widths={**p.macro_widths,'FO':66}))]
        for label,bad in changes:
            assert bad!=p
            reject(label+'-'+row['id'],lambda raw=raw,text=text,bad=bad:encode_relocatable_dialogue(raw,text,bad),profile_guard)
        wrong='progressive' if row['source_selector']==254 else 'FE-paper'
        reject('wrong-consumer-'+row['id'],lambda row=row,wrong=wrong:profile_for(arm,blocks[45],row['id'],row['file_path'],wrong),'Original Rafael-B45 consumer required')
    zero=doc['records'][0];raw=bytes.fromhex(zero['source_hex']);text=zero['english'];p=profiles[zero['id']]
    texts=[('manual-break',text+'{LB}'),('positioned-break',text+'{LB@3}'),('alignment',text+'{ALIGN@3}'),
        ('padding',text+'{PAD}'),('literal-LF',text+'\n'),('literal-CR',text+'\r'),
        ('leading-space',text.replace('}','} ',1)),('embedded-NUL',text+'\0'),
        ('missing-zero-selector',text.removeprefix('{SPEAKER:00}')),
        ('changed-zero-selector',text.replace('{SPEAKER:00}','{SPEAKER:06}')),
        ('invented-FI',text+'{MACRO:FI}'),('invented-FA',text+'{MACRO:FA}'),('invented-FO',text+'{MACRO:FO}')]
    for label,bad in texts:
        assert bad!=text;reject(label,lambda bad=bad:encode_relocatable_dialogue(raw,bad,p),body_guard)
    reject('missing-source00-byte',lambda:encode_relocatable_dialogue(raw[1:],text,p),body_guard)
    for label,index,old,new in SEMANTIC:
        row=next(r for r in doc['records'] if r['source_record_index']==index);assert old in row['english']
        bad=row['english'].replace(old,new);assert bad!=row['english']
        reject(label,lambda row=row,bad=bad:encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),bad,profiles[row['id']]),body_guard)
    fe=next(r for r in doc['records'] if r['source_selector']==254)
    for label,bad in [
        ('erased-company',fe['english'].replace('{MACRO:FO}','a company')),
        ('wrong-company-macro',fe['english'].replace('{MACRO:FO}','{MACRO:FI}')),
        ('unsafe-printf-percent',fe['english'].replace('20 percent','20% of sales')),
        ('converted-FE-selector',fe['english'].replace('{SPEAKER:FE}','{HEX:F8 F2}'))]:
        assert bad!=fe['english']
        reject(label,lambda bad=bad:encode_relocatable_dialogue(bytes.fromhex(fe['source_hex']),bad,profiles[fe['id']]),body_guard)
    block_guard='file-qualified B45 source/current block and2b6 runtime required'
    for label,bad in [('changed-tail',blocks[45][:-1]+bytes([blocks[45][-1]^1])),
                      ('changed-header',bytes([blocks[45][0]^1])+blocks[45][1:]),('wrong-block',blocks[44]),('already-target-block',target)]:
        assert bad!=blocks[45]
        reject(label,lambda bad=bad:profile_for(arm,bad,zero['id'],zero['file_path']),block_guard)
    reject('wrong-file',lambda:profile_for(arm,blocks[45],zero['id'],'/data/SC2.DK4'),block_guard)
    reject('changed-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],blocks[45],zero['id'],zero['file_path']),block_guard)
    reject('unreviewed-ID',lambda:profile_for(arm,blocks[45],'DK4_MES_B45_R9999',zero['file_path']),'Unreviewed Rafael-B45 paragraph')
    for component in c['runtime_component_hashes']:
        original=image.read_file(component);changed=original[:-1]+bytes([original[-1]^1]);assert changed!=original
        class AlteredImage:
            def read_file(self,path):return changed if path==component else image.read_file(path)
        reject('runtime-component-'+component,lambda:validate_runtime(AlteredImage()),'Exact Rafael-B45 runtime component required:')
    for field,value,message in [('target_locale','en-GB','requires target_locale en-US'),('encoder','legacy','requires a supported dialogue encoder')]:
        altered=deepcopy(doc);altered[field]=value;assert altered!=doc
        reject('batch-'+field,lambda altered=altered:validate_natural_dialogue_batch(altered),message)
    assert len(positive)==12 and len({r['case'] for r in negative})==len(negative)
    assert sum(i['code']=='line-break-count' for r in positive for i in r['qa']['issues'])==6
    assert before=={str(p):sha(p.read_bytes()) for p in paths}
    ROOT.mkdir(parents=True);save(ROOT/'12_positives_actual_changing_expected_guard_rejections.json',dict(
        positive_cases=positive,positive_count=12,negative_cases=negative,negative_count=len(negative),
        all_original_QA_infos_preserved_no_warnings_orwaivers=True,original_rowcount_infos=6,
        all_expected_ValueError_guards_not_arbitrary_exceptions=True,
        exact_twelve_source_current_profile_pairs_andruntime_components_bound=True,
        all_ROM_registry_ledger_pins_andpolicy_files_unchanged=True,
        source00_NUL_body_guard_andFE_null_actor_scope_challenged=True,
        all_five_record_gates_challenged_for_each_record=True,
        semantic_qualifier_fee_city_share_optional_sale_andno_invented_facts_challenges=16,
        atomic_production_andregistered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in sorted(paths)},producer_sha256=sha(Path(__file__).read_bytes()),
        new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('12 exact policy positives;',len(negative),'actual-changing expected-guard rejections;six original infos/no warning waivers.All inputs unchanged;atomic production pending.')
