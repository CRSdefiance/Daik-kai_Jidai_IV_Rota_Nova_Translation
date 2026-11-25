"""Reuse exact qualified name planes for current and proposed actual-header comparisons."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
OUT=ROOT/'actual_name_inputs_v1'

def main():
    assert not OUT.exists()
    bound_path=ROOT/'scoped_names_current_v1.json';retained_path=ROOT/'retained_name_planes_v1/native_name_planes.json'
    fields_path=ROOT/'name_field_checks_v1/native_name_fields_verification.json'
    bound,retained,fields=map(load,(bound_path,retained_path,fields_path));OUT.mkdir()
    versions={v['version']:v['names']['rows'] for v in fields['versions']}
    for version in ['current','proposed']:
        rows=[]
        for r in bound['records']:
            value=next(c['text'] for c in r['current_consumers'] if c['consumer']=='progressive-nameplate')
            if version=='proposed' and r['actor_ID'] in [55,56,57]:
                value=next(c['text'] for c in versions[version] if c['actor_ID']==r['actor_ID'] and c['consumer']=='progressive-nameplate')
            rows.append(dict(actor_ID=r['actor_ID'],english=value,source_native_name_binding=str(bound_path),original_getters_not_reexecuted=True))
        decisions=OUT/(version+'_decisions.json');save(decisions,dict(records=rows,actual_headers_not_yet_approved=True,new_credit=0))
        planes=deepcopy(retained['planes'])
        for p in fields['planes']:
            if p['version']==version and p['style']==11:
                assert digest(p['plane'])==p['plane_sha256']
                planes.append(dict(text=p['text'],native_plane=p['plane'],native_plane_sha256=p['plane_sha256'],
                    source_native_proof=str(fields_path),source_native_proof_sha256=digest(fields_path)))
        bytext={p['text']:p for p in planes}
        assert set(r['english'] for r in rows)==set(bytext) and len(rows)==42 and len(bytext)==41
        for p in bytext.values():assert digest(p['native_plane'])==p['native_plane_sha256']
        save(OUT/(version+'_planes.json'),dict(name_decisions=str(decisions),name_decisions_sha256=digest(decisions),planes=list(bytext.values()),
            runtime=bound['runtime'],name_data_version=version,actual_gameplay=False,new_credit=0,
            exact_name_plane_reuse_no_new_native_execution=True,evidence={str(p):digest(p) for p in [bound_path,retained_path,fields_path,decisions,Path(__file__)]}))
    print('Prepared current/proposed42-actor name expectations from41 exact native strings each; no CPU rerender or gameplay credit.')

if __name__=='__main__':main()
