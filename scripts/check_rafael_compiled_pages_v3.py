"""Add qualified FU expected text to the unchanged complete native page/ABI checks."""
from pathlib import Path
from scripts import check_rafael_compiled_pages_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

MACRO_QUALIFICATION=Path('work/analysis/Rafael557_macros_inputs_v1_20261105/qualified_identity_andmacros.json')
source=checked_text(previous.source,{
    '    font=ctx.image.read_file(\'/GRP/KANJI.FNT\')':
        "    qualified=load(MACRO_QUALIFICATION)\n    assert qualified['runtime']==ctx.receipt()\n    assert qualified['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10,FU=13)\n    assert qualified['full_name']=='Rafael Castor'\n    assert doc['scoped_identity_proof_sha256']==sha(MACRO_QUALIFICATION.read_bytes())\n    font=ctx.image.read_file('/GRP/KANJI.FNT')",
    "expected=body.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')":
        "expected=body.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.').replace(b'FU',b'Rafael Castor')",
    "logical=row['english'].replace('{LB}',' ').replace('{MACRO:FI}','Rafael').replace('{MACRO:FA}','Castor').replace('{MACRO:FO}','Castor Co.')":
        "logical=row['english'].replace('{LB}',' ').replace('{MACRO:FI}','Rafael').replace('{MACRO:FA}','Castor').replace('{MACRO:FO}','Castor Co.').replace('{MACRO:FU}','Rafael Castor')",
    'args.manuscript,args.plan,SOURCE,MACROS,':
        'args.manuscript,args.plan,SOURCE,MACROS,MACRO_QUALIFICATION,',
})
env={**vars(previous),'MACRO_QUALIFICATION':MACRO_QUALIFICATION,'__file__':__file__}
exec(compile(source,__file__+'::same-native-checks-with-qualified-full-name-expectations','exec'),env)
main=env['main']
if __name__=='__main__':main()
