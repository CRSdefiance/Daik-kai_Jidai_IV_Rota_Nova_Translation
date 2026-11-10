"""Format all remaining Help prose on the corrected31 research successor; no release or credit."""
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import source_links
from dk4tool.dialogue.reviewed_help_pages_v13 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Remaining_HELP67_formatting_20261105')
COMP=Path('work/analysis/Shared_HELP_T133_T201_clean_20261105/whole_article_comparisons_v1.json')
PARENT_PLAN=Path('work/analysis/HELP31_active_terms_20261105/production_plan_v1.json')
PARENT_QUAL=Path('work/analysis/HELP31_active_terms_20261105/preview_qualification_v1/qualification.json')

if __name__=='__main__':
    assert not ROOT.exists();doc=deepcopy(load(COMP));prior=load(PARENT_PLAN);qual=load(PARENT_QUAL)
    assert load(prior['manuscript'])['all31_individual_five_gates_pass']
    parent=NdsImage.open(qual['research_ROM']);assert sha(Path(qual['research_ROM']).read_bytes())==qual['research_ROM_sha256']
    clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');file=doc['file_path']
    raw,source,canonical=[i.read_file(file) for i in [parent,clean,base]]
    blocks,original,baseline=[IlnkContainer.parse(b).blocks for b in [raw,source,canonical]]
    assert sha(raw)==prior['target_HELP_sha256']
    for row in doc['records']:
        n=row['topic_id'];assert blocks[n].hex()==row['current_hex'] and original[n].hex()==row['source_hex']
        if n==133:
            row['semantic_sections']=[s.strip() for s in re.findall(r'[^;]+;|[^;]+$',row['english'])]
            assert len(row['semantic_sections'])==16 and ' '.join(row['semantic_sections'])==row['english']
        row.update(clean_source_hex=original[n].hex(),canonical_source_hex=baseline[n].hex(),current_source_hex=blocks[n].hex(),
            original_link_IDs=[l['topic_id'] for l in source_links(original[n])],comparison_current_reference=row['current_reference'],
            current_reference=dict(file_path=file,block=n,archive_offset=int.from_bytes(raw[8+4*n:12+4*n],'little'),bytes=len(blocks[n]),offset_table_slot=8+4*n))
    doc.update(format='dk4-remaining-help67-formatting-input-v1',current_ROM=qual['research_ROM'],current_ROM_sha256=qual['research_ROM_sha256'],
        source_clean_HELP_sha256=sha(source),source_canonical_HELP_sha256=sha(canonical),source_current_HELP_sha256=sha(raw),
        current_topic_count=217,source_topic_count=202,registered_parent_pending=True,new_credit=0)
    doc['evidence'].update({str(p):sha(p.read_bytes()) for p in [COMP,PARENT_PLAN,PARENT_QUAL,Path(__file__),Path('dk4tool/dialogue/reviewed_help_pages_v13.py')]})
    resource,plan=plan_articles(doc,source,canonical,raw,require_formatting=False)
    ROOT.mkdir();manuscript=ROOT/'formatting_input_v1.json';save(manuscript,doc);output=ROOT/'Remaining_HELP67_RESEARCH_ONLY.DK4';output.write_bytes(resource)
    save(ROOT/'automatic_plans_v1.json',dict(**plan,manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),research_resource=str(output),
        current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],all_fresh_native_visual_actual_andformatting_gates_pending=True,new_credit=0))
    print(dict(articles=67,pages=len(plan['pages']),topics=plan['target_topic_count'],navigation=plan['compiler_generated_navigation_pairs']))
    for p in plan['pages']:print(p['topic_id'],'/'.join(p['visible_lines']))
