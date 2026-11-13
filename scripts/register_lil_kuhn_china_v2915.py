"""Register218 guarded ordinary/FE speeches after fullV2883 cumulative stack."""
import os
from pathlib import Path
from copy import deepcopy
from dk4tool.patch import lil_kuhn_china_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_China_registration_v2915')
PROFILE='all-routes-unified-v2916'
PARENT=Path('out/all_routes_combined_v2883_candidate.nds')
DOC=Path('translations/lil_kuhn_china_editorial_manuscript_v7.json')
MAP=Path('translations/lil_kuhn_china_editorial_relocation_map_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent=NdsImage.open(PARENT);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapping=read(DOC),read(MAP)
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(MAP),str(Path(owned.__file__)),__file__,
        'dk4tool/dialogue/lil_kuhn_china_profile.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/lil_kuhn_china_layout_v1.py',
        doc['source_context'],doc['control_contract'],doc['branch_proof'],doc['native_font_proof'],doc['native_FE_font_proof'],doc['representative_proof'],
        'scripts/verify_lil_kuhn_china_FE_v2901b.py','scripts/lil_kuhn_china_FE_painter_v2909.py','scripts/approve_lil_kuhn_china_fonts_v2905.py',
        doc['historical_representative_sheet_review'],doc['prior_current_sheet_review'],doc['final_padding_proof'],
        mapping['source_plan'],mapping['source_census'],
        'work/analysis/lil_Kuhn_China_reference_approval_v2914/approval_receipt.json',
        'work/analysis/lil_Kuhn_China_loader_v2911/whole_SC2_and_nine_selected_blocks_initial_entry_proof.json',
        'scripts/research_lil_kuhn_china_relocation_v2908.py','scripts/prepare_lil_kuhn_china_research_v2910.py',
        'scripts/verify_lil_kuhn_china_loader_v2911.py','scripts/verify_lil_kuhn_china_references_v2912.py',
        'scripts/reconcile_lil_kuhn_china_sampling_v2913.py','scripts/seal_lil_kuhn_china_references_v2914.py',
        'scripts/prove_lil_kuhn_china_controls_v2894.py','scripts/verify_lil_kuhn_china_fonts_v2904.py',
        'docs/editorial_testing_scope_v1870.md'}
    font=read(doc['native_font_proof']);deps.add(font['reused_proof'])
    for p in list(deps):
        if Path(p).suffix=='.json':
            item=read(p)
            for key in ['evidence','hashes']:
                if isinstance(item.get(key),dict):deps.update(p for p in item[key] if Path(p).is_file())
    for p in [doc['historical_representative_sheet_review'],doc['prior_current_sheet_review']]:deps.add(read(p)['sheet'])
    deps.update(s['path'] for s in font['review_sheets'])
    fe=read(doc['native_FE_font_proof']);deps.update(s['path'] for s in fe['review_sheets'])
    for panel in fe['cases']:deps.update([panel['native_plane'],panel['preview']])
    conf=dict(format='dk4-lil-kuhn-china-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],
        canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive)
    assert test.read_file(owned.PATH)==Path('work/analysis/lil_Kuhn_China_relocation_v2908/SC2_RESEARCH_ONLY.DK4').read_bytes()
    assert test.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin');save(ROOT/'positive_reconstruction.json',proof)
    negative=[]
    def reject(label,image,baseline,config):
        initial=(image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))
        try:owned.apply_release(image,baseline,config)
        except (AssertionError,ValueError):
            assert (image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))==initial
            negative.append(dict(case=label,rejected_before_mutation=True))
        else:raise AssertionError(label)
    reject('repeated_application',test,base,positive)
    for label,path in [('wrong_SC2',owned.PATH),('wrong_ARM9','/__arm9__.bin')]:
        image=NdsImage.open(PARENT);data=bytearray(image.read_file(path));data[256]^=1;image.replace_file(path,bytes(data));reject(label,image,base,positive)
    badbase=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');data=bytearray(badbase.read_file(owned.PATH));data[32]^=1;badbase.replace_file(owned.PATH,bytes(data));reject('wrong_canonical',NdsImage.open(PARENT),badbase,positive)
    def worker(d):return next(r for r in d['records'] if r['source_presentation_prefix_hex']=='38')
    def named(d):return next(r for r in d['records'] if '{MACRO:FI}' in r['english'])
    changes=[('missing_format_review',str(DOC),'manuscript',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('wrong_Japanese_source',str(DOC),'manuscript',lambda d:d['records'][0].update(source_hex='00')),
        ('wrong_consumer',str(DOC),'manuscript',lambda d:d['records'][0].update(native_display_consumer='original_FE_modal_5473C_mode1')),
        ('missing_printable_speaker',str(DOC),'manuscript',lambda d:worker(d).update(english=worker(d)['english'].replace('{SPEAKER:38}',''))),
        ('wrong_printable_speaker',str(DOC),'manuscript',lambda d:worker(d).update(english=worker(d)['english'].replace('SPEAKER:38','SPEAKER:5C'))),
        ('invented_macro',str(DOC),'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FI}')),
        ('changed_approved_prose',str(DOC),'manuscript',lambda d:d['records'][0].update(english='{SPEAKER:1F}My fleet was destroyed.')),
        ('missing_source_name_macro',str(DOC),'manuscript',lambda d:named(d).update(english=named(d)['english'].replace('{MACRO:FI}','Lil'))),
        ('wrong_complete_preamble',str(DOC),'manuscript',lambda d:d['records'][0].update(source_complete_preamble_hex='0040ffff005c')),
        ('missing_reference_approval',str(MAP),'reference_map',lambda d:d.update(external_references_complete=False)),
        ('wrong_mapped_command',str(MAP),'reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_relative_target',str(MAP),'reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=0)),
        ('missing_relocated_predicate_approval',str(MAP),'reference_map',lambda d:d.update(all40_relocated_native_predicates_preserve_source_semantics_and_mapped_cursor=False))]
    def FErow(d):return next(r for r in d['records'] if r['kind']=='system-FE')
    def FEname(d):return next(r for r in d['records'] if r['kind']=='system-FE' and '{MACRO:FI}' in r['english'])
    def xien(d):return next(r for r in d['records'] if r['source_presentation_prefix_hex']=='0a')
    changes.extend([
        ('FE_wrong_consumer',str(DOC),'manuscript',lambda d:FErow(d).update(native_display_consumer='original_progressive_54020')),
        ('FE_missing_null_actor_name_macro',str(DOC),'manuscript',lambda d:FEname(d).update(english=FEname(d)['english'].replace('{MACRO:FI}','Lil'))),
        ('FE_converted_selector',str(DOC),'manuscript',lambda d:FErow(d).update(source_hex='f8f2'+FErow(d)['source_hex'][2:])),
        ('FE_as_ordinary_actor_tag',str(DOC),'manuscript',lambda d:FErow(d).update(english=FErow(d)['english'].replace('SPEAKER:FE','SPEAKER:02'))),
        ('FE_missing_literal_label',str(DOC),'manuscript',lambda d:FEname(d).update(english=FEname(d)['english'].replace('Mysterious Woman: ',''))),
        ('missing_0A_actor_state',str(DOC),'manuscript',lambda d:xien(d).update(english=xien(d)['english'].replace('{SPEAKER:0A}',''))),
        ('wrong_legal_0A_actor_state',str(DOC),'manuscript',lambda d:xien(d).update(english=xien(d)['english'].replace('SPEAKER:0A','SPEAKER:02')))])
    for label,path,key,mutate in changes:
        value=read(path);mutate(value);mp=ROOT/(label+'.json');save(mp,value)
        cfg=deepcopy(conf);cfg[key]=str(mp);cfg['dependencies'][str(mp)]=sha(mp.read_bytes());cp=ROOT/(label+'_config.json');save(cp,cfg)
        reject(label,NdsImage.open(PARENT),base,cp)
    assert len(negative)==24;save(ROOT/'negative_cases.json',dict(cases=negative,all_rejected_before_mutation=True))
    stage=b'''    lil_kuhn_china = profile_config.get('lil_kuhn_china_editorial')
    if lil_kuhn_china:
        from dk4tool.patch.lil_kuhn_china_editorial import apply_release as apply_lil_kuhn_china

        lil_kuhn_china_report = apply_lil_kuhn_china(candidate, baseline, lil_kuhn_china)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_kuhn_china_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_kuhn_china_editorial'] = {
            'release_config': lil_kuhn_china,
            'release_config_sha256': sha256(Path(lil_kuhn_china).read_bytes()),
            'proof': lil_kuhn_china_report}
        kuhn_china_batch = Path(lil_kuhn_china_report['manuscript'])
        if kuhn_china_batch in release_batches:
            raise ValueError('Kuhn/China must run once after the complete V2883 stack')
        release_batches.append(kuhn_china_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_kuhn_china_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,conf)
    profile=deepcopy(registry['profiles']['all-routes-unified-v2883']);profile.update(lil_kuhn_china_editorial=owned.CONFIG,
        description='Full V2883 cumulative stack plus218 complete-context Kuhn/China speeches inSC2B51/B52/B53/B54/B55/B56/B146/B147/B148.',
        note='152 revisions/66 justified retentions;196 ordinary and22 FE complete native planes/1744 macro alignments plus872 final parity cases. Preserve501 commands/160 relative sites/800 relocated cases/40 relocated predicates/four exact event queries/336 whole loaders/two parent modes and exact shared representative rules. All28 sheets viewed,with one changed successor and24 exact reused sheets;89 row-count-only notes and no other waiver. Literal FE labels, null-actor FI and Xien0A state are separately proven. Preserve uncertain claims, private knowledge, identity reveal timing and Camille/Hodram interlude without invented relationships/ranks. No selected-scene activation or earned travel/funding/pact/battle is claimed. Registered build/exact clean patch/current startup pending. Experimental;preserve every ROM/translation;no promotion.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    pending=rp.with_name('release_stack_v2915_pending.json');assert not pending.exists();save(pending,registry)
    builder.write_bytes(after);os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v2883',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        negative_cases=24,all114accepted_layers_previous_profiles_and_V1492_promotion_unchanged=True,only_one_optional_stage_and_one_experimental_profile_added=True,
        release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),no_ROM_created_or_promoted=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('RegisteredV2916 optional218-speech stage afterfullV2883;24negative cases rejectbeforemutation. Allpreviousprofiles/114acceptedlayers/V1492promotion preserved.')
