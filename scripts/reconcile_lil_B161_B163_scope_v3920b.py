"""Use the actual name-proof evidence schema and registered naming-policy path; preserve failed draft."""
from pathlib import Path
if __name__=='__main__':
    DRAFT=Path('scripts/reconcile_lil_B161_B163_scope_v3920.py');t=DRAFT.read_text(encoding='utf-8');changes={'lil_B161_B163_scope_v3920':'lil_B161_B163_scope_v3920b',"==names['source_context_sha256']":"==names['evidence'][str(SOURCE)]","docs/naming_policy.md":"translations/character_name_localization_policy_v1.json",'for p in [SOURCE,GLOSS,VOICE,ENTRY,NAMES,cp,policy,Path(__file__)]':'for p in [DRAFT,SOURCE,GLOSS,VOICE,ENTRY,NAMES,cp,policy,Path(__file__)]'}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    exec(compile(t,__file__,'exec'),dict(__name__='__main__',__file__=__file__,DRAFT=DRAFT))
