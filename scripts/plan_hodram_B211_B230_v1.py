"""Use the qualified Hodram planner with exact source/current body and style bindings."""
from pathlib import Path
from types import FunctionType
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts import plan_editorial_scene_prose_v19 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.finish_hodram_B211_B230_contextual_v1 import OUT as PROSE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B211_B230_formatting_v1 import MACROS,TERMS,ROLES
from scripts.review_hodram_B211_B230_names_v1 import NATIVE as NAMES,OUT as NAME_REVIEW
from scripts.review_hodram_B221_B230_contextual_v1 import CURRENT,OBJECTS

def qualify_source(doc):
    current,objects,prose,macros,terms,names,roles=map(load,(CURRENT,OBJECTS,PROSE,MACROS,TERMS,NAMES,ROLES))
    assert doc['runtime']==current['runtime']==objects['runtime']==macros['runtime']==terms['runtime']==names['runtime']==roles['runtime']
    assert doc['file_path']=='/data/SC1.DK4' and doc['blocks']==list(range(211,231))
    assert doc['physical_speech_objects']==270 and doc['all_individual_four_prose_gates_pass']
    for key,path in [('source_full_manuscript_sha256',PROSE),('scoped_names_sha256',NAME_REVIEW),
            ('native_names_sha256',NAMES),('macro_proof_sha256',MACROS),('term_proof_sha256',TERMS),('dynamic_roles_sha256',ROLES)]:
        assert doc[key]==digest(path)
    assert macros['macro_ascii_lengths']==dict(FI=6,FA=9,FO=15)
    assert current['all_source_preambles_andcommand_kinds_preserved']
    clean_path=Path('work/clean.nds');assert digest(clean_path)=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    image=NdsImage.open(doc['current_ROM'])
    assert digest(doc['current_ROM'])==doc['current_ROM_sha256']==current['runtime']['candidate_sha256']
    from dk4tool.patch.grand_race_menu_release import sha
    assert sha(image.read_file('/__arm9__.bin'))==current['runtime']['ARM9_sha256']
    assert sha(image.read_file(doc['file_path']))==doc['current_archive_sha256']
    clean,bank=[IlnkContainer.parse(im.read_file(doc['file_path'])).blocks for im in (NdsImage.open(clean_path),image)]
    ordinary={r['id']:r for g in current['groups'] for r in g['records']}
    styles={r['id']:r for r in objects['style_records']}
    originals={r['id']:r for r in prose['records']}
    allowed=set(names['actors'])|{r['source_selector'] for r in roles['native_roles']['rows']}|{254}
    zeros=set();bindings=[]
    for row in doc['records']:
        assert row['english']==originals[row['id']]['english'] and row['review']==originals[row['id']]['review']
        if row['kind']=='typed-choice-label':continue
        raw,stored=map(bytes.fromhex,(row['source_hex'],row['current_hex']))
        sr,cr=row['source_reference'],row['current_reference'];block=row['block']
        assert row['source_selector'] in allowed
        assert clean[block][sr['offset']:sr['offset']+len(raw)+1]==raw+b'\0'
        assert bank[block][cr['offset']:cr['offset']+len(stored)+1]==stored+b'\0'
        if row.get('native_object_kind')=='4100-style-alternative':
            original=styles[row['id']]
            assert all(row[k]==original[k] for k in ['source_reference','current_reference','source_hex','current_hex',
                'source_header_hex','source_choice_object_hex','current_style_object_hex','source_style_indices','current_style_indices'])
            head=bytes.fromhex(row['source_header_hex'])
            assert len(head)==20 and head[:2]==b'\0A' and head[-2:]==bytes([0,row['source_selector']])
            assert clean[block][sr['command_offset']:sr['command_offset']+20]==head
            assert row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
        else:
            original=ordinary[row['id']]
            assert all(row[k]==original[k] for k in ['source_reference','current_reference','source_hex','current_hex','source_complete_preamble_hex'])
            head=bytes.fromhex(row['source_complete_preamble_hex'])
            assert len(head)==6 and head[:5]==bytes.fromhex('0040ffff00') and head[-1]==raw[0]==stored[0]==row['source_selector']
            assert clean[block][sr['offset']-5:sr['offset']+len(raw)+1]==head[:5]+raw+b'\0'
            assert bank[block][cr['offset']-5:cr['offset']+len(stored)+1]==head[:5]+stored+b'\0'
            if raw[0]==0:zeros.add(raw)
            if raw[0]==254:assert row['source_FE_presentation_kind'] and row['FE_is_not_an_ordinary_actor_nameplate']
        bindings.append(dict(id=row['id'],source_reference=sr,current_reference=cr,
            complete_source_header_hex=head.hex(),source_body_sha256=sha(raw),
            scoped_identity_binding=str(NAMES),scoped_identity_binding_sha256=digest(NAMES)))
    assert len(bindings)==270
    return zeros,bindings

main=FunctionType(previous.main.__code__,{**previous.main.__globals__,'qualify_source':qualify_source,
    '__file__':__file__},argdefs=previous.main.__defaults__)

if __name__=='__main__':main()
