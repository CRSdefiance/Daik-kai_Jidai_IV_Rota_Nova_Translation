"""Preserve229 qualified plans andadd14 complete source-bound runtime-style alternatives."""
import linecache
from pathlib import Path
from scripts import plan_rafael_B101_B120_v1 as previous
from scripts.audit_story_glyph_consistency import load
from dk4tool.patch.grand_race_menu_release import sha

OBJECTS=Path('work/analysis/Rafael14_style_current678_20261105/current_objects.json')
QUAL=Path('work/analysis/Rafael255_extended_identity_20261105.json')

def qualify_source(doc):
    assert doc['all255_individual_four_prose_gates_pass']
    base={**doc,'records':[r for r in doc['records'] if r.get('native_object_kind')!='4100-style-alternative'],
        'scoped_identity_proof_sha256':sha(previous.PROOF.read_bytes())}
    zeros,bindings=previous.qualify_source(base)
    objects,identity=map(load,[OBJECTS,QUAL])
    assert doc['scoped_identity_proof_sha256']==sha(QUAL.read_bytes()) and identity['runtime']==objects['runtime']
    originals={r['id']:r for r in objects['style_records']}
    for row in doc['records']:
        if row.get('native_object_kind')!='4100-style-alternative':continue
        original=originals[row['id']]
        assert all(row[k]==original[k] for k in ['source_reference','current_reference','source_hex','current_hex',
            'source_header_hex','source_choice_object_hex','current_style_object_hex','source_style_indices','current_style_indices'])
        assert row['source_selector']==208 and row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
        assert bytes.fromhex(row['source_header_hex'])[18:20]==b'\0\xd0'
        bindings.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            exact_source_header_hex=row['source_header_hex'],source_style_indices=row['source_style_indices'],
            complete_compound_binding=str(OBJECTS),complete_compound_binding_sha256=sha(OBJECTS.read_bytes()),
            runtime_identity_binding=str(QUAL),runtime_identity_binding_sha256=sha(QUAL.read_bytes()),
            virtual_prefix_not_in_stored_source_orcurrent_body=True))
    assert len(bindings)==243
    return zeros,bindings

env={**previous.env,'qualify_source':qualify_source,'__file__':__file__}
source=previous.source
filename=__file__+'::same-native-geometry-243-complete-source-bound-bodies'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
