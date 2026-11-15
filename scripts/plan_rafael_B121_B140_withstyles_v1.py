"""Reuse qualified paragraph geometry with fresh bindings for341 bodies and ten captions."""
import linecache
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import plan_rafael_B101_B120_withstyles_v2 as previous

CURRENT = Path('work/analysis/Rafael_B121_B140_current678_20261105/current_effective.json')
OBJECTS = Path('work/analysis/Rafael351_current_objects_v1_20261105/current_objects.json')
IDENTITY = Path('work/analysis/Rafael351_identity_note_alignment_v1_20261105/qualified_names_roles_andparticle_findings.json')
TERMS = Path('work/analysis/Rafael351_item_UI_terms_v1_20261105/term_bindings.json')
MACROS = Path('work/analysis/Rafael261_names_terms_20261105/names_macros_andconsumer_dependency_qualification_v1.json')


def qualify_source(doc):
    current, objects, identity, terms, macros = map(load,[CURRENT,OBJECTS,IDENTITY,TERMS,MACROS])
    assert current['runtime'] == objects['runtime'] == identity['runtime'] == terms['runtime']
    assert doc['file_path'] == '/data/SC0.DK4' and doc['blocks'] == list(range(121,141))
    assert doc['all351_individual_four_prose_gates_pass'] and not doc['pending_name_term_IDs']
    assert doc['scoped_identity_proof_sha256'] == sha(IDENTITY.read_bytes())
    assert doc['scoped_term_proof_sha256'] == sha(TERMS.read_bytes())
    assert macros['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']
    assert macros['macro_ascii_lengths'] == dict(FI=6,FA=6,FO=10)
    assert all(macros['runtime'][k]==current['runtime'][k] for k in ['ARM9_sha256','COMMON_sha256'])
    assert str(MACROS) in identity['evidence'] and sha(MACROS.read_bytes()) == identity['evidence'][str(MACROS)]
    assert current['all_source_preambles_andcommand_kinds_preserved']
    image = NdsImage.open(doc['current_ROM']); cleanpath = Path('work/clean.nds')
    assert sha(cleanpath.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256'] == current['runtime']['candidate_sha256']
    assert sha(image.read_file('/__arm9__.bin')) == current['runtime']['ARM9_sha256']
    assert sha(image.read_file(doc['file_path'])) == doc['current_archive_sha256']
    clean = IlnkContainer.parse(NdsImage.open(cleanpath).read_file(doc['file_path'])).blocks
    bank = IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    ordinary = {r['id']:r for g in current['groups'] for r in g['records']}
    styles = {r['id']:r for r in objects['style_records']}
    zeros, bindings = set(), []
    allowed = set(identity['actors'])|{r['source_selector'] for r in identity['dynamic_roles']}|{254}
    for row in doc['records']:
        if row['kind']=='typed-choice-label': continue
        raw,stored = map(bytes.fromhex,[row['source_hex'],row['current_hex']])
        sr,cr = row['source_reference'],row['current_reference']
        assert row['source_selector'] in allowed
        assert clean[row['block']][sr['offset']:sr['offset']+len(raw)+1] == raw+b'\0'
        assert bank[row['block']][cr['offset']:cr['offset']+len(stored)+1] == stored+b'\0'
        if row.get('native_object_kind') == '4100-style-alternative':
            original = styles[row['id']]
            assert all(row[k] == original[k] for k in ['source_reference','current_reference','source_hex','current_hex',
                'source_header_hex','source_choice_object_hex','current_style_object_hex','source_style_indices','current_style_indices'])
            head = bytes.fromhex(row['source_header_hex'])
            assert len(head)==20 and head[:2]==b'\0A' and head[-2:]==bytes([0,row['source_selector']])
            assert clean[row['block']][sr['command_offset']:sr['command_offset']+20]==head
            assert row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
        else:
            original = ordinary[row['id']]
            assert all(row[k] == original[k] for k in ['source_reference','current_reference','source_hex','current_hex','source_complete_preamble_hex'])
            head = bytes.fromhex(row['source_complete_preamble_hex'])
            assert len(head)==6 and head[:5]==bytes.fromhex('0040ffff00') and head[-1]==raw[0]==stored[0]==row['source_selector']
            assert b'\0' not in raw[1:] and b'\0' not in stored[1:]
            assert clean[row['block']][sr['header_offset']:sr['offset']+len(raw)+1] == head[:5]+raw+b'\0'
            assert bank[row['block']][cr['header_offset']:cr['offset']+len(stored)+1] == head[:5]+stored+b'\0'
            if raw[0]==0: zeros.add(raw)
            if raw[0]==254: assert row['source_FE_presentation_kind'] and row['FE_is_not_an_ordinary_actor_nameplate']
        bindings.append(dict(id=row['id'],source_reference=sr,current_reference=cr,
            complete_source_header_hex=head.hex(),source_body_sha256=sha(raw),
            scoped_identity_binding=str(IDENTITY),scoped_identity_binding_sha256=sha(IDENTITY.read_bytes()),
            source_object_binding=str(OBJECTS if row['id'] in styles else CURRENT),
            macro_dependency_reuse=str(MACROS),macro_dependency_reuse_sha256=sha(MACROS.read_bytes()),
            no_new_native_dispatch_orconditional_activation_claim=True))
    assert len(bindings)==341 and {r['id'] for r in bindings} == set(ordinary)|set(styles)
    return zeros, bindings


source = checked_text(previous.source, {
    "fe_cells={'DK4_MES_B118_R0022':36,'DK4_MES_B127_R0053':36,'DK4_MES_B134_R0028':37,'DK4_MES_B135_R0035':36,'DK4_MES_B136_R0027':36}":
        'fe_cells={}  # No record-specific old guard budget is inherited for changed prose.',
})
env = {**previous.env,'qualify_source':qualify_source,'__file__':__file__}
filename = __file__+'::same-native-paragraph-geometry-new351-exact-bindings'
linecache.cache[filename] = (len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main = env['main']
if __name__ == '__main__': main()
