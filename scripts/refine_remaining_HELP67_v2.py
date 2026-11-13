"""Clarify native Product in the heading; keep good body wording and bind semantic page preferences."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Shared_HELP_T133_T201_clean_20261105')
if __name__=='__main__':
    prior=ROOT/'whole_article_comparisons_v1.json';out=ROOT/'whole_article_comparisons_v2.json';assert not out.exists()
    doc=deepcopy(load(prior))
    for row in doc['records']:
        if row['topic_id']==150:
            text=row['english'];marker='You must obtain';at=text.index(marker)
            row['semantic_sections']=[text[:at].strip(),text[at:].strip()]
            row['semantic_section_reason']='Keep the initial contract prerequisite and home-port qualification together after the ordinary share-acquisition explanation; preserve all words, with automatic page boundaries.'
        if row['topic_id']==194:
            row['heading']='Products (Raw Materials)'
            row['english']=row['english'].replace('Products are raw materials that can create','Products can create')
            row['finding']='Bind the native Product category and explain raw materials in the heading. Retain the existing natural body apart from Product/Trade House terminology; no repeated definition is needed. Preserve suitability, five-specialty ceiling and high-share advice.'
            row['localization_note']=row['finding']
    doc.update(previous_comparisons=str(prior),previous_comparisons_sha256=sha(prior.read_bytes()),proposed_revisions=7,justified_retentions=60)
    doc['evidence'][str(Path(__file__))]=sha(Path(__file__).read_bytes());save(out,doc)
    print('Preserved all67 decisions;Product/raw-material heading avoids redundant definition. Share prerequisite remains a complete source concept.')
