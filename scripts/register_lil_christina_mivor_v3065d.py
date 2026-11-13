"""Register145 guarded ordinary/FE speeches after fullV3029 cumulative stack."""
import os
from pathlib import Path
from copy import deepcopy
from dk4tool.patch import lil_christina_mivor_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Christina_Mivor_registration_v3065d')
PROFILE='all-routes-unified-v3066'
PARENT=Path('out/all_routes_combined_v3029_candidate.nds')
DOC=Path('translations/lil_christina_mivor_editorial_manuscript_v8.json')
MAP=Path('translations/lil_christina_mivor_editorial_relocation_map_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent=NdsImage.open(PARENT);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapping=read(DOC),read(MAP)
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(MAP),str(Path(owned.__file__)),__file__,
        'dk4tool/dialogue/lil_christina_mivor_profile.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/lil_christina_mivor_layout_v2.py',
        doc['source_context'],doc['name_identity_contract'],'scripts/reconcile_lil_christina_mivor_names_v3039c.py',doc['control_contract'],doc['branch_proof'],doc['native_font_proof'],doc['native_FE_font_proof'],doc['representative_proof'],
        'scripts/verify_lil_christina_mivor_FE_v3047.py','scripts/lil_kuhn_china_FE_painter_v2909.py','scripts/approve_lil_christina_fonts_v3056.py',
        doc['historical_representative_sheet_review'],doc['prior_current_sheet_review'],doc['final_padding_proof'],
        mapping['source_plan'],mapping['source_census'],
        'work/analysis/lil_Christina_Mivor_reference_approval_v3064/approval_receipt.json',
        'work/analysis/lil_Christina_Mivor_loader_v3061/whole_SC2_and_two_selected_blocks_initial_entry_proof.json',
        'scripts/research_lil_christina_mivor_relocation_v3059.py','scripts/prepare_lil_christina_mivor_research_v3060.py',
        'scripts/verify_lil_christina_mivor_loader_v3061.py','scripts/verify_lil_christina_mivor_references_v3062.py',
        'scripts/reconcile_lil_christina_mivor_sampling_v3063.py','scripts/seal_lil_christina_mivor_references_v3064.py',
        'scripts/prove_lil_christina_mivor_controls_v3037.py','scripts/verify_lil_christina_mivor_fonts_v3055.py',
        'docs/editorial_testing_scope_v1870.md'}
    font=read(doc['native_progressive_proof']);deps.add(font['reused_proof']);deps.add(doc['native_progressive_proof'])
    for p in list(deps):
        if Path(p).suffix=='.json':
            item=read(p)
            for key in ['evidence','hashes']:
                if isinstance(item.get(key),dict):deps.update(p for p in item[key] if Path(p).is_file())
    for p in [doc['historical_representative_sheet_review'],doc['prior_current_sheet_review']]:deps.add(read(p)['sheet'])
    deps.update(s['path'] for s in read(doc['native_font_proof'])['all19_review_sheets'])
    fe=read(doc['native_FE_font_proof']);deps.update(s['path'] for s in fe['review_sheets'])
    for panel in fe['cases']:deps.update([panel['native_plane'],panel['preview']])
    conf=dict(format='dk4-lil-christina-mivor-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],
        canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive)
    assert test.read_file(owned.PATH)==Path('work/analysis/lil_Christina_Mivor_relocation_v3059/SC2_RESEARCH_ONLY.DK4').read_bytes()
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
    def worker(d):return next(r for r in d['records'] if r['source_presentation_prefix_hex']=='4f')
    def named(d):return next(r for r in d['records'] if '{MACRO:FI}' in r['english'])
    changes=[('missing_format_review',str(DOC),'manuscript',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('wrong_Japanese_source',str(DOC),'manuscript',lambda d:d['records'][0].update(source_hex='00')),
        ('wrong_consumer',str(DOC),'manuscript',lambda d:d['records'][0].update(native_display_consumer='original_FE_modal_5473C_mode1')),
        ('missing_printable_speaker',str(DOC),'manuscript',lambda d:worker(d).update(english=worker(d)['english'].replace('{SPEAKER:4F}',''))),
        ('wrong_printable_speaker',str(DOC),'manuscript',lambda d:worker(d).update(english=worker(d)['english'].replace('SPEAKER:4F','SPEAKER:07'))),
        ('invented_macro',str(DOC),'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FI}')),
        ('changed_approved_prose',str(DOC),'manuscript',lambda d:d['records'][0].update(english='{SPEAKER:1F}My fleet was destroyed.')),
        ('missing_source_name_macro',str(DOC),'manuscript',lambda d:named(d).update(english=named(d)['english'].replace('{MACRO:FI}','Lil'))),
        ('wrong_complete_preamble',str(DOC),'manuscript',lambda d:d['records'][0].update(source_complete_preamble_hex='0040ffff005c')),
        ('missing_reference_approval',str(MAP),'reference_map',lambda d:d.update(external_references_complete=False)),
        ('wrong_mapped_command',str(MAP),'reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_relative_target',str(MAP),'reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=0)),
        ('missing_relocated_predicate_approval',str(MAP),'reference_map',lambda d:d.update(all3_relocated_native_predicates_preserve_source_semantics_and_mapped_cursor=False))]
    def FErow(d):return next(r for r in d['records'] if r['kind']=='system-FE')
    def FEname(d):return next(r for r in d['records'] if r['kind']=='system-FE' and r['id']=='DK4_MES_B73_R0103')
    def cesare(d):return next(r for r in d['records'] if r['source_presentation_prefix_hex']=='a2')
    changes.extend([
        ('FE_wrong_consumer',str(DOC),'manuscript',lambda d:FErow(d).update(native_display_consumer='original_progressive_54020')),
        ('FE_invented_name_macro',str(DOC),'manuscript',lambda d:FEname(d).update(english=FEname(d)['english']+' {MACRO:FI}')),
        ('FE_converted_selector',str(DOC),'manuscript',lambda d:FErow(d).update(source_hex='f8f2'+FErow(d)['source_hex'][2:])),
        ('FE_as_ordinary_actor_tag',str(DOC),'manuscript',lambda d:FErow(d).update(english=FErow(d)['english'].replace('SPEAKER:FE','SPEAKER:02'))),
        ('FE_missing_source_Boy_label',str(DOC),'manuscript',lambda d:FEname(d).update(english=FEname(d)['english'].replace('Boy: ',''))),
        ('missing_A2_actor_state',str(DOC),'manuscript',lambda d:cesare(d).update(english=cesare(d)['english'].replace('{SPEAKER:A2}',''))),
        ('wrong_legal_A2_actor_state',str(DOC),'manuscript',lambda d:cesare(d).update(english=cesare(d)['english'].replace('SPEAKER:A2','SPEAKER:02')))])
    def FEsecond(d):return next(r for r in d['records'] if r['id']=='DK4_MES_B73_R0113')
    def crash(d):return next(r for r in d['records'] if r['id']=='DK4_MES_B73_R0119')
    changes.extend([
        ('FE_distinct_source_boy_body_swapped',str(DOC),'manuscript',lambda d:FEname(d).update(english=FEsecond(d)['english'])),
        ('FE_boy_invented_mother_label',str(DOC),'manuscript',lambda d:crash(d).update(english='{SPEAKER:FE}Mother: Help!')),
        ('missing_source_Boy_label_approval',str(MAP),'reference_map',lambda d:d.update(all3_FE_source_Boy_labels_preserved=False)),
        ('wrong_source_bound_formatter',str(DOC),'manuscript',lambda d:d.update(native_formatter_module='dk4tool/dialogue/encoder.py'))])
    for label,path,key,mutate in changes:
        value=read(path);mutate(value);mp=ROOT/(label+'.json');save(mp,value)
        cfg=deepcopy(conf);cfg[key]=str(mp);cfg['dependencies'][str(mp)]=sha(mp.read_bytes());cp=ROOT/(label+'_config.json');save(cp,cfg)
        reject(label,NdsImage.open(PARENT),base,cp)
    assert len(negative)==28;save(ROOT/'negative_cases.json',dict(cases=negative,all_rejected_before_mutation=True))
    stage=b'''    lil_christina_mivor = profile_config.get('lil_christina_mivor_editorial')
    if lil_christina_mivor:
        from dk4tool.patch.lil_christina_mivor_editorial_v2 import apply_release as apply_lil_christina_mivor

        lil_christina_mivor_report = apply_lil_christina_mivor(candidate, baseline, lil_christina_mivor)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_christina_mivor_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_christina_mivor_editorial'] = {
            'release_config': lil_christina_mivor,
            'release_config_sha256': sha256(Path(lil_christina_mivor).read_bytes()),
            'proof': lil_christina_mivor_report}
        christina_mivor_batch = Path(lil_christina_mivor_report['manuscript'])
        if christina_mivor_batch in release_batches:
            raise ValueError('Christina/Mivor must run once after the complete V3029 stack')
        release_batches.append(christina_mivor_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_christina_mivor_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,conf)
    profile=deepcopy(registry['profiles']['all-routes-unified-v3029']);profile.update(lil_christina_mivor_editorial=owned.CONFIG,
        description='Full V3029 cumulative stack plus145 complete-context Christina recruitment andMivor harbor-rescue speeches inSC2B72/B73.',
        note='130revisions/15justifiedretentions;142ordinary/3source-labeled BoyFE panels;1160logical-compiled/580finalparity macro cases.236commands/12sites/60relocatedcases/3predicates/noqueries/nochoices/336wholeloaders/twoparents. Registered Mivor Genz spelling,source-proven grandfather,firm marriage refusals,initial fear-wins andlaterlove-wins comparisons preserved. No invented rescue kinship,gift identity,permanent swimming skill ormutual consent. Original name-ring scratch writes bounded/restored;no nameasset edit. Ninechanged planes/72cases rerun,133/1064reused with exactEnglish/source/runtime/bytes/hashes. All19final sheets viewed;51row-count-only notes.28compiler negatives reject beforemutation. No selected-scene,newnameplate or earned progress claim. Registeredbuild/exactpatch/currentstartup pending. Experimental;preserve everyROM/translation;no promotion.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    pending=rp.with_name('release_stack_v3065d_pending.json');assert not pending.exists();save(pending,registry)
    builder.write_bytes(after);os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v3029',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        negative_cases=28,all114accepted_layers_previous_profiles_and_V1492_promotion_unchanged=True,only_one_optional_stage_and_one_experimental_profile_added=True,
        release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),no_ROM_created_or_promoted=True,
        preserved_failed_registration_producers=['scripts/register_lil_christina_mivor_v3065.py','scripts/register_lil_christina_mivor_v3065b.py','scripts/register_lil_christina_mivor_v3065c.py'],prior_failures_before_any_ROM_or_registry_mutation=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('RegisteredV3066 optional145-speech stage afterfullV3029;28negativecasesrejectbeforemutation. Previousprofiles/114acceptedlayers/V1492promotion preserved.')
