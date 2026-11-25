"""Restore original native catalogue indices from the exact current binder, without deriving them from text IDs."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    before=ROOT/'formatting_v3/formatting_input.json'
    after=ROOT/'formatting_v3/formatting_input_complete_indices_v1.json'
    receipt=ROOT/'formatting_v3/native_index_projection_v1.json'
    current_path=ROOT/'current_v1/current_effective.json'
    assert not after.exists() and not receipt.exists()
    doc=deepcopy(load(before));current=load(current_path)
    assert doc['runtime']==current['runtime']
    bound={r['id']:r for g in current['groups'] for r in g['records']};assert len(bound)==299
    bindings=[]
    for row in doc['records']:
        if row['kind']=='typed-choice-label':
            assert row['id'] not in bound;continue
        native=bound[row['id']]
        for key in ['source_hex','source_reference','current_reference','source_selector','source_complete_preamble_hex']:
            assert native[key]==row[key],(row['id'],key)
        assert 'source_record_index' not in row
        row['source_record_index']=native['source_record_index']
        bindings.append(dict(id=row['id'],source_record_index=row['source_record_index'],
            source_reference=row['source_reference'],source_complete_preamble_hex=row['source_complete_preamble_hex']))
    assert len(bindings)==299
    doc.update(complete_original_catalogue_index_projection=dict(source=str(current_path),sha256=digest(current_path),
        physical_speeches=299,choice_labels_excluded_from_catalogue_indices=4),
        pre_projection_formatting_input=str(before),pre_projection_formatting_input_sha256=digest(before))
    save(after,doc)
    save(receipt,dict(bindings=bindings,current_native_binder=str(current_path),current_native_binder_sha256=digest(current_path),
        before=str(before),before_sha256=digest(before),after=str(after),after_sha256=digest(after),
        prose_controls_references_macros_andall_five_gate_values_unchanged=True,new_credit=0))
    print('Projected299 original native catalogue indices;four typed labels remain separate. No prose or gate changes.')

if __name__=='__main__':main()
