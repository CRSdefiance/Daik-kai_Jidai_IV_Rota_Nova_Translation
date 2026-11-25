"""Add derived page/name counts to immutable run fixtures;preserve all original run inputs andbytes."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael330_actual_fixtures_20261105')
OUT=Path('work/analysis/Rafael330_actual_analysis_inputs_20261105')
NATIVE=Path('work/analysis/Rafael330_stored_consumer_inputs_20261105/native_consumer_planes.json')

if __name__=='__main__':
    assert not OUT.exists();native=load(NATIVE);byid={r['id']:r for r in native['records']};OUT.mkdir();rows=[]
    for name in ['B81_complete_bullfight','names_pages_FE_transitions','B84_two_andthree_choice']:
        source=ROOT/(name+'_fixture.json');original=load(source);doc=deepcopy(original);pages=0
        for row in doc['selected_records']:
            display=byid[row['id']]['complete_native_English_display'];pages+=1 if row['selector']==254 else len(display['pages'])
        doc.update(expected_pages=pages,ordinary_actor_IDs=sorted({r['selector'] for r in doc['selected_records'] if r['selector']!=254}),
            original_run_fixture=str(source),original_run_fixture_sha256=sha(source.read_bytes()),
            analysis_metadata_only_all_run_ROM_inputs_commands_andbody_bindings_exact=True)
        assert all(doc[k]==v for k,v in original.items());path=OUT/(name+'_fixture.json');save(path,doc)
        rows.append(dict(source_fixture=str(source),source_sha256=sha(source.read_bytes()),analysis_fixture=str(path),analysis_sha256=sha(path.read_bytes()),
            utterances=len(doc['selected_records']),pages=pages,actors=len(doc['ordinary_actor_IDs'])))
    save(OUT/'metadata_equivalence.json',dict(fixtures=rows,native=str(NATIVE),native_sha256=sha(NATIVE.read_bytes()),
        all_actual_run_fixtures_preserved_exactly=True,new_credit=0))
    print([(r['utterances'],r['pages'],r['actors']) for r in rows])
