"""Reuse credited HELP and Deck proofs on their unchanged cumulative resources."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.build_registered_rafael5186_v1 import RELEASE,REGISTRY,CLEAN
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER

OUT=Path('work/priority_tutorials_Rafael5186_v1.json')

def main():
    assert not OUT.exists()
    ledger,release=map(load,(LEDGER,RELEASE))
    assert digest(REGISTRY)==release['registry_sha256']
    current=NdsImage.open(release['candidate']);clean=NdsImage.open(CLEAN)
    keys={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    help_rows={};evidence={}
    deck=None
    for family in ledger['completed_editorial_families']:
        path=family.get('final_review')
        if not path or not ('help' in family['id'].lower() or family['id']=='shared_Deck_four_panel_complete_contextual_release_20261104'):continue
        doc=load(path);evidence[path]=digest(path)
        for row in doc['records']:
            if row.get('file_path')=='/COMMON/HELP.DK4':
                assert (row['file_path'],row['id']) in keys and all(row['review'].values())
                help_rows[row['topic_id']]=dict(id=row['id'],final_review=path,review=row['review'])
        if family['id']=='shared_Deck_four_panel_complete_contextual_release_20261104':deck=(family,doc)
    assert set(help_rows)==set(range(202))
    help_parent=load('work/analysis/Help97_Rafael330_release_verified_20261105/registered_release_verification.json')
    old=NdsImage.open(help_parent['candidate'])
    assert digest(help_parent['candidate'])==help_parent['candidate_sha256']
    assert current.read_file('/COMMON/HELP.DK4')==old.read_file('/COMMON/HELP.DK4')
    assert len(IlnkContainer.parse(clean.read_file('/COMMON/HELP.DK4')).blocks)==202
    assert deck is not None and len(deck[1]['records'])==4
    binding_path=deck[0]['integrated_record_bindings'];bindings=load(binding_path)
    # The complete registered parent is retained; compare only the owned panel
    # text/pointer spans, since later independent name fields changed ARM9.
    data=current.read_file('/__arm9__.bin')
    panel_rows=[];bound={r['id']:r for r in bindings['records']}
    for row in deck[1]['records']:
        assert (row['file_path'],row['id']) in keys and all(row['review'].values())
        ref=bound[row['id']]['registered_reference'];at=ref['offset']
        payload=bytes.fromhex(ref['padded_hex'])
        assert len(payload)==ref['capacity'] and data[at:at+len(payload)]==payload
        pointer=row['source_reference']['pointer_field']
        assert data[pointer:pointer+4]==row['current_reference']['pointer'].to_bytes(4,'little')
        panel_rows.append(dict(id=row['id'],review=row['review'],registered_reference=ref,
            current_text_allocation_andpointer_exact=True))
    prior=load('work/analysis/Shared_tutorial_name_data_release_verified_20261104/registered_release_verification.json')
    parent=NdsImage.open(prior['candidate']);old_arm=parent.read_file('/__arm9__.bin')
    assert digest(prior['candidate'])==prior['candidate_sha256']
    assert all(data[r['registered_reference']['offset']:r['registered_reference']['offset']+r['registered_reference']['capacity']]
        ==old_arm[r['registered_reference']['offset']:r['registered_reference']['offset']+r['registered_reference']['capacity']] for r in panel_rows)
    save(OUT,dict(release=str(RELEASE),release_sha256=digest(RELEASE),candidate_sha256=release['candidate_sha256'],
        HELP_topics=202,all_HELP_topics_have_credited_five_gate_reviews=True,
        HELP_archive_exact_to_final_registered_HELP_parent=True,HELP_records=list(help_rows.values()),
        Deck_panels=panel_rows,Deck_binding=str(binding_path),Deck_binding_sha256=digest(binding_path),
        Deck_current_text_allocations_andpointers_exact=True,
        Rafael_native_source_census='work/Rafael_B0_B34_clean_20261106/registered_coverage_v1.json',
        shared_non_HELP_resources_remain_in_scope=True,not_a_global_tutorial_census=True,
        no_new_editorial_credit_or_gameplay=True,new_credit=0,evidence=evidence,producer_sha256=digest(__file__)))
    print('202 HELP topics and four Deck panels reconciled with exact current resources; no duplicate review credit.')

if __name__=='__main__':main()
