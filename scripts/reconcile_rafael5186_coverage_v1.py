"""Extend the sealed SC0 census with only the newly integrated residual bindings."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.build_registered_rafael5186_v1 import RELEASE,CLEAN,REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import ROOT
from scripts.reconcile_rafael_source_coverage_v1 import source_location

OUT=ROOT/'registered_coverage_v1.json'
PRIOR=Path('work/analysis/Rafael_source_coverage_20261106_v2/coverage.json')
FINAL=Path('translations/rafael_B0_B34_integrated_final_review_v1.json')
LEDGER=Path('translations/editorial_review_current_v1.json')

def main():
    assert not OUT.exists()
    prior,doc,release,ledger=map(load,(PRIOR,FINAL,RELEASE,LEDGER))
    assert digest(REGISTRY)==release['registry_sha256']
    assert digest(CLEAN)==prior['source_ROM_sha256']
    assert not prior['inventory_failures'] and not prior['legacy_source_bindings_not_exact']
    assert len(prior['records'])==6887 and len(prior['missing'])==283
    assert doc['target_ROM_sha256']==release['candidate_sha256']
    assert doc['all283_individual_five_gates_pass'] and len(doc['records'])==283
    keys={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    blocks=IlnkContainer.parse(NdsImage.open(CLEAN).read_file('/data/SC0.DK4')).blocks
    family=ledger['Rafael_SC0_B0_B34_clean_20261106']['completed_in_combined_family']
    fresh={source_location(r):r for r in doc['records']}
    assert len(fresh)==283
    records=deepcopy(prior['records']); added=[]
    for row in records:
        ref=row['source_reference']; location=(row['block'],ref['offset'],row['source_hex'])
        raw=bytes.fromhex(row['source_hex'])
        assert blocks[row['block']][ref['offset']:ref['offset']+len(raw)]==raw
        if not row['covered']:
            new=fresh[location]
            assert new['file_path']==row['file_path'] and new['id']==row['id'] and all(new['review'].values())
            row['exact_credited_source_bindings']=[dict(id=new['id'],family=family,block=row['block'],offset=ref['offset'],source_hex=row['source_hex'])]
            row['covered']=True;added.append(new['id'])
        assert all((row['file_path'],r['id']) in keys for r in row['exact_credited_source_bindings'])
        assert row['covered'] and row['exact_credited_source_bindings']
    assert len(added)==283 and len(set(added))==283
    save(OUT,dict(prior_census=str(PRIOR),prior_census_sha256=digest(PRIOR),
        registered_release=str(RELEASE),registered_release_sha256=digest(RELEASE),
        final_review=str(FINAL),final_review_sha256=digest(FINAL),ledger_sha256=digest(LEDGER),
        source_ROM_sha256=prior['source_ROM_sha256'],object_counts=prior['object_counts'],records=records,
        source_objects=6887,previous_exact_bindings_reused=6604,new_exact_bindings=283,missing=[],
        all_clean_source_positions_rechecked=True,all_credited_keys_present_in_current_ledger=True,
        native_SC0_dialogue_style_caption_inventory_complete=True,
        not_a_full_player_facing_resource_or_reachability_census=True,
        no_new_gameplay_or_editorial_credit=True,full_goal_complete=False,new_credit=0,
        producer_sha256=digest(__file__)))
    print('SC0 source census reconciled: all 6,887 native speech/style/caption objects credited; no residual objects.')

if __name__=='__main__':main()
