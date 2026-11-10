"""Prepare fresh native plans for the ordinary B166–B167 speech and modal bodies."""
import linecache
from pathlib import Path
import re

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts import plan_rafael_B177_B180_v1 as previous
from scripts.qualify_rafael_B166_B167_names_v1 import CURRENT, IDENTITY, MACROS
from scripts.write_rafael_B166_B167_contextual_v1 import OUT as PROSE
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = CURRENT.parent
FORMATTING = ROOT / 'ordinary_formatting_manuscript_v1.json'
PREFERENCES = ROOT / 'ordinary_visual_preferences_v1.json'
STAGED = ROOT / 'source_staged_FE_inputs_v1.json'
TOKEN = re.compile(r'\b(FI|FA|FO|FU)\b')
PLAIN_FE = {526,538,564,572,595,610,629}


def prepare():
    assert not any(p.exists() for p in (FORMATTING,PREFERENCES,STAGED))
    doc, ident = map(load,(PROSE,IDENTITY))
    assert ident['runtime']==doc['runtime'] and ident['exact_unchanged_actor0_macro_dependencies']
    assert ident['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10,FU=13)
    assert ident['evidence'][str(MACROS)]==sha(MACROS.read_bytes())
    ordinary,staged=[],[]
    for row in doc['records']:
        assert not row['review']['formatting']
        row['editorial_logical_English']=row['english']
        tokens = TOKEN.findall(row['english'])
        assert tokens==row['native_literal_tokens']
        row['english']=TOKEN.sub(lambda m:'{MACRO:'+m[0]+'}',row['english'])
        row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
        row['prior_macro_normalized_comparison']=None
        if not row['english'].isascii():
            assert row['decision']=='retention' and row['deliberate_source_punctuation_retention']
            row['prior_macro_normalized_comparison']=row['current_comparison_paragraph']
            assert row['prior_macro_normalized_comparison']==row['english']
        if row['kind']=='system-FE':
            assert row['source_complete_preamble_hex']=='0040ffff00fe'
            row['FE_is_not_an_ordinary_actor_nameplate']=True
            if row['source_record_index'] not in PLAIN_FE:
                staged.append(row)
                continue
            row['source_FE_presentation_kind']='Ordinary FE prose within a source-qualified exchange'
        ordinary.append(row)
    assert (len(ordinary),len(staged))==(164,22)
    assert sum(len(r['native_literal_tokens']) for r in ordinary+staged)==12
    proof=dict(manuscript_sha256=sha(PROSE.read_bytes()),scoped_identity_proof_sha256=sha(IDENTITY.read_bytes()),
        reused_macro_proof_sha256=sha(MACROS.read_bytes()),no_prose_changes_or_manual_breaks=True,
        typed_choice_objects=0)
    save(FORMATTING,{**doc,**proof,'records':ordinary,'physical_speech_objects':164,
        'complete_contextual_batch_records':186,'ordinary_subset_only_pending_staged_FE_merge':True})
    save(STAGED,{**proof,'runtime':doc['runtime'],'records':staged,'source_staging_only_no_display_approval':True})
    save(PREFERENCES,dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_old_record_specific_guard_orsemantic_preference_inherited=True,author_inserted_ordinary_breaks=0,new_credit=0))
    print('164 ordinary records ready for fresh wrapping and 22 source-staged FE inputs isolated for layout checks.')


def qualify_source(doc):
    current, ident = map(load,(CURRENT,IDENTITY))
    assert doc['blocks']==[166,167] and doc['all_individual_four_prose_gates_pass']
    assert doc['runtime']==current['runtime']==ident['runtime']
    assert doc['scoped_identity_proof_sha256']==sha(IDENTITY.read_bytes())
    assert doc['reused_macro_proof_sha256']==sha(MACROS.read_bytes())
    assert current['all_source_preambles_andcommand_kinds_preserved']
    assert all(c['word'] not in (0x2100,0x2200,0x4100) for g in current['groups'] for c in g['all_source_commands'])
    clean_path,current_path = Path('work/clean.nds'),Path(doc['current_ROM'])
    assert sha(clean_path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(current_path.read_bytes())==doc['current_ROM_sha256']==ident['runtime']['candidate_sha256']
    image=NdsImage.open(current_path)
    assert sha(image.read_file('/__arm9__.bin'))==ident['runtime']['ARM9_sha256']
    archive=doc['file_path']
    assert archive=='/data/SC0.DK4'
    raw_current=image.read_file(archive)
    assert sha(raw_current)==doc['current_archive_sha256']
    clean=IlnkContainer.parse(NdsImage.open(clean_path).read_file(archive)).blocks
    bank=IlnkContainer.parse(raw_current).blocks
    originals={r['id']:r for g in current['groups'] for r in g['records']}
    zeros,bindings=set(),[]
    for row in doc['records']:
        sr,cr=row['source_reference'],row['current_reference']
        b,selector=row['block'],row['source_selector']
        keys=['source_reference','current_reference','source_hex','current_hex','source_complete_preamble_hex']
        assert all(row[k]==originals[row['id']][k] for k in keys)
        raw,stored,head=(bytes.fromhex(row[k]) for k in keys[2:])
        assert head==bytes.fromhex('0040ffff00')+bytes([selector])
        assert raw[0]==stored[0]==selector and selector in set(ident['actors'])|{254}
        assert all(b'\0' not in body[1:] for body in (raw,stored))
        for blocks,ref,body in ((clean,sr,raw),(bank,cr,stored)):
            assert blocks[b][ref['header_offset']:ref['offset']+len(body)+1]==head[:5]+body+b'\0'
        if not selector:
            zeros.add(raw)
        bindings.append(dict(id=row['id'],source_reference=sr,current_reference=cr,complete_source_preamble_hex=head.hex(),
            source_body_sha256=sha(raw),selector00_owned_by_complete_preamble=selector==0,
            scoped_identity_binding=str(IDENTITY),scoped_identity_binding_sha256=doc['scoped_identity_proof_sha256']))
    assert len(bindings)==164
    return zeros,bindings


source = checked_text(previous.source,{
    "'Rafael early-tutorial plan:'":"'Rafael B166–B167 ordinary plan:'",
    "'Rafael-early-tutorial-RESEARCH-ONLY:'":"'Rafael-B166-B167-RESEARCH-ONLY:'",
})
env = {**previous.env,'__file__':__file__,'qualify_source':qualify_source}
filename=__file__+'::same-qualified-native-planner-for-ordinary-bodies'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
if __name__=='__main__':
    import sys
    if sys.argv[1:]==['--prepare']:
        prepare()
    else:
        env['main']()
