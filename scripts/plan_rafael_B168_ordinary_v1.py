"""Run the registered native paragraph planner for the 47 B168 speeches."""
from pathlib import Path
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_rafael_B166_B167_ordinary_v1 as previous
from scripts.audit_story_glyph_consistency import load,save
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B168_contextual_v1 import CURRENT, IDENTITY, OUT as PROSE

ROOT=CURRENT.parent
FORMATTING=ROOT/'formatting_manuscript_v1.json'
PREFERENCES=ROOT/'visual_preferences_v1.json'
MACROS=previous.MACROS


def prepare():
    assert not FORMATTING.exists() and not PREFERENCES.exists()
    doc,ident=map(load,(PROSE,IDENTITY))
    assert ident['runtime']==doc['runtime'] and ident['exact_unchanged_actor0_macro_dependencies']
    assert ident['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10,FU=13)
    assert len(doc['records'])==47 and all(r['kind']=='progressive' for r in doc['records'])
    for row in doc['records']:
        assert not row['review']['formatting']
        row['editorial_logical_English']=row['english']
        assert previous.TOKEN.findall(row['english'])==row['native_literal_tokens']
        row['english']=previous.TOKEN.sub(lambda m:'{MACRO:'+m[0]+'}',row['english'])
        row['planned_English_markup']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
        row['prior_macro_normalized_comparison']=None
        if not row['english'].isascii():
            assert row['decision']=='retention' and row['deliberate_source_punctuation_retention']
            row['prior_macro_normalized_comparison']=row['current_comparison_paragraph']
    assert sum(len(r['native_literal_tokens']) for r in doc['records'])==4
    doc.update(manuscript_sha256=sha(PROSE.read_bytes()),scoped_identity_proof_sha256=sha(IDENTITY.read_bytes()),
        reused_macro_proof_sha256=sha(MACROS.read_bytes()),no_prose_changes_or_manual_breaks=True,
        typed_choice_objects=0,physical_speech_objects=47,ordinary_speech_objects=47)
    save(FORMATTING,doc)
    save(PREFERENCES,dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_old_record_specific_guard_orsemantic_preference_inherited=True,author_inserted_ordinary_breaks=0,new_credit=0))


scope=checked_text(__import__('inspect').getsource(previous.qualify_source),{
    "doc['blocks']==[166,167]":"doc['blocks']==[168]",
    'len(bindings)==164':'len(bindings)==47',
})
env={**previous.env,'__file__':__file__}
source_env={**previous.qualify_source.__globals__,'CURRENT':CURRENT,'IDENTITY':IDENTITY}
exec(compile(scope,__file__+'::exact-B168-source-current-scope','exec'),source_env)
env['qualify_source']=source_env['qualify_source']
main=FunctionType(previous.env['main'].__code__,env)
if __name__=='__main__':
    import sys
    if sys.argv[1:]==['--prepare']:
        prepare()
    else:
        main()
