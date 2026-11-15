"""Bind unchanged stored bytes/runtime exactly;refresh one body and all relocated branches."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael330_incremental_stored_v2_20261105')
NEW=Path('work/analysis/Rafael330_stored_consumer_inputs_v2_20261105')
OLD=Path('work/analysis/Rafael330_stored_consumer_inputs_20261105')
ID='DK4_MES_B81_R0220'

if __name__=='__main__':
    assert not ROOT.exists()
    oldpath=OLD/'native_consumer_reconstruction.json';newpath=NEW/'native_consumer_reconstruction.json'
    old,new=map(load,[oldpath,newpath])
    storedpath=Path('work/analysis/Rafael330_stored_native_20261105/stored_native_verification.json')
    stored=load(storedpath);assert stored['reconstruction_sha256']==sha(oldpath.read_bytes())
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    oldnative,newnative=[load(Path(d['native'])) for d in [old,new]]
    assert oldnative['runtime']==newnative['runtime']==stored['runtime']
    assert oldnative['font_sha256']==newnative['font_sha256']
    assert old['parent_sha256']==new['parent_sha256']
    a,b=[NdsImage.open(d['research_ROM']) for d in [old,new]]
    assert all(a.read_file(p)==v for p,v in b.iter_components())
    assert [p for _,p,v in a.iter_files() if b.read_file(p)!=v]==['/data/SC0.DK4']
    banks=[IlnkContainer.parse(x.read_file('/data/SC0.DK4')).blocks for x in [a,b]]
    assert [i for i,(u,v) in enumerate(zip(*banks,strict=True)) if u!=v]==[81]
    priorrows={r['id']:r for r in stored['records']};oldn={r['id']:r for r in oldnative['records']}
    currentn={r['id']:r for r in newnative['records']};bindings=[];changed=[]
    for g in new['groups']:
        block=banks[1][g['block']];assert sha(block)==g['target_sha256']
        for t in g['text_records']:
            raw=bytes.fromhex(t['stored_hex']);at=t['new_offset']
            assert block[at:at+len(raw)+1]==raw+b'\0'
            assert block[at-5:at+1].hex()==t['complete_source_preamble_hex']
            assert t['new_record_index']==block[:at].count(b'\0')
            if t['stored_hex']!=priorrows[t['id']]['stored_hex']:changed.append(t['id']);continue
            assert currentn[t['id']]==oldn[t['id']]
            assert t['compiled_hex']==currentn[t['id']]['compiled_hex']
            assert t['parity_space_added']==priorrows[t['id']]['parity_space_added']
            for page in priorrows[t['id']]['directly_viewed_planes']:
                assert sha(Path(page['path']).read_bytes())==page['sha256']
            bindings.append(dict(id=t['id'],block=g['block'],new_offset=at,new_record_index=t['new_record_index'],
                stored_hex=t['stored_hex'],exact_prior_stored_record=priorrows[t['id']]))
    assert changed==[ID] and len(bindings)==326
    ROOT.mkdir()
    native=deepcopy(newnative);native['records']=[currentn[ID]];native['pages']=1
    save(ROOT/'one_fresh_native.json',native)
    subset=deepcopy(new);subset.update(native=str(ROOT/'one_fresh_native.json'),
        native_sha256=sha((ROOT/'one_fresh_native.json').read_bytes()),speech_count=1)
    for g in subset['groups']:g['text_records']=[r for r in g['text_records'] if r['id']==ID]
    save(ROOT/'one_fresh_reconstruction.json',subset)
    save(ROOT/'exact326_stored_reuse.json',dict(changed_ID=ID,records=bindings,
        exact_reused_records=326,exact_reused_pages=335,complete_current_source_objects=330,
        complete_current_native_speech_commands=327,complete_current_body_pages=336,
        only_B81_changed=True,all_other_files_components_fonts_runtime_andnative_proofs_exact=True,
        all327_current_stored_bytes_full_preambles_offsets_indices_and327_source_owners_bound=True,
        one_fresh_native_body_andall28_relative_sites_pending=True,actual_gameplay=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [oldpath,newpath,storedpath,Path(old['native']),Path(new['native']),Path(__file__)]}))
    print('Exactly326 stored body proofs/335 pages reused;one fresh body plusall28 native branch sites queued.')
