"""Apply direct29-page findings without shortening good body text ordiscarding prior evidence."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text

BASE=Path('work/analysis/Shared_HELP_T21_T43_clean_20261104')
old=BASE/'whole_article_comparisons_v4.json';new=BASE/'whole_article_comparisons_v5.json'
if __name__=='__main__':
    assert not new.exists();doc=load(old)
    row=next(r for r in doc['records'] if r['topic_id']==22)
    assert 'An [[119|Purser]]' in row['english'];row['english']=row['english'].replace('An [[119|Purser]]','A [[119|Purser]]')
    row['finding']+=' Direct first-preview review catches the article left overfromaccountant→Purser:correct An Purser toA Purser. Full instruction meaning andall links remain.'
    doc['previous_comparison']=str(old);doc['previous_comparison_sha256']=sha(old.read_bytes());doc['evidence'][str(Path(__file__))]=sha(Path(__file__).read_bytes());save(new,doc)
    source=checked_text(Path('scripts/plan_town_HELP23.py').read_text(encoding='utf-8'),{
        'reviewed_help_pages_v2':'reviewed_help_pages_v3',
        "ROOT=Path('work/analysis/Shared_HELP_T21_T43_formatting_20261104')":"ROOT=Path('work/analysis/Shared_HELP_T21_T43_formatting_20261104/refined_v2')",
        'whole_article_comparisons_v4.json':'whole_article_comparisons_v5.json',
        "        assert all(row['review'][g]":
            """        if t in [22,25,38,39]:
            marker={22:'[!]',25:'Take a [[38|',38:'Even if other factions',39:'Even if other factions'}[t]
            cut=row['english'].index(marker)
            row['semantic_sections']=[row['english'][:cut].strip(),row['english'][cut:].strip()]
            row['semantic_section_reason']={22:'Keep both original source tips withtheir markers afterthe main trading explanation.',25:'The complete source instruction totake letters tothe governor forms its own paragraph;do not split Introduction orRecommendation across pages.',38:'Group the complete100-percent exception andprohibitions afterthe basic Introduction benefits,as separate logical instructions.',39:'Group the complete100-percent exception andprohibitions afterthe basic Recommendation benefits,as separate logical instructions.'}[t]
            assert ' '.join(row['semantic_sections'])==row['english']
        assert all(row['review'][g]""",
    })
    exec(compile(source,__file__+'::same-source-bound-rebase-andpreservation-with-reviewed-flow','exec'),globals())
