"""Validate one formatting correction and register it after the complete V4966 stack."""
from pathlib import Path
from copy import deepcopy
import json,os
from dk4tool.patch import earlier775_reflow_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/earlier775_registration_v4986')
DOC=Path('translations/earlier_common_wraps_editorial_manuscript_v2.json')
PARENT=Path('out/all_routes_combined_v4966_candidate.nds')
PROFILE='all-routes-unified-v4987'
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    verified=Path('work/analysis/editorial_handoff_verification_v4982/verified_handoff.json');v=read(verified)
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==v['ledger_sha256'] and sha(PARENT.read_bytes())==v['candidate_sha256']
    image=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc=read(DOC)
    ap=Path('work/analysis/earlier_common_wraps_approval_v4979/four_retentions_one_reflow_source_native_approval.json');a=read(ap)
    native=Path(doc['source_context_proof']);copies=Path('work/analysis/earlier_common_wraps_copies_v4980/all7336_native_copies_and_letter_sequences.json');actual=Path(doc['postscene_native_state_proof'])
    deps={str(p) for p in [DOC,ap,native,copies,actual,verified,Path(__file__),Path(owned.__file__).relative_to(Path.cwd()),
        Path('dk4tool/dialogue/earlier_market_letters_reflow_v2.py'),Path('dk4tool/dialogue/review.py'),
        Path('work/analysis/earlier_common_wraps_glosses_v4976/four_clean_source_glosses_before_English.json'),
        Path('work/analysis/earlier_common_wraps_clean_v4975/clean_only_target_and_neighbor_records.json'),
        Path('work/analysis/recommendation_focus_tools_v4983/prepared_reference_and_fixture_tools.json'),
        Path('work/analysis/recommendation_actual_verification_v4985/sealed_manuscript_receipt.json')]}
    registry_path,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');rb,bb=registry_path.read_bytes(),builder.read_bytes();registry=read(registry_path)
    excluded={p.resolve() for p in [registry_path,builder,Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),
        *[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
    pending=list(deps);seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        if Path(p).suffix!='.json':continue
        data=read(p)
        if not isinstance(data,dict):continue
        for key in ['evidence','dependencies']:
            if not isinstance(data.get(key),dict):continue
            for item in data[key]:
                if Path(item).is_file() and Path(item).resolve() not in excluded and item not in deps:deps.add(item);pending.append(item)
    for row in read(native)['records']:deps.update(c['preview'] for c in row['native_cases'])
    deps.update([a['viewed_sheet'],read(actual)['review_sheet']])
    conf=dict(format='dk4-earlier775-reflow-release-v1',manuscript=str(DOC),source_ARM9_sha256=a['source_ARM9_sha256'],
        source_COMMON_sha256=a['source_COMMON_sha256'],target_COMMON_sha256=a['target_COMMON_sha256'],directory_sha256=a['directory_sha256'],
        canonical_COMMON_sha256=sha(baseline.read_file(owned.PATH)),clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        native_proof=str(native),native_approval=str(ap),copy_proof=str(copies),actual_approval=str(actual),
        source_text_hex=doc['records'][-1]['current_hex'],target_text_hex=doc['records'][-1]['target_hex'],dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,positive)
    assert test.read_file(owned.PATH)==Path(a['target_COMMON']).read_bytes() and len(proof['changed_records'])==1
    save(ROOT/'positive_reconstruction.json',proof);negatives=[];original_load=owned.load
    def reject(label,path,edit):
        test=NdsImage.open(PARENT);before=[test.read_file(p) for p in [owned.PATH,'/__arm9__.bin']]
        value=deepcopy(read(path));old=deepcopy(value);edit(value);assert value!=old,label
        def changed(p):return deepcopy(value) if Path(p)==Path(path) else original_load(p)
        owned.load=changed
        try:
            try:owned.apply_release(test,baseline,positive)
            except (ValueError,AssertionError,KeyError) as error:negatives.append(dict(case=label,rejected=True,reason=str(error)))
            else:raise AssertionError('Accepted negative:'+label)
        finally:owned.load=original_load
        assert before==[test.read_file(p) for p in [owned.PATH,'/__arm9__.bin']],label
    for key in ['format','source_ARM9_sha256','source_COMMON_sha256','target_COMMON_sha256','canonical_COMMON_sha256','clean_ROM_sha256']:
        reject('config-'+key,positive,lambda d,k=key:d.update({k:'0'*64}))
    reject('dependency-hash',positive,lambda d:d['dependencies'].update({str(DOC):'0'*64}))
    for gate in ['source','context','localization','naturalness','formatting']:reject('missing-'+gate,DOC,lambda d,g=gate:d['records'][3]['review'].update({g:False}))
    mutations=[
        ('missing-record',DOC,lambda d:d['records'].pop()),
        ('wrong-English',DOC,lambda d:d['records'][3].update(english='Different words.{PAD}')),
        ('authored-break',DOC,lambda d:d['records'][3].update(english=d['records'][3]['english']+'{LB}')),
        ('wrong-current',DOC,lambda d:d['records'][3].update(current_hex='00')),
        ('wrong-Japanese',DOC,lambda d:d['records'][3].update(source_hex='00')),
        ('wrong-reference',DOC,lambda d:d['records'][3]['current_reference'].update(offset=0)),
        ('lost-retention-reason',DOC,lambda d:d['records'][0].update(fresh_retained_wording_justification='')),
        ('lost-layout-reason',DOC,lambda d:d['records'][2].update(layout_review_reason='')),
        ('changed-774-layout',DOC,lambda d:d['records'][2].update(target_hex='00')),
        ('lost-actual-scope',DOC,lambda d:d['records'][3].update(actual_recommendation_branch_observed=False)),
        ('duplicate-credit',DOC,lambda d:d.update(source_prose_or_completion_credit_added=1)),
        ('wrong-target',positive,lambda d:d.update(target_text_hex='00')),
        ('missing-native-case',native,lambda d:d['records'][3]['native_cases'].pop()),
        ('lost-first-glyph',native,lambda d:d['records'][3]['native_cases'][1].update(complete_leading_internal_final_glyphs_and_bounds=False)),
        ('extra-page',native,lambda d:d['records'][3]['native_cases'][1].update(all_source_bytes_consumed_one_native_page=False)),
        ('wrong-native-target',native,lambda d:d['records'][3]['native_cases'][1].update(compiled_hex='00')),
        ('missing-copy',copies,lambda d:d['cases'].pop()),
        ('lost-774-partition-proof',ap,lambda d:d['intro774_exhaustive_complete_word_partitions_at1_2_3_rows']['3'].append(['invented'])),
        ('unviewed-native',ap,lambda d:d.update(all8_current_and_reviewed_complete_native_planes_viewed=False)),
        ('unviewed-actual',actual,lambda d:d.update(ten_full_screens_viewed=False)),
        ('wrong-original-sequence',actual,lambda d:d.update(actual_original_reward_sequence=[774,779,766])),
        ('concealed-input-fixture',actual,lambda d:d.update(input_fixtures_are_counterfactual_not_earned_large_sale_share_inventory_qualification_or_letter=False)),
        ('wrong-quantity-disclosure',actual,lambda d:d['versions'][0]['qualification_input_fixture'].update(original_sale_hold_total=16)),
        ('wrong-fixture-PC',actual,lambda d:d['versions'][0]['qualification_input_fixture'].update(PC=0x020BBCA8)),
        ('incomplete-actual-plane',actual,lambda d:d['versions'][1]['holds'][0].update(complete_ink_and_blank_paper_match=False)),
        ('different-state',actual,lambda d:d['native_final_component_equality'].update(models=False)),
        ('wrong-donor-captain',actual,lambda d:d.update(actual_donor_captain_IDs=[2,2])),
        ('wrong-RNG',actual,lambda d:d.update(PRNG_equal=False)),
        ('changed-timing',actual,lambda d:d['versions'][1]['all_font_rows'][0].update(frame=0)),
        ('different-return',actual,lambda d:d.update(whole_final_RGB_equal=False)),
    ]
    for label,path,edit in mutations:reject(label,path,edit)
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_any_image_mutation=True,producer_sha256=sha(Path(__file__).read_bytes())))
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    stage=b'''    earlier775 = profile_config.get('earlier775_reflow')
    if earlier775:
        from dk4tool.patch.earlier775_reflow_v1 import apply_release as apply_earlier775

        earlier775_report = apply_earlier775(candidate, baseline, earlier775)
        grouped.setdefault('/COMMON/MESFILE.DK4', [])
        changed_records.setdefault('/COMMON/MESFILE.DK4', []).append('COMMON_MESSAGE_775')
        relocation_checks.setdefault('/COMMON/MESFILE.DK4', {})['earlier775_reflow'] = {
            'release_config': earlier775,
            'release_config_sha256': sha256(Path(earlier775).read_bytes()),
            'proof': earlier775_report}
        more_batch = Path(earlier775_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('Earlier775 reflow must run once after the full V4966 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert bb.count(anchor)==1 and b"profile_config.get('earlier775_reflow')" not in bb
    after=bb.replace(anchor,stage+anchor,1);compile(after,str(builder),'exec')
    profile=deepcopy(registry['profiles']['all-routes-unified-v4966']);profile.update(status='experimental',earlier775_reflow=owned.CONFIG,
        description='Full V4966 stack plus one exact-allocation775 formatting correction:four to three rows,every word retained.682/764/774 keep their individually justified exact layouts. Paired12001-frame disclosed reward-input cold boots preserve original775->780->766 and town return;not earned reward eligibility. Zero duplicate editorial credit.',
        note='Native,copy and representative transition approved;registered build,patch and startup pending.')
    registry['profiles'][PROFILE]=profile
    (ROOT/'release_stack.before.json').write_bytes(rb);(ROOT/'build_integrated_release.py.before').write_bytes(bb);save(owned.CONFIG,conf)
    assert registry_path.read_bytes()==rb and builder.read_bytes()==bb
    temp=builder.with_name('build_integrated_release_v4986.tmp');assert not temp.exists();temp.write_bytes(after);os.replace(temp,builder)
    data=(json.dumps(registry,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    with registry_path.open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
    check=deepcopy(read(registry_path));check['profiles'].pop(PROFILE);assert check==json.loads(rb) and builder.read_bytes().replace(stage,b'',1)==bb
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v4966',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        registry_before_sha256=sha(rb),registry_after_sha256=sha(registry_path.read_bytes()),builder_before_sha256=sha(bb),builder_after_sha256=sha(builder.read_bytes()),
        negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(negatives),all_negatives_reject_before_mutation=True,
        expected_manifest_batches=566,accepted_layers=114,main_V4701_unchanged=True,new_editorial_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(registered=PROFILE,negative_cases=len(negatives),expected_manifest_batches=566,accepted_layers=114,new_editorial_credit=0))
