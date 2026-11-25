"""Reversibly update the existing13-record family;add no duplicate editorial credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.retrospective_B218_final_paths_v7853 import *
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_completion_v7862')
VERIFY=Path('work/analysis/editorial_handoff_verification_v7863')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7852/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
RELEASE=Path('work/analysis/retrospective_B218_release_v7858/registered_release_verification.json')
START=Path('work/analysis/retrospective_B218_startup_binding_v7860/own_Lil_startup_andstrict_current_context.json')
START_VIEW=Path('work/analysis/retrospective_B218_startup_view_v7861/own_registered_Lil_startup_sheet_viewed.json')
ATOMIC=Path('work/analysis/retrospective_B218_atomic_challenges_v7855/atomic_validation_receipt.json')
FINAL=Path('translations/lil_B218_retrospective_contextual_final_review_v1.json')
LEADS=Path('work/analysis/completed_contraction_wrap_leads_v7831/completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json')
KEY='Lil_SC2B218_retrospective_layout_completion_v7862'
SCOPE='unfinished_editorial_scope_v7862'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
VALUES=(6938,6941,6941,4347,2591)
SUMMARY="""Lil's retrospective B218 R27 wrap refinement is integrated in registered cumulative V7857. The private aside now displays (Ian's interested? / That's a surprise.), keeping the short final thought together. All 13 existing English wordings were reread against the complete clean Japanese exchange and retained with individual reasons. Only one automatic wrap changes; the other 12 stored speech bodies remain exact. No words, punctuation, source controls, selectors, substitutions, font or 216px/four-row geometry change.

The completed family is updated in place, with exact source, V7821 predecessor, compiled/stored, actual and V7857 integrated references in translations/lil_B218_retrospective_contextual_final_review_v1.json. This formatting revisit adds zero source/prose, completion, wording-revision or retention credit. Counts remain 6,938 completed / 6,941 source-prose and drafts / 4,347 integrated wording revisions / 2,591 retentions. SC0 135, SC1 91, SC2 4,915, SC3 197 and COMMON 1,600 remain; COMMON has three source-prose drafts. Route 5,338/5,338 is only a subset.

V7857 retains the complete V7821 stack plus this reviewed layer: 632 batches, 114 accepted layers, 18 passing registered release checks and 110 regressions. Its whole ROM equals the reviewed reference. The clean-input xdelta patch reconstructs it byte for byte. Main V4701 and all earlier profiles, ROMs, translations, drafts, producers and proofs remain. No separate unified test package, promotion, pruning, commit or push occurred.

The changed logical/previous/proposed paragraph passes 12 current processor alignment cases and two complete before/after native planes; its zero-ink stored parity tail passes four more cases and an exact plane. All 13 final dispatches retain actors2/21, voices3/1 and zero macros. All 15 original commands and 13 complete preambles remain. B218 changes 1016/logical1016/tail0 to 1020/logical1018/tail2. Original eight-byte A000 00a0ffff2e000110 and the four-byte normal end remain; 25 isolated seeded ends preserve type0/value carry. Opaque structural bridging is not full effect mechanics. Both clean/predecessor block inverses and the full predecessor archive inverse are exact; all 335 other SC2 blocks and all other files/components remain unchanged. Original 336 loads/cache hits, 672 parent modes and bounded shipped callers pass.

Two fresh previous/proposed English initialized scenes each run 16,001 frames with the same nine original B22 initializers, all 15 B218 commands, ordinary inputs and read-only observation. All 13 speeches in each provide 26 complete pages and 102 body/nameplate holds, zero partial sampled holds and no unreturned commands. All 26 exact panes/eight sheets were viewed. Lil Argot/Ian Dukov headers and 13 paired upper scenes/portraits/nameplates agree. Both exits are5975; all24 results/UI agree. Eight comparison rows differ only in decoded lengths/relocated offsets. Durations, all167 sampled later RGB frames, five final components, whole actors and seed3000421369 agree. Preserve raw measurements and every-frame/full-RAM/future/causal/full-mechanics/natural-location/activation/full-route/hardware limits. No new Japanese capture or incidental navigation/sailing prose credit is claimed.

The frozen source-bound formatting policy passes 13 positives and 221 actual-changing rejections without warnings or waivers; nine individual row-count infos remain justified. Atomic production passes an exact whole-ROM positive and 128 actual-changing corruptions with production dependency checks bypassed; every corruption rejects before any final files-list commit. A fresh own-V7857 Lil startup matches all six prior whole-RGB frames and whole-actor/captain2 controls and supplies a strict own-ROM native snapshot. Unaffected route startup evidence is retained without replay.

One of the 13 retrospective contraction-wrap candidates is now integrated. The other 12 are rebound offline to V7857 by unchanged block bytes and remain editorial candidates, not automatic defects. The markup-only scan covered 558/6938 records; extend it through exact current consumers. The original 151-159 水夫/Sailor progressive-name retention remains separate from 配下/Retainer full-name and other consumers. Continue all 207 names/roles/aliases, all four storylines and earlier translated dialogue, broad practical shared shop/town/random capture, Help and remaining prose. Keep graphics/all18 plaques and the later older-record technical re-audit separate."""
NEXT="""Continue the full editorial goal from verified V7863/current V7857. The B218 retrospective R27 wrap is integrated; do not repeat its unchanged source/gloss/native/stored/controls/inverse/loaders/callers/paired scenes/visual/policy/atomic/build/regression/patch/startup checks. Use work/analysis/current_V7857_Lil_native_v7860/current_native_input.json for further Lil native work. Maria's own captain3 snapshot remains V7821 at work/analysis/current_V7821_native_v7824/route3/current_native_input.json; it is historical to V7857. Obtain each route's own current context when needed; never substitute another route's RAM or relabel older captures as current.

Review the remaining 12 contraction/question-tag candidates as complete clean/current exchanges, measuring alternatives under their exact consumers. The first558-plan scan is not whole-goal wrap coverage. Retain ordinary complete-word wraps with individual reasons and extend coverage through exact current native boundaries and substitutions; use no global keep-together rule, manual line breaks or warning waiver.

Continue all four storylines, earlier translations, practical broad shop/town/random scenes, Help and all remaining player-facing prose, all207 names/roles/aliases and every earlier unfinished inventory/counterpart/item/display lead. Retain the source-supported 151-159 Sailor nameplates; review their separate full-name/indirect/typed/COMMON/UI consumers. Keep all measured older scene limits and the normal-end value-carry/source-only nineteenth-cell findings for the later older-record technical re-audit. Preserve all ROMs, translations, drafts, failed producers and proofs. Graphics/all18 plaques remain separate. MainV4701 stays unchanged; no canceled separate unified package, automatic promotion, pruning, commit or push."""
def digest(value):return sha(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['kind']=='append':
            assert len(parent[key])==op['before_length']+op['count'] and digest(parent[key][op['before_length']:])==op['appended_sha256']
            del parent[key][op['before_length']:]
        elif op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result
def gates():
    release,start,view,atomic,seal=map(read,[RELEASE,START,START_VIEW,ATOMIC,SEAL])
    assert release['candidate_sha256']==start['candidate_sha256']==view['candidate_sha256']==sha(Path(release['candidate']).read_bytes())
    manifest=read(release['manifest']);registry=read('translations/release_stack.json')
    assert manifest['profile']=='all-routes-unified-v7857' and len(manifest['batches'])==632 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert release['all110_release_dialogue_regressions_pass'] and release['whole_clean_input_ROM_reconstruction_byte_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256'] and Path(release['exact_patch_reconstruction']).read_bytes()==Path(release['candidate']).read_bytes()
    assert start['all_prior_whole_RGB_actor_andcaptain_controls_equal'] and start['actual_captain']==2 and start['whole_RGB_pair_count']==6
    assert start['all_strict2b6_COMMON_directory_and123264_payload_guards_pass'] and view['viewed'] and view['startup_proof_sha256']==sha(START.read_bytes())
    assert atomic['positive_records']==13 and atomic['changed_records']==1 and atomic['negative_count']==128 and atomic['all_negatives_reject_before_any_files_list_commit']
    assert atomic['all_dependency_digests_deliberately_bypassed'] and seal['manuscript_sha256']==sha(SEALED.read_bytes())
    return release
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    release=gates()
    if mode=='stage':
        assert not ROOT.exists() and not FINAL.exists()
        before=LEDGER.read_bytes();old=json.loads(before);prior=read(PRIOR)
        assert sha(before)==prior['ledger_sha256'] and KEY not in old and tuple(old[k] for k in COUNTERS)==VALUES
        assert old['goal_status']=='active' and not old['full_goal_complete']
        doc,mapping=map(read,[SEALED,MAP]);actual=read(proofs()['actual']);g=mapping['groups'][0]
        image=NdsImage.open(release['candidate']);bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;block=bank[218]
        fi,family=next((i,f) for i,f in enumerate(old['completed_editorial_families']) if f.get('file_path')=='/data/SC2.DK4' and f.get('blocks')==[218])
        assert len(family['records'])==13 and family['revised_count']==6 and family['retained_count']==7
        previous={r['id']:r for r in family['records']};panels={p['id']:p for p in actual['groups'][1]['panels']}
        catalogue=read(proofs()['stored_controls'])['offline_catalogue_binding']['records']
        keys={bytes.fromhex(v['key_hex']) for v in catalogue if v['route_mask']&4};rows=[]
        assert sha(block)==g['target_block_sha256']
        for source in doc['records']:
            row=deepcopy(source);ident=row['id'];ref=next(r for r in g['text_records'] if r['id']==ident)
            raw=bytes.fromhex(ref['target_hex']);oldraw=bytes.fromhex(ref['old_hex']);at=ref['new_offset']
            assert row['english']==previous[ident]['english'] and block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==ref['new_record_index']
            assert oldraw[1:] not in keys
            current_command=next(c for c in mapping['current_packet']['all_current_commands'] if c['offset']==ref['old_offset']-5)
            target_command=next(c for c in g['all_target_commands'] if c['offset']==at-5)
            row.update(previous_completed_record=deepcopy(previous[ident]),previous_completed_final_review=family['final_review'],
                current_native_extent=current_command['native_extent'],
                predecessor_effective_reference=deepcopy(ref['current_reference']),
                current_raw_storage_English=oldraw[1:].decode('cp932'),
                current_effective_paragraph=' '.join(oldraw[1:].decode('cp932').split()),
                current_effective_runtime_template_hex=oldraw[1:].hex(),current_expanded_runtime_hex=oldraw[1:].hex(),
                current_registered_catalogue_match=None,
                integrated_reference=dict(file_path='/data/SC2.DK4',block=218,offset=at,bytes=len(raw),
                    record_index=ref['new_record_index'],header_offset=at-5,stored_hex=raw.hex(),block_sha256=sha(block),
                    ROM=release['candidate'],ROM_sha256=release['candidate_sha256']),
                integrated_hex=raw.hex(),integrated_command_extent=target_command['native_extent'],
                current_stored_English=raw[1:].decode('cp932'),current_effective_runtime_English=raw[1:].decode('cp932'),
                completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],
                registered_integration_pending=False,atomic_registered_release_andmetadata_completion_pending=False,
                retrospective_no_duplicate_credit=True,source_prose_orcompletion_credit_added_here=0,
                actual_complete_display_proof=proofs()['actual'],actual_complete_body_holds=len(panels[ident]['complete_body_andheader_holds']),
                actual_complete_name_holds=len(panels[ident]['complete_body_andheader_holds']),
                status='retrospective-auto-wrap-registered-integrated-no-duplicate-credit')
            rows.append(row)
        assert {historical_key(r) for r in rows}=={historical_key(r) for r in family['records']}
        leads=read(LEADS);remaining=[]
        for lead in leads['leads']:
            if lead['file_path']=='/data/SC2.DK4' and lead['id']=='DK4_MES_B218_R0027':continue
            b=IlnkContainer.parse(image.read_file(lead['file_path'])).blocks[lead['block']]
            original=next(x for x in leads['source_current_native_groups'] if x['file_path']==lead['file_path'] and x['block']==lead['block'])
            assert sha(b)==original['current_block_sha256'];ref=lead['current_reference'];value=bytes.fromhex(ref['raw_hex']);at=ref['offset']
            assert b[at:at+len(value)+1]==value+b'\0' and b[at-5:at+1].hex()==ref['complete_preamble_hex']
            remaining.append(dict(file_path=lead['file_path'],id=lead['id'],block=lead['block'],current_reference=deepcopy(ref),
                current_ROM=release['candidate'],current_ROM_sha256=release['candidate_sha256'],block_sha256=sha(b),
                original_lead_packet=str(LEADS),original_lead_packet_sha256=sha(LEADS.read_bytes()),
                offline_exact_block_rebinding_not_new_gameplay_orfinal_editorial_judgment=True))
        assert len(remaining)==12
        ROOT.mkdir(parents=True);rp=ROOT/'remaining12_contraction_wrap_leads_rebound_offline_to_V7857.json'
        save(rp,dict(records=remaining,one_B218_candidate_integrated=True,new_credit=0,full_goal_complete=False))
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,SEALED,MAP,SEAL,RELEASE,START,START_VIEW,ATOMIC,rp,*proofs().values(),Path(__file__)]}
        save(FINAL,dict(format='dk4-retrospective-contextual-final-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
            previous_final_review=family['final_review'],previous_final_review_sha256=sha(Path(family['final_review']).read_bytes()),
            candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],records=rows,
            wording_retentions=13,automatic_wrap_revisions=1,unchanged_stored_records=12,
            source_prose_completion_wording_revision_andretention_credit_added=0,
            actual_two_English_scenes_pages=26,actual_complete_body_andheader_holds=102,
            historical_Japanese_capture_not_relabelled_as_new=True,all_measured_limits_full_goal_and207_names_preserved=True,
            new_registered_startup_runs=1,new_registered_startup_frames=4001,evidence=evidence,summary=SUMMARY,full_goal_complete=False))
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(kind='set',path=path,existed=existed,before=deepcopy(parent[key]) if existed else None));parent[key]=deepcopy(value)
        def append(path,values):
            parent,key=parent_at(new,path);ops.append(dict(kind='append',path=path,before_length=len(parent[key]),count=len(values),appended_sha256=digest(values)))
            parent[key].extend(deepcopy(values))
        put(['completed_editorial_families',fi,'records'],rows)
        for key,value in dict(previous_contextual_final_review=family['final_review'],final_review=str(FINAL),
            retrospective_wording_retentions=13,retrospective_automatic_wrap_revisions=1,retrospective_new_editorial_credit=0).items():
            put(['completed_editorial_families',fi,key],value)
        for key,value in dict(latest_retrospective_layout_review=KEY,latest_retrospective_manuscript=str(SEALED),latest_retrospective_final_review=str(FINAL)).items():
            put(['contextual_story_natural_dialogue_pass_v1871',key],value)
        current=deepcopy(new['current_integrated_candidate']);current.update(path=release['candidate'],sha256=release['candidate_sha256'],
            profile=release['profile'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
            ARM9_sha256=release['ARM9_sha256'],MESFILE_sha256=release['COMMON_sha256'],details=SUMMARY,status='experimental-verified-editorial-checkpoint-not-promoted')
        current.update({f'SC{i}_sha256':release['story_hashes'][f'SC{i}'] for i in range(4)})
        put(['current_integrated_candidate'],current);put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        for pending in ['retrospective_B218_predicate_layout_pending_v7834','retrospective_B218_native_actual_policy_pending_integration_v7851']:
            put([pending,'registered_integration_completed_by'],dict(checkpoint=KEY,final_review=str(FINAL),candidate=release['candidate'],
                all_historical_pending_flags_superseded_not_deleted=True,new_credit=0))
        put(['formatting_watchlist',KEY],dict(status='one-automatic-wrap-integrated-13-wordings-retained-no-duplicate-credit',
            final_review=str(FINAL),remaining12_wrap_leads=str(rp),full_goal_complete=False))
        ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');put(['coverage_units',ri,'next'],NEXT)
        append(['coverage_units'],[dict(id=KEY,file_path='/data/SC2.DK4',block=218,status='retrospective-formatting-integrated',
            reviewed_existing_records=13,automatic_wrap_revisions=1,new_completed_records=0,new_credit=0,final_review=str(FINAL))])
        oldscope=old['unfinished_editorial_scope_v7851'];assert sha(Path(oldscope['path']).read_bytes())==oldscope['sha256']
        inventory=deepcopy(read(oldscope['path']));inventory['next_focus']=NEXT
        inventory[KEY]=dict(final_review=str(FINAL),registered_candidate=release['candidate'],one_wrap_integrated=True,
            wording_retentions=13,new_credit=0,remaining12_wrap_candidates=str(rp),all_prior_leads_andfull_scope_preserved=True)
        for pending in ['retrospective_B218_predicate_layout_pending_v7834','retrospective_B218_native_actual_policy_pending_integration_v7851']:
            if pending in inventory:inventory[pending]['registered_integration_completed_by']=dict(checkpoint=KEY,final_review=str(FINAL),new_credit=0)
        scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_andfull_scope_preserved=True,new_credit=0,full_goal_complete=False))
        evidence[str(FINAL)]=sha(FINAL.read_bytes());evidence[str(scope)]=sha(scope.read_bytes())
        new[KEY]=dict(summary=SUMMARY,next=NEXT,final_review=str(FINAL),evidence=evidence,inverse_operations=ops,
            existing_family_updated=family['id'],wording_retentions=13,automatic_wrap_revisions=1,new_credit=0,
            new_registered_ROM_startup_runs=1,new_registered_ROM_startup_frames=4001,goal_turn_classification='progress',full_goal_complete=False)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==VALUES
        assert {historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}=={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
        assert new['completed_editorial_record_counts_by_file']==old['completed_editorial_record_counts_by_file']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V7862: Lil retrospective wrap integrated in V7857; full editorial goal continues\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;prefix=('# Current editorial handoff - V7862; V7857 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_completion.json',dict(files=files,evidence=evidence,zero_duplicate_credit=True,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six retrospective completion targets staged;13 existing family records updated/one wrap/zero new credit.Deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_completion.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==VALUES and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,value in plan['evidence'].items():assert sha(Path(path).read_bytes())==value
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_completion.json').read_bytes()),
                deep_inverse_recovers_every_prior_root_family_record_counter_andROM=True,zero_duplicate_credit=True,full_goal_complete=False))
            print('Deep inverse/all six before-planned hashes/evidence pass;every prior value recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_completion.json').read_bytes())
            workspace=Path.cwd().resolve()
            for entry in plan['files']:assert Path(entry['target']).is_relative_to(workspace) and Path(entry['planned']).is_relative_to(ROOT.resolve())
            for entry in plan['files']:
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,zero_duplicate_credit=True,current=release['candidate'],full_goal_complete=False))
            print('Six audited retrospective completion targets applied;V7857 current/6938 counts unchanged.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_hash_exact']
            completed={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']};assert len(completed)==6938
            verified=deepcopy(read(PRIOR));verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],profile=release['profile'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=release['manifest'],
                manifest_batches=632,accepted_layers=114,release_checks=18,regressions=110,
                retrospective_B218_R27_layout_pending=False,retrospective_B218_native_actual_policy_complete=True,
                retrospective_B218_layout_registered_integrated=True,retrospective_wrap_candidates_remaining=12,
                strict_own_Lil_current_input=read(START)['strict_current_native_input'],
                final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),latest_completion=KEY,
                unfinished_scope=SCOPE,next_required=NEXT,new_credit=0,new_emulator_runs=1,new_actual_frames=4001,
                all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV7863/currentV7857:one wrap integrated/13 wordings retained/zero duplicate credit;6938 completed.Fullobjective active.')
