"""Original18-byte editor contract and legal-sized scheme name stress cases."""

from itertools import product
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_map_player_faction_name as editor
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_tavern_continuation_layout_v768 import format_case
from scripts.verify_scheme_confirmation_v775 import ROOT,MANUSCRIPT
from scripts.verify_village_wrap_v608 import read,save

BOUNDARIES=(b'ABCDEFGHIJKLMNOPQR',b'ABCDEFGHI JKLMNOPQ',
            b'A BCDEFGHIJKLMNOPQ',b'ABCDEFGHIJKLMNOP Q')


def main():
    rom_path=Path('out/all_routes_combined_v773_candidate.nds')
    arm=NdsImage.open(rom_path).read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert all(arm[a:b]==clean[a:b] for a,b in editor.LOCKS)
    names=[b'A'*n for n in range(1,19)]+['ア'.encode('cp932')*n for n in range(1,10)]
    producer=[]
    for name in names:
        field=editor.native_copy(arm,name)
        producer.append({'name_hex':name.hex(),'editor':editor.edit_dispatch(arm,name),
            'save':editor.serialize(arm,field),'load':editor.serialize(arm,field,restore=True)})
    save(ROOT/'company_name_bound.json',{'source_ROM_sha256':sha(rom_path.read_bytes()),
        'source_current_exact_spans':editor.LOCKS,'cases':producer,'capacity':18,'serialized_bytes':19,
        'shared_offset':0x1A39,'special_owner_offset':0x19E4,'field_offset':0x55,
        'original_editor_limit_and_setter_and_serialization_verified':True,
        'legacy_producer_sha256':sha(Path(editor.__file__).read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),
        'scope':'Original native editor dispatch with keyboard UI stub,complete setter,NUL and save/load. Not an actual keyboard UI session.'})
    assert all(len(s)==18 for s in BOUNDARIES)
    doc=read(MANUSCRIPT)
    rows={r['message_id']:r for r in doc['records']}
    old_path=ROOT/'native_layout_matrix.json'
    old=read(old_path)
    real=[r for r in old['cases'] if not r['synthetic_23_byte_faction_boundary']]
    stress=[r for r in old['cases'] if r['synthetic_23_byte_faction_boundary']]
    assert len(real)==39730 and len(stress)==2152
    cases=[]
    for i,case in enumerate(stress):
        args=tuple(bytes.fromhex(s) for s in case['source_values_hex'])
        for boundary in BOUNDARIES:
            if len(cases)%64==0:u=machine(arm)
            result=format_case(u,rows[case['id']],tuple(boundary if len(s)==23 else s for s in args))
            result['legal18_byte_boundary_research']=True
            cases.append(result)
    # Include differently split names on both sides of a faction conflict.
    for n in range(948,956):
        for a,b in product(BOUNDARIES,BOUNDARIES):
            if a==b:continue
            if len(cases)%64==0:u=machine(arm)
            result=format_case(u,rows[n],(a,b))
            result['legal18_byte_boundary_research']=True
            cases.append(result)
    findings=[r for r in cases if r['findings']]
    save(ROOT/'legal_name_boundary_layouts.json',{'cases':cases,'count':len(cases),'findings':findings,
        'basis':'Proven18-byte editor;four explicit maximal names with different word boundaries,including mixed conflict pairs. Not all possible player-authored strings.',
        'real_catalog_layouts_reference':str(old_path),'real_catalog_matrix_sha256':sha(old_path.read_bytes()),
        'all39730_real_catalog_cases_clean':not any(r['findings'] for r in real),
        'synthetic23_byte_cases_not_legal_editor_input':True,
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'Original18-byte bound verified;{len(cases)} legal-sized name boundary layouts,{len(findings)} findings.',flush=True)


if __name__=='__main__':main()
