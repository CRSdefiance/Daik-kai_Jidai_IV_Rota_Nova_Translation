"""Independently audit staged/live progress, exact references and whole inverses."""
import re,sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_checkpoint_v8887')
KEY='Hodram_SC1B61_B70_224_source_native_current_bound_first44_prose_180_pending_v8887'
SCOPE='unfinished_editorial_scope_v8887'
LEDGER=Path('translations/editorial_review_current_v1.json')
COUNTERS={'records_editorially_completed':7319,'records_with_source_and_prose_pass':7322,'records_with_source_prose_drafts':7322,
    'records_revised_and_integrated':4538,'retained_wordings_editorially_completed':2781}

def audit(mode):
    manifest=read(ROOT/'stage_manifest.json');before=read(ROOT/'ledger_before.json');staged=read(ROOT/'ledger_staged.json')
    assert sha((ROOT/'ledger_before.json').read_bytes())==manifest['ledger_before_sha256']
    assert sha((ROOT/'ledger_staged.json').read_bytes())==manifest['ledger_staged_sha256']
    previous=read(manifest['previous_verified_handoff'])
    assert previous['pass'] and previous['ledger_sha256']==manifest['ledger_before_sha256']
    assert sha(Path(manifest['previous_verified_handoff']).read_bytes())==manifest['previous_verified_handoff_sha256']
    for p,digest in {**manifest['evidence'],**manifest['protected_files']}.items():assert sha(Path(p).read_bytes())==digest,p
    for k,v in COUNTERS.items():assert before[k]==staged[k]==v
    assert staged['goal_status']==before['goal_status']=='active' and not staged['full_goal_complete']
    assert staged['current_integrated_candidate']==before['current_integrated_candidate']
    assert staged['completed_editorial_families']==before['completed_editorial_families']
    inverse=deepcopy(staged)
    assert KEY not in before and SCOPE not in before
    inverse.pop(KEY);descriptor=inverse.pop(SCOPE);inverse['latest_checkpoint']=before['latest_checkpoint']
    added=inverse['research_checkpoints'].pop()
    assert added['id']=='V8887-Hodram-B61-B70-source-native224-first44-prose' and added['new_editorially_completed']==0
    assert inverse==before
    scope_before=read(ROOT/'scope_before.json');scope=read(descriptor['path'])
    assert sha((ROOT/'scope_before.json').read_bytes())==manifest['scope_before_sha256']
    assert sha(Path(descriptor['path']).read_bytes())==descriptor['sha256']
    assert scope.pop(KEY)==staged[KEY] and scope==scope_before
    assert read(manifest['scope_before_path'])==scope_before
    for d in manifest['documents']:
        old,planned=Path(d['before']).read_bytes(),Path(d['staged']).read_bytes()
        assert sha(old)==d['before_sha256'] and sha(planned)==d['staged_sha256']
        assert planned[d['prefix_bytes']:]==old and planned[:d['prefix_bytes']].endswith((staged['latest_checkpoint']+'\n').encode())
        assert Path(d['path']).read_bytes()==(old if mode=='stage' else planned)
    assert sha(Path(manifest['checkpoint_doc']).read_bytes())==manifest['checkpoint_doc_sha256']
    pending=staged[KEY];doc=read(pending['manuscript']);view=read(pending['source_view']);names=read(pending['names'])
    assert pending['new_credit']==pending['new_emulator_runs']==0 and not pending['new_ROM'] and not pending['full_goal_complete']
    assert (pending['total_uncredited_physical_speeches'],pending['source_first_meanings'],pending['individual_prose_decisions'],pending['remaining_individual_prose_decisions'])==(224,224,44,180)
    assert sha(Path(pending['manuscript']).read_bytes())==pending['manuscript_sha256']
    assert sha(Path(pending['source_view']).read_bytes())==pending['source_view_sha256']
    assert sha(Path(pending['names']).read_bytes())==pending['names_sha256']
    assert view['all23_source_sheets224_complete_native_pages_directly_viewed_before_current_English']
    assert len(view['viewed_sheets'])==23 and sum(s['source_page_count'] for s in view['viewed_sheets'])==224
    for sheet in view['viewed_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ns=view['sixteen_actor24_current_nameplanes_sheet_directly_viewed'];assert sha(Path(ns['path']).read_bytes())==ns['sha256']
    for p,digest in view['evidence'].items():assert sha(Path(p).read_bytes())==digest
    controls=read('work/analysis/Hodram_B61_B70_source_controls_v8878/source_controls.json')
    current=read('work/analysis/Hodram_B61_B70_current_v8885/current_effective.json')
    display=read('work/analysis/Hodram_B61_B70_source_display_v8881/224_complete_source_dispatches_alignments_pages_andmacro_binding.json')
    gloss=read('work/analysis/Hodram_B61_B70_clean_gloss_v8877/224_complete_clean_first_meanings_all_ten_exchanges_before_current_English.json')
    paths=read('work/analysis/Hodram_B61_B70_source_paths_v8883/all224_source_memberships_original_branch_cases.json')
    assert (controls['complete_source_commands'],controls['complete_speech_preambles'],controls['relative_sites'],controls['native_relative_cases'],controls['raw_unforced_query_cases'],controls['opaque_structural_decode_pairs'],controls['normal_seeded_end_cases'])==(392,224,60,300,15,83,250)
    assert len(display['records'])==display['complete_native_source_page_count']==224 and display['source_FE_count']==0
    assert sum(len(r['original_four_alignments']['cases']) for r in display['records'])==896
    assert display['source_macro_counts']=={'FI':15,'FA':3,'FO':0}
    assert sum(g['five_native_argument_compositions_checked'] for g in paths['groups'])==15830
    assert sum(g['conditional_utterances'] for g in paths['groups'])==48
    assert len(names['records'])==16 and all(r['decision']=='retention' and r['retention_reason'] and not r['review']['formatting'] for r in names['records'])
    assert len(current['records'])==224 and len(current['current_relative_cases'])==60 and len(current['current_query_cases'])==15
    assert sum(len(r['cases']) for r in current['current_relative_cases'])==300
    source_rom=NdsImage.open('work/clean.nds');candidate=staged['current_integrated_candidate']
    assert candidate['profile']=='all-routes-unified-v8865' and candidate['sha256']==previous['candidate_sha256']==controls['candidate_sha256']==current['current_ROM_sha256']
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']
    current_rom=NdsImage.open(candidate['path'])
    source_blocks=IlnkContainer.parse(source_rom.read_file('/data/SC1.DK4')).blocks
    current_blocks=IlnkContainer.parse(current_rom.read_file('/data/SC1.DK4')).blocks
    all_records={r['id']:r for r in current['records']};assert len(all_records)==224
    first_meanings={r['id']:r for g in gloss['groups'] for r in g['records']};assert set(first_meanings)==set(all_records)
    for group in current['groups']:
        number=group['block'];source,cur=source_blocks[number],current_blocks[number]
        assert source.hex()==group['clean_block_hex'] and cur.hex()==group['current_block_hex']
        assert len(group['all_source_commands'])==len(group['all_current_commands'])==len(group['all_command_reference_pairs'])
        for commands,raw in [(group['all_source_commands'],source),(group['all_current_commands'],cur)]:
            for c in commands:
                value=bytes.fromhex(c['whole_command_hex']);assert raw[c['offset']:c['offset']+len(value)]==value
            assert commands[-1]['whole_command_hex']=='00000000' and commands[-1]['native_extent']==4
        for r in group['records']:
            for reference,hexkey,raw in [('source_reference','source_hex',source),('current_reference','current_hex',cur)]:
                at=r[reference]['offset'];value=bytes.fromhex(r[hexkey]);assert raw[at:at+len(value)]==value and raw[at+len(value)]==0
                assert raw[at-5:at+1].hex()==r['source_complete_preamble_hex']
            assert r['current_English_body_now_exposed'] and not r['current_English_body_unread']
            first=first_meanings[r['id']];assert first['current_English_dialogue_still_unconsulted']
            for k in ['source_hex','source_reference','source_meaning_gloss','whole_exchange_fidelity_note']:assert r[k]==first[k]
    assert len(doc['records'])==44 and len(doc['remaining180_records_pending_individual_prose_decisions'])==180
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert doc['full_batch_blocks']==list(range(61,71)) and doc['full_batch_physical_speeches']==224 and doc['blocks']==[61,62]
    decisions=set();revised=retained=0
    for r in doc['records']:
        ident=r['id'];assert ident not in decisions;decisions.add(ident);old=all_records[ident]
        assert r['block'] in [61,62]
        for k in ['source_reference','source_hex','source_Japanese','current_reference','current_hex','source_meaning_gloss']:assert r[k]==old[k]
        assert r['source_meaning']==old['source_meaning_gloss'] and r['context'] and r['finding'] and r['localization_note'] and r['exact_structural_neighbor_pairs']
        assert r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        text=r['english'];assert text==text.strip() and not any(x in text for x in ['\n','\r','{LB','{ALIGN','{PAD','  ','%']);text.encode('cp932')
        prior=re.sub(r'\b(FI|FA|FO)\b',lambda m:'{MACRO:'+m[1]+'}',old['effective_predecessor_paragraph'])
        assert r['prior_macro_normalized_comparison']==prior
        assert r['decision']==('retention' if text==prior else 'revision')
        for macro in ['FI','FA','FO']:assert text.count('{MACRO:'+macro+'}')==bytes.fromhex(r['source_hex'])[1:].count(macro.encode())
        if r['decision']=='retention':assert r['retention_reason'];retained+=1
        else:assert r['retention_reason'] is None;revised+=1
    assert revised==doc['revised']==32 and retained==doc['retained']==12
    assert {r['id'] for r in doc['remaining180_records_pending_individual_prose_decisions']}==set(all_records)-decisions
    for r in doc['remaining180_records_pending_individual_prose_decisions']:
        assert all(r[k]==all_records[r['id']][k] for k in r)
    assert manifest['new_credit']==0 and not manifest['full_goal_complete']
    if mode=='stage':assert LEDGER.read_bytes()==(ROOT/'ledger_before.json').read_bytes()
    else:
        assert LEDGER.read_bytes()==(ROOT/'ledger_staged.json').read_bytes()
        assert Path('docs/editorial_Hodram_B61_B70_v8887.md').read_bytes()==Path(manifest['checkpoint_doc']).read_bytes()
        applied=read(ROOT/'applied.json');assert applied['ledger_sha256']==sha(LEDGER.read_bytes()) and applied['stage_manifest_sha256']==sha((ROOT/'stage_manifest.json').read_bytes())
    return dict(pass_audit=True,stage_manifest_sha256=sha((ROOT/'stage_manifest.json').read_bytes()),
        whole_prior_ledger_andscope_value_inverses_exact=True,all_prior_document_bytes_preserved=True,
        source_current224_raw_references392_commands_andpreambles_rebound_to_exact_ROMs=True,
        clean_meanings_source_native_name_views_before_current_comparison_bound=True,
        first44_individual_four_prose_gates_32revisions12retentions_verified=True,
        all224_uncredited_and180_individual_prose_decisions_still_pending=True,
        completed_counters_release_stack_builder_candidate_patch_manifest_baselines_unchanged=True,
        no_new_gameplay_formatting_storage_release_orfull_goal_approval=True,new_credit=0,full_goal_complete=False,
        auditor=str(Path(__file__)),auditor_sha256=sha(Path(__file__).read_bytes()))

if __name__=='__main__':
    mode=sys.argv[1];assert mode in ['stage','live'];result=audit(mode);result['pass']=result.pop('pass_audit')
    target=ROOT/('independent_staged_audit.json' if mode=='stage' else 'independent_live_audit.json')
    assert not target.exists();save(target,result)
    if mode=='live':
        output=Path('work/analysis/editorial_handoff_verification_v8889');assert not output.exists();output.mkdir(parents=True)
        ledger=read(LEDGER);candidate=ledger['current_integrated_candidate'];manifest=read(ROOT/'stage_manifest.json')
        save(output/'verified_handoff.json',dict(**result,goal_status='active',full_goal_active=True,
            ledger_sha256=sha(LEDGER.read_bytes()),candidate=candidate['path'],candidate_sha256=candidate['sha256'],profile=candidate['profile'],
            patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],manifest=candidate['manifest'],completed=7319,
            source_prose=7322,revised=4538,retained=2781,**COUNTERS,
            previous_verified_handoff=manifest['previous_verified_handoff'],previous_verified_handoff_sha256=manifest['previous_verified_handoff_sha256'],
            unfinished_scope=ledger[SCOPE],pending_source_batch=ledger[KEY],latest_manuscript=ledger[KEY]['manuscript'],latest_names=ledger[KEY]['names'],
            new_emulator_runs=0,new_actual_frames=0,new_registered_ROM=False,
            source_display_session84795_andcurrent_comparison_session81856_terminal_exit0=True,
            next_required=['remaining180 whole-exchange individual English decisions','automatic native English plans/pages/direct views',
                'complete stored relocation references andinverses','representative gameplay/focused risks','production atomic registered integration/exact clean patch/own startup','once-only224 completion credit after necessary gates']))
    print('Independent '+mode+' audit passes: all prior state recoverable;224 source/current references,44 prose decisions and180 pending; no credit orROM change.')
