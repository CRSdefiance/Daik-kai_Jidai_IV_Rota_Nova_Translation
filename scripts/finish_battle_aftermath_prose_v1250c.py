"""Finish ledger update after the immutable75-line manuscript saved.

V1250b stopped because38 older active drafts were still present. Preserve and
merge those drafts rather than replace them;never rewrite the saved manuscript.
"""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_aftermath_layout_v1250 import IDS,paragraph
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_aftermath_prose_v1250c')
MANUSCRIPT=Path('translations/battle_aftermath_editorial_manuscript_v1.json')


def main():
    assert not ROOT.exists()
    proof_path=Path('work/analysis/battle_aftermath_prose_v1250b/source_prose_review.json')
    doc,proof=read(MANUSCRIPT),read(proof_path)
    assert proof['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert tuple(r['message_id'] for r in doc['records'])==IDS
    assert doc['formatting_review_pending'] and doc['no_compiled_release_payload_or_layout_approval_yet']
    assert sum(r['editorial_decision']=='revise' for r in doc['records'])==55
    for r in doc['records']:
        assert all(r['review'][k] for k in ('source','context','localization','naturalness'))
        assert not r['review']['formatting'] and paragraph(r).hex()==r['unwrapped_paragraph_hex']
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1260 and ledger['records_with_source_and_prose_pass']==1298
    old=set(ledger['reviewed_but_incomplete_COMMON_IDs']);assert len(old)==38 and not old.intersection(IDS)
    done={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert len(done)==1259 and not done.intersection(IDS)
    drafts=ledger['active_source_prose_drafts'];older_manuscripts=list(drafts['manuscripts'])
    assert set(drafts['native_message_IDs'])==old and len(older_manuscripts)==3
    ledger['records_with_source_and_prose_pass']=1373
    ledger['source_prose_reviewed_counts_by_file']={'/COMMON/MESFILE.DK4':1372,'/data/SC2.DK4':1}
    ledger['reviewed_but_incomplete_COMMON_IDs']=sorted(old|set(IDS))
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==113
    drafts['native_message_IDs']=sorted(set(drafts['native_message_IDs'])|set(IDS))
    assert str(MANUSCRIPT) not in drafts['manuscripts']
    drafts['manuscripts'].append(str(MANUSCRIPT))
    drafts['manuscript_record_subsets_pending'][str(MANUSCRIPT)]=list(IDS)
    drafts.update(status='75-new-aftermath-drafts-and38-preserved-older-reviewed-entries-open',
        note='55 revised and20 retained aftermath drafts need native layout,integration and original gameplay. Older750-752,successful Lookout shot and remaining sighting contexts remain;broader shared/routes/raw inventory is also unfinished.')
    ledger['battle_aftermath_prose_v1250']={'native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),
        'source_context':doc['native_context_proof'],'source_binding':doc['complete_source_binding'],
        'source_prose_proof':str(proof_path),'reviewed_entries':75,'revised_drafts':55,'retained_drafts':20,
        'native_format_and_actual_pending':True,'completed_entries':0}
    ledger['latest_checkpoint']='V1250c records75 source/prose reviews:55 revisions20 retentions. Source/prose1373,completed1260 unchanged;113 reviewed COMMON entries incomplete. Both114 town branches,2288 voice choices,86 consumers and exact town-name/2192/city/ship bindings pass. Native formatting,full fonts,registered integration and actual gameplay remain open;older38 drafts preserved.'
    ROOT.mkdir(parents=True)
    save(ROOT/'ledger_recovery.json',{'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'source_prose_proof':str(proof_path),'source_prose_proof_sha256':sha(proof_path.read_bytes()),
        'source_counts_before_after':[1298,1373],'completed_count_unchanged':1260,
        'preserved_older_native_IDs':sorted(old),'preserved_older_manuscripts':older_manuscripts,
        'new_source_prose_IDs':list(IDS),'no_duplicate_or_completed_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    save(ledger_path,ledger)
    print('75 new prose drafts recorded;older38 drafts preserved.1373 source/prose,1260 completed;native layout/integration/gameplay remain open.',flush=True)


if __name__=='__main__':main()
