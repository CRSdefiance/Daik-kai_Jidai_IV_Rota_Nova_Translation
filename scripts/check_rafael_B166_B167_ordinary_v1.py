"""Refine one modal line and bind the unchanged native page checker to Rafael1674."""
from pathlib import Path
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts import check_rafael_compiled_pages_v3 as native
from scripts import plan_rafael_B166_B167_ordinary_v1 as planning
from scripts.audit_story_glyph_consistency import load, save
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = planning.ROOT
OLD = planning.PROSE
PROSE = OLD.with_name('rafael_B166_B167_contextual_review_v2.json')
FORMATTING = ROOT / 'ordinary_formatting_manuscript_v2.json'
STAGED = planning.STAGED
PREFERENCES = ROOT / 'ordinary_FE_reserve_v2.json'
ID = 'DK4_MES_B166_R0595'
TEXT = "Yes. Admiral Albuquerque was already Portugal's naval commander in chief. A sailor like me, viceroy? It just doesn't seem right."


def prepare():
    assert not any(p.exists() for p in (PROSE,FORMATTING,PREFERENCES))
    doc, ordinary, reserves = map(load,(OLD,planning.FORMATTING,ROOT/'ordinary_FE_reserve_trials_v1.json'))
    source_row=next(r for r in doc['records'] if r['id']==ID)
    layout_row=next(r for r in ordinary['records'] if r['id']==ID)
    assert source_row['english']==layout_row['editorial_logical_English']
    old=source_row['english']
    note=source_row['finding'] + ' Read aloud, the natural placement of already keeps the title, nationality and sequence clear.'
    for row in (source_row,layout_row):
        row.update(english=TEXT,finding=note,localization_note=note,previous_review_English=old)
    layout_row.update(editorial_logical_English=TEXT,planned_English_markup='{SPEAKER:FE}'+TEXT)
    evidence = {str(p):sha(p.read_bytes()) for p in (OLD,ROOT/'ordinary_plans_v3/diagnostics.json',Path(__file__))}
    doc.update(single_read_aloud_refinement=ID,prior_contextual_version=str(OLD),evidence={**doc['evidence'],**evidence})
    save(PROSE,doc)
    ordinary.update(manuscript_sha256=sha(PROSE.read_bytes()),parent_contextual_proof=str(PROSE))
    save(FORMATTING,ordinary)
    reserves['records'][ID]['bindings']['english']=sha(TEXT.encode('utf-8'))
    save(PREFERENCES,reserves)
    print('One read-aloud refinement saved. All other 185 decisions are byte-identical in JSON values.')


source = checked_text(native.source,{
    "    assert qualified['runtime']==ctx.receipt()":
        "    identity=load(IDENTITY)\n    assert identity['runtime']==ctx.receipt() and identity['exact_unchanged_actor0_macro_dependencies']\n    assert identity['evidence'][str(MACRO_QUALIFICATION)]==sha(MACRO_QUALIFICATION.read_bytes())",
    "doc['scoped_identity_proof_sha256']==sha(MACRO_QUALIFICATION.read_bytes())":
        "doc['scoped_identity_proof_sha256']==sha(IDENTITY.read_bytes())",
    'args.manuscript,args.plan,SOURCE,MACROS,MACRO_QUALIFICATION,':
        'args.manuscript,args.plan,SOURCE,MACROS,MACRO_QUALIFICATION,IDENTITY,',
})
env = {**native.env,'IDENTITY':planning.IDENTITY,'__file__':__file__}
exec(compile(source,__file__+'::same-native-guards-and-runtime-qualified-FU','exec'),env)
if __name__=='__main__':
    if sys.argv[1:]==['--prepare']:
        prepare()
    else:
        env['main']()
