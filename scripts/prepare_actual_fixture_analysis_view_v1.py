"""Derive native page/actor counts without changing an immutable actual-run fixture."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['fixture','native','out']:parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists();original,native=map(load,[args.fixture,args.native])
    byid={r['id']:r for r in native['records']};doc=deepcopy(original);pages=0
    for row in doc['selected_records']:
        value=byid[row['id']];assert bytes.fromhex(row['expected_expanded_body_hex']).rstrip(b' ')==bytes.fromhex(value['expanded_native_hex']).rstrip(b' ')
        display=value['complete_native_English_display'];pages+=1 if row['selector']==254 else len(display['pages'])
    doc.update(expected_pages=pages,ordinary_actor_IDs=sorted({r['selector'] for r in doc['selected_records'] if r['selector']!=254}),
        original_run_fixture=str(args.fixture),original_run_fixture_sha256=sha(args.fixture.read_bytes()),
        original_run_ROM_inputs_frames_commands_andbody_bindings_preserved=True,
        native_source=str(args.native),native_source_sha256=sha(args.native.read_bytes()),new_credit=0)
    assert all(doc[k]==v for k,v in original.items());save(args.out,doc)
    print('Derived',len(doc['selected_records']),'utterances/',pages,'native pages for exact',doc['frames'],'frame run;original fixture unchanged.')
