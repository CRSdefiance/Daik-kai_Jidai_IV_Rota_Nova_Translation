"""Record reviewed native previews and create the scoped battle-consumer auditor."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_battle_personal_prose_v891 import MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_personal_v893')
PRODUCTION=Path('translations/battle_personal_editorial_manuscript_v2.json')


def main():
    assert not PRODUCTION.exists();ROOT.mkdir(parents=True,exist_ok=True)
    path=Path('work/analysis/battle_personal_v892/native_font_proof.json');fonts=read(path)
    assert tuple(c['message_id'] for c in fonts['cases'])==IDS
    assert fonts['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    for case in fonts['cases']:
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        assert case['all_body_ink_inside_registered216x36_crop']
    visual=Path('work/analysis/battle_personal_v892/visual_review.json')
    assert not visual.exists()
    save(visual,{'native_font_proof':str(path),'native_font_proof_sha256':sha(path.read_bytes()),
        'review_sheet':fonts['review_sheet'],'review_sheet_sha256':fonts['review_sheet_sha256'],
        'all25_previews_visually_reviewed':True,'native_IDs':list(IDS),'visual_review_pending':False,
        'findings':'All25 complete source-native body previews reviewed. Every row starts at x0;all leading/trailing letters and punctuation are present. Book title,drink joke,sword/model care,experiment,nodding direction and sleep/refusal continuations fit the native216x36 visible crop. No word splits,padding gaps,stray storage text or extra pages. Actual RGB battle UI and normal transitions remain pending.',
        'research_scope':'CPU-only battle predicate and role/UI fixtures;not an emulator gameplay capture.',
        'full_goal_complete':False})
    doc=deepcopy(read(MANUSCRIPT))
    doc['reviewed_research_manuscript']=str(MANUSCRIPT)
    doc['reviewed_research_manuscript_sha256']=sha(MANUSCRIPT.read_bytes())
    for key,p in [('native_font_proof',path),('visual_review_proof',visual)]:
        doc[key]=str(p);doc[key+'_sha256']=sha(p.read_bytes())
    doc['formatting_review_pending']=False
    doc['review_gates']=['source','context','localization','naturalness','formatting']
    doc['status']='25-source-prose-native-font-and-visual-reviewed-registered-release-and-actual-pending'
    for row in doc['records']:
        row['review']['formatting']=True
        if row['message_id']==1575:
            row['localization_note']=row['localization_note'].replace('Kaizen Jiten','Kaisen Jiten')
    doc['draft_note_correction']='Corrects the romanization typo Kaizen to Kaisen in1575 explanatory note;Japanese source,source gloss and shipped English are unchanged.'
    save(PRODUCTION,doc)
    source=Path('scripts/audit_gunnery_deck_native_v888.py');before=source.read_bytes()
    text=before.decode('utf-8')
    for old,new in [('gunnery_deck_editorial','battle_personal_editorial'),('gunnery_deck_layout_v887','battle_personal_layout_v892'),
        ('deck-gunnery-deck-visible-v1','deck-battle-personal-visible-v1'),('all50_original_role_helper_selections','all125_original_selector_and_discriminating_control_cases'),
        ("==50","==125"),('probe_gunnery_deck_fonts_v887','probe_battle_personal_fonts_v892'),
        ('scripts/gunnery_deck_layout_v887.py','scripts/battle_personal_layout_v892.py'),
        ('all24_previews_visually_reviewed','all25_previews_visually_reviewed'),('all24_native_previews_visually_reviewed','all25_native_previews_visually_reviewed'),
        ('==24','==25'),('24 records','25 records'),('all24 source','all25 source'),
        ('Gunnery and deck cleaning native-consumer audit','Battle personal native-consumer audit')]:
        if old=='scripts/gunnery_deck_layout_v887.py':continue
        assert old in text,old;text=text.replace(old,new)
    target=Path('scripts/audit_battle_personal_native_v893.py');assert not target.exists()
    with target.open('x',encoding='utf-8') as f:f.write(text)
    assert source.read_bytes()==before
    save(ROOT/'auditor_successor_provenance.json',{'source':str(source),'source_sha256':sha(before),
        'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,
        'successor':str(target),'successor_sha256':sha(target.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('25 native previews visually reviewed;production manuscript and scoped successor auditor created. Actual battle display pending.',flush=True)


if __name__=='__main__':main()
