"""Preserve the three source-authored rows of the parrot chase sound effects."""
from pathlib import Path

from scripts.plan_rafael_B201_B220_v1 import ROOT, FORMATTING
from scripts.audit_story_glyph_consistency import load, save
from scripts.source_locked_derivation_v5118 import checked_text


TEMPLATE = Path('scripts/check_rafael_B216_signature_v1.py')
STAGED = ROOT/'source_staged_parrot_FE_inputs_v1.json'
ID = 'DK4_MES_B217_R0052'
EFFECT_ROWS = ['Flap, flap! Bang! Crack!', 'Flap!', 'Thump! Rustle!']


def prepare():
    assert not STAGED.exists()
    manuscript = load(FORMATTING)
    row, = (r for r in manuscript['records'] if r['id']==ID)
    assert row['kind']=='system-FE' and row['english']==' '.join(EFFECT_ROWS)
    row['localized_effect_rows'] = EFFECT_ROWS
    save(STAGED,dict(runtime=manuscript['runtime'],records=[row],source_staging_only_no_display_approval=True))


source = checked_text(TEMPLATE.read_text(encoding='utf-8'),{
    'from scripts.plan_rafael_B201_B220_v1 import ROOT, STAGED, STAGED_ID, digest':
        'from scripts.plan_rafael_B201_B220_v1 import digest\nSTAGED_ID = ID',
    "OUT = ROOT / 'staged_FE_native_v1'": "OUT = ROOT / 'staged_parrot_FE_native_v1'",
    """    assert len(clean_rows) == len(current_rows) == 2
    assert clean_rows[0] == (0,0,'じゃあ、元気でな')
    assert clean_rows[1] == (12,36,'ジャム・ジャック・ルドワイヤン')
    print('Letter rows (clean/current):', clean_rows, current_rows, flush=True)
    shape = [(clean_rows[i][1], row[k]) for i,k in enumerate(('localized_letter_farewell','localized_signature'))]""":
        """    assert [(y,x) for y,x,_ in clean_rows] == [(0,0),(12,0),(24,0)]
    assert clean_rows[1][2] == 'バサッ！'
    assert len(current_rows) in (2,3,4)
    print('Chase effect rows (clean/current):', clean_rows, current_rows, flush=True)
    shape = [(x,english) for (_,x,_),english in zip(clean_rows,row['localized_effect_rows'],strict=True)]""",
    'The farewell and signature did not reach the original row origins.':
        'The three chase beats did not reach the original row origins.',
    'Castle letter farewell and signature': 'Parrot chase sound effects',
    'Preserve the source farewell row and the separate indented author signature.':
        'Preserve the separate wingbeat between the opening racket and the final thump and rustle.',
    'Two original letter row origins': 'Three original chase sound-effect rows',
    "if __name__ == '__main__':\n    main()": "if __name__ == '__main__':\n    prepare()\n    main()",
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::three-original-parrot-sound-effect-rows','exec'),globals())

