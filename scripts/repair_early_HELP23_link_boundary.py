"""Keep the old continuation's visible word separator in unpositioned proposed prose."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    before=Path('translations/help_early23_contextual_manuscript_v2.json')
    after=Path('translations/help_early23_contextual_manuscript_v3.json');assert not after.exists()
    doc=deepcopy(load(before));row=next(r for r in doc['records'] if r['topic_id']==7)
    assert row['english'].count('usual[[184|Power]]')==1
    row['english']=row['english'].replace('usual[[184|Power]]','usual [[184|Power]]')
    row['ordinary_link_separator_note']='Current202 has the visible separator inside its native link label. Preserve it as an ordinary English word separator between usual andPower;all invisible pair-alignment bytes remain compiler-owned.'
    doc.update(previous_manuscript=str(before),previous_manuscript_sha256=sha(before.read_bytes()),
        one_ordinary_English_word_separator_recovered_from_current_link_label=True,
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(after,doc)
    print('Preserved the usual/Power word boundary in logical prose;no source/current bytes,meaning orcontrol changes.')
