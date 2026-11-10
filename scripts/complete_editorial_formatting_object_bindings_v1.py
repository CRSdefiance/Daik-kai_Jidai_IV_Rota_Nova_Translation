"""Add already proven style/menu storage metadata without changing prose or gates."""
import argparse
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('manuscript','objects','out'):p.add_argument('--'+k,type=Path,required=True)
    a=p.parse_args();assert not a.out.exists()
    doc,objects=map(load,(a.manuscript,a.objects));result=deepcopy(doc)
    bound={r['id']:r for r in objects['style_records']+objects['choice_records']}
    assert doc['runtime']==objects['runtime']
    touched=[]
    for row in result['records']:
        if row['id'] not in bound:continue
        original=bound[row['id']]
        assert all(row[k]==original[k] for k in ('source_reference','source_hex','current_reference','current_hex'))
        added=[]
        for key,value in original.items():
            if key.startswith(('current_style_','current_choice_')):
                if key in row:assert row[key]==value
                else:row[key]=deepcopy(value);added.append(key)
        touched.append(dict(id=row['id'],added_storage_metadata=added))
    assert len(touched)==len(bound)
    prior={r['id']:r for r in doc['records']}
    assert all(all(row[k]==v for k,v in prior[row['id']].items()) for row in result['records'])
    result.update(complete_original_style_menu_storage_metadata_rebound=True,
        previous_formatting_input=str(a.manuscript),previous_formatting_input_sha256=digest(a.manuscript),
        exact_object_metadata_source=str(a.objects),exact_object_metadata_source_sha256=digest(a.objects),
        object_metadata_bindings=touched,object_binding_producer_sha256=digest(__file__))
    save(a.out,result)
    print(f'Bound{len(touched)} original style/caption storage objects; all English, references and gates unchanged.')


if __name__=='__main__':main()
