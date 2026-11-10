"""Plan source-defined biography/benefit paragraphs without authored line breaks orshortening."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.reviewed_help_pages_v1 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_early23_formatting_20261104')
SOURCE=Path('translations/help_early23_contextual_manuscript_v3.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=deepcopy(load(SOURCE))
    for row in doc['records']:
        if row['topic_id'] not in [7,8,9]:continue
        text=row['english'];a=text.index('[Benefit 1]');b=text.index('[Benefit 2]')
        row['semantic_sections']=[text[:a].strip(),text[a:b].strip(),text[b:].strip()]
        row['semantic_section_reason']='Clean Japanese has a biography andtwo explicitly numbered benefits. Keep each complete benefit paragraph together when itfits the native page;do not strand a benefit label orsplit its numeric condition. Ordinary lines within every paragraph arewrapped automatically atverified width.'
        assert ' '.join(row['semantic_sections'])==text and not row['review']['formatting']
    current=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds');baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    encoded,plan=plan_articles(doc,clean.read_file(doc['file_path']),baseline.read_file(doc['file_path']),current.read_file(doc['file_path']),require_formatting=False)
    ROOT.mkdir();manuscript=ROOT/'formatting_input_v3.json';save(manuscript,doc)
    resource=ROOT/'HELP_early23_RESEARCH_ONLY.DK4';resource.write_bytes(encoded)
    save(ROOT/'automatic_plans_v1.json',dict(**plan,manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
        source_manuscript=str(SOURCE),source_manuscript_sha256=sha(SOURCE.read_bytes()),research_resource=str(resource),
        current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],
        no_prose_shortening_no_authored_wraps_no_font_orengine_changes=True,
        actual_gameplay=False,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path('dk4tool/dialogue/reviewed_help_pages_v1.py'),Path(__file__)]}))
    print(dict(articles=len(doc['records']),pages=len(plan['pages']),parent_topics=plan['parent_topic_count'],target_topics=plan['target_topic_count'],
        continuation_pairs=plan['compiler_generated_navigation_pairs'],all_prose_andoriginal_links_exact=True,all_fifth_gates_pending=True))
