"""Independent additive-state, complete prose/reference/native-artifact audit."""
import re,sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_checkpoint_v8897')
KEY='Hodram_SC1B61_B70_224_prose229_native_English_pages_pending_storage_actual_release_v8897'
SCOPE='unfinished_editorial_scope_v8897'
LEDGER=Path('translations/editorial_review_current_v1.json')

def audit(mode):
    m=read(ROOT/'stage_manifest.json');old=read(ROOT/'ledger_before.json');new=read(ROOT/'ledger_staged.json')
    assert sha((ROOT/'ledger_before.json').read_bytes())==m['ledger_before_sha256'] and sha((ROOT/'ledger_staged.json').read_bytes())==m['ledger_staged_sha256']
    previous=read(m['previous_verified_handoff']);assert previous['pass'] and previous['ledger_sha256']==m['ledger_before_sha256']
    assert sha(Path(m['previous_verified_handoff']).read_bytes())==m['previous_verified_handoff_sha256']
    for p,h in {**m['evidence'],**m['protected_files']}.items():assert sha(Path(p).read_bytes())==h,p
    assert old['goal_status']==new['goal_status']=='active' and not new['full_goal_complete']
    expected={'records_editorially_completed':7319,'records_with_source_and_prose_pass':7322,'records_with_source_prose_drafts':7322,
        'records_revised_and_integrated':4538,'retained_wordings_editorially_completed':2781}
    for k,v in expected.items():assert old[k]==new[k]==v
    assert old['completed_editorial_families']==new['completed_editorial_families'] and old['current_integrated_candidate']==new['current_integrated_candidate']
    inverse=deepcopy(new);pending=inverse.pop(KEY);scope_ref=inverse.pop(SCOPE);inverse['latest_checkpoint']=old['latest_checkpoint']
    last=inverse['research_checkpoints'].pop();assert last['id']=='V8897-Hodram-B61-B70-224-prose-229-native-English-pages' and last['new_editorially_completed']==0
    assert inverse==old
    scope=read(scope_ref['path']);assert sha(Path(scope_ref['path']).read_bytes())==scope_ref['sha256'] and scope.pop(KEY)==pending
    assert scope==read(ROOT/'scope_before.json')==read(m['scope_before_path'])
    assert sha((ROOT/'scope_before.json').read_bytes())==m['scope_before_sha256']
    for d in m['documents']:
        before,after=Path(d['before']).read_bytes(),Path(d['staged']).read_bytes()
        assert sha(before)==d['before_sha256'] and sha(after)==d['staged_sha256'] and after[d['prefix_bytes']:]==before
        assert after[:d['prefix_bytes']].endswith((new['latest_checkpoint']+'\n').encode())
        assert Path(d['path']).read_bytes()==(before if mode=='stage' else after)
    assert sha(Path(m['checkpoint_doc']).read_bytes())==m['checkpoint_doc_sha256']
    doc=read(pending['manuscript']);view=read(pending['native_view']);partial=read('translations/hodram_B61_B70_editorial_manuscript_partial_v1.json')
    assert sha(Path(pending['manuscript']).read_bytes())==pending['manuscript_sha256'] and sha(Path(pending['native_view']).read_bytes())==pending['native_view_sha256']
    assert pending['new_credit']==pending['new_emulator_runs']==0 and not pending['new_ROM'] and pending['remaining_individual_prose_decisions']==0
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and len(doc['records'])==224
    assert doc['revised']==132 and doc['retained']==92 and doc['first44_all_record_values_reused_exactly']
    assert [r for r in doc['records'] if r['block'] in [61,62]]==partial['records']
    current=read(doc['current_packet']);assert sha(Path(doc['current_packet']).read_bytes())==doc['current_packet_sha256']
    rows={r['id']:r for r in current['records']};assert len(rows)==224 and current['all224_source_units_uncredited_in_current_ledger']
    candidate=new['current_integrated_candidate'];assert candidate['profile']=='all-routes-unified-v8865' and candidate['sha256']==current['current_ROM_sha256']==previous['candidate_sha256']
    banks={label:IlnkContainer.parse(NdsImage.open(path).read_file('/data/SC1.DK4')).blocks for label,path in [('clean','work/clean.nds'),('current',candidate['path'])]}
    revisions=retentions=0;macro_counts=dict(FI=0,FA=0,FO=0);ids=set()
    for r in doc['records']:
        assert r['id'] not in ids;ids.add(r['id']);c=rows[r['id']]
        for k in ['source_hex','source_reference','source_Japanese','current_hex','current_reference','source_meaning_gloss']:assert r[k]==c[k]
        for label,key,hexkey in [('clean','source_reference','source_hex'),('current','current_reference','current_hex')]:
            raw=banks[label][r['block']];at=r[key]['offset'];value=bytes.fromhex(r[hexkey]);assert raw[at:at+len(value)]==value and raw[at+len(value)]==0
            assert raw[at-5:at+1].hex()==r['source_complete_preamble_hex']
        assert r['source_meaning']==r['source_meaning_gloss'] and r['context'] and r['finding'] and r['localization_note'] and r['exact_structural_neighbor_pairs']
        assert r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        text=r['english'];assert text==text.strip() and not any(v in text for v in ['\n','\r','{LB','{ALIGN','{PAD','  ','%']);text.encode('cp932')
        prior=re.sub(r'\b(FI|FA|FO)\b',lambda v:'{MACRO:'+v[1]+'}',c['effective_predecessor_paragraph'])
        assert r['decision']==('retention' if text==prior else 'revision')
        if r['decision']=='retention':assert r['retention_reason'];retentions+=1
        else:assert r['retention_reason'] is None;revisions+=1
        for token in macro_counts:
            n=bytes.fromhex(r['source_hex'])[1:].count(token.encode());assert text.count('{MACRO:'+token+'}')==n;macro_counts[token]+=n
    assert (revisions,retentions)==(132,92) and macro_counts=={'FI':15,'FA':3,'FO':0}
    assert view['all23_sheets229_English_native_pages_directly_viewed'] and view['complete_native_pages']==229 and len(view['review_sheets'])==23
    assert len(view['two_page_record_IDs'])==5 and view['actual_findings_separate_from_passing_validation']==dict(editorial_revisions=132,justified_retentions=92,
        first_plan_readability_findings=4,plans_refined=16,new_source_native_control_or_glyph_failures=0,new_logical_macro_failures=0,new_compiled_native_page_failures=0)
    for p,h in view['evidence'].items():assert sha(Path(p).read_bytes())==h
    for s in view['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    pages=read('work/analysis/Hodram_B61_B70_pages_v8894/compiled_native_pages.json');plans=read('work/analysis/Hodram_B61_B70_layout_v8893/automatic_plans.json')
    assert len(pages['records'])==len(plans['records'])==224 and not plans['failures']
    assert pages['fresh_compiled_alignment_cases']==pages['total_bound_compiled_alignment_cases']==896 and pages['complete_native_English_pages']==229
    total=0
    for r,p in zip(pages['records'],plans['records'],strict=True):
        assert r['id']==p['id'] and r['logical_English']==' '.join(p['lines']) and r['compiled_hex']==p['encoded_hex']
        assert p['original_consumer_usable_text_width_px']==216 and not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        assert len(r['complete_native_English_display']['pages'])==p['expected_native_pages']
        for page in r['complete_native_English_display']['pages']:
            assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
            assert sha(Path(page['preview']).read_bytes())==page['preview_sha256']
            assert page['complete_first_internal_final_codes_bounds_consumption_andindependent_ink_exact'];total+=1
    assert total==229 and sum(len(r['base_QA']['issues']) for r in plans['records'])==68
    if mode=='stage':assert LEDGER.read_bytes()==(ROOT/'ledger_before.json').read_bytes()
    else:
        assert LEDGER.read_bytes()==(ROOT/'ledger_staged.json').read_bytes()
        assert Path('docs/editorial_Hodram_B61_B70_v8897.md').read_bytes()==Path(m['checkpoint_doc']).read_bytes()
        assert read(ROOT/'applied.json')['ledger_sha256']==sha(LEDGER.read_bytes())
    return dict(stage_manifest_sha256=sha((ROOT/'stage_manifest.json').read_bytes()),whole_prior_ledger_scope_anddocument_inverses_exact=True,
        all224_source_current_prose_four_gates_and132_92_decisions_bound=True,first44_record_values_exact=True,
        all229_native_pages23_direct_sheets_896_alignments_and68_original_QAinfos_bound=True,
        four_readability_findings_distinct_from_no_new_runtime_failures=True,
        all224_formatting_gates_false_stored_actual_production_atomic_andregistered_integration_pending=True,
        no_count_family_release_stack_builder_ROM_patch_manifest_orbaseline_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        auditor=str(Path(__file__)),auditor_sha256=sha(Path(__file__).read_bytes()),**{'pass':True})

if __name__=='__main__':
    mode=sys.argv[1];assert mode in ['stage','live'];result=audit(mode)
    target=ROOT/('independent_staged_audit.json' if mode=='stage' else 'independent_live_audit.json');assert not target.exists();save(target,result)
    if mode=='live':
        out=Path('work/analysis/editorial_handoff_verification_v8899');assert not out.exists();out.mkdir(parents=True)
        ledger=read(LEDGER);c=ledger['current_integrated_candidate'];m=read(ROOT/'stage_manifest.json')
        save(out/'verified_handoff.json',dict(**result,ledger_sha256=sha(LEDGER.read_bytes()),goal_status='active',full_goal_active=True,
            candidate=c['path'],candidate_sha256=c['sha256'],profile=c['profile'],patch=c['patch'],patch_sha256=c['patch_sha256'],manifest=c['manifest'],
            completed=7319,source_prose=7322,revised=4538,retained=2781,
            records_editorially_completed=7319,records_with_source_and_prose_pass=7322,records_with_source_prose_drafts=7322,
            records_revised_and_integrated=4538,retained_wordings_editorially_completed=2781,
            previous_verified_handoff=m['previous_verified_handoff'],previous_verified_handoff_sha256=m['previous_verified_handoff_sha256'],
            unfinished_scope=ledger[SCOPE],pending_source_batch=ledger[KEY],latest_manuscript=ledger[KEY]['manuscript'],latest_native_view=ledger[KEY]['native_view'],
            logical_session74493_native_session54986_terminal_exit0=True,new_registered_ROM=False,new_actual_frames=0,
            next_required=['complete stored relocation maps controls references andinverses','stored native planes/loaders','representative gameplay andfocused risks',
                'production atomic registered integration/exact clean-input patch/own startup','once-only224 completion credit afternecessary gates']))
    print('Independent '+mode+' audit passes:224 prose/229 native pages;full prior state retained;stored-actual-release pending;zero credit.')
