"""Reuse calibrated formatting with the nine exact B168 Rafael preambles and a source comic literal."""
import struct
from pathlib import Path
from types import FunctionType,SimpleNamespace

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import plan_editorial_scene_prose_v13 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text


def qualify_source(doc):
    assert doc['file_path']=='/data/SC1.DK4'
    proof_path=Path('work/analysis/Hodram_B151_B170_clean_20261102/native_identity_and_item_checkpoint_v1.json')
    proof=load(proof_path);declared={r['id']:r for r in proof['Rafael_actor0_complete_preamble_records']}
    clean_path=Path('work/clean.nds');assert sha(clean_path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    blocks=IlnkContainer.parse(NdsImage.open(clean_path).read_file(doc['file_path'])).blocks
    bodies,bindings,ids=set(),[],set()
    for row in doc['records']:
        if row['kind']=='typed-choice-label':continue
        ref=row['source_reference'];raw=bytes.fromhex(row['source_hex']);block=blocks[row['block']]
        assert block[ref['offset']:ref['offset']+len(raw)]==raw and b'\0' not in raw[1:]
        assert row.get('native_object_kind')!='4100-style-alternative'
        assert not (row['block']==156 and row['source_selector']==254)
        if row['source_selector']==0:
            header=bytes.fromhex(row['source_complete_preamble_hex'])
            assert row['block']==168 and row['id'] in declared and header.hex()==declared[row['id']]['complete_preamble_hex']=='0040ffff0000'
            assert ref==declared[row['id']]['source_reference'] and block[ref['header_offset']:ref['header_offset']+6]==header
            assert raw[0]==0 and block[ref['offset']+len(raw)]==0
            bodies.add(raw);ids.add(row['id'])
            bindings.append(dict(id=row['id'],source_reference=ref,complete_source_preamble_hex=header.hex(),source_body_with_real_selector_hex=raw.hex(),
                original_Rafael_identity_proof=str(proof_path),original_Rafael_identity_proof_sha256=sha(proof_path.read_bytes()),actual_B168_gameplay_pending=True))
    assert ids==set(declared) and len(bodies)==len(bindings)==9
    return bodies,bindings


inherited=previous.main.__globals__['previous']
adapter=checked_text(inherited.ADAPTER,{"c in '…？！○×Ｉ'":"c in '…？！○×Ｉ△◎▲□◇'"})
parameters={**vars(inherited),'ADAPTER':adapter,'PAIRS':inherited.PAIRS|{('proof','of'),('of','supremacy'),('supreme','commander'),
    ('naval','commander'),('royal','academy'),('research','institute'),('market','share'),('cargo','holds'),('supply','holds'),
    ('marine','quarters'),('armed','batteries'),('last','coin'),('one','percent'),('old','hand'),('seven','seas'),('good','luck'),
    ('new','world'),('sail','handlers'),('my','family'),('new','family')}}
main=FunctionType(previous.main.__code__,{**previous.main.__globals__,'qualify_source':qualify_source,
                  'previous':SimpleNamespace(**parameters),'__file__':__file__},argdefs=previous.main.__defaults__)

if __name__=='__main__':main()
