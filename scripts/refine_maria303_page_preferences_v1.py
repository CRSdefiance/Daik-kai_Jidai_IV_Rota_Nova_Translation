"""Trial ordinary complete-word soft wraps while preserving both reviewed paragraphs verbatim."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    path=ROOT/'formatting_v3/preferences_page_continuity_v1.json';assert not path.exists()
    doc_path=ROOT/'formatting_v3/formatting_input_complete_indices_v1.json'
    doc=load(doc_path);rows={r['id']:r for r in doc['records']}
    initial=ROOT/'formatting_v3/initial_preferences.json';pref=deepcopy(load(initial))
    rules={
        'DK4_MES_B61_R0023':dict(one_page=True,ordinary_boundaries=[['with','something'],['get','those']],
            reason='Trial ordinary adjacent-row complete-word preposition/object and verb/object boundaries. Preserve the entire neighborhood/science/almost-daily-blasts paragraph rather than leaving every day alone after A. No authored break, width change or prose shortening.'),
        'DK4_MES_B70_R0034':dict(one_page=True,ordinary_boundaries=[['mortal','risk']],
            reason='Trial the ordinary adjacent-row adjective/noun boundary mortal/risk within one complete panel, preserving every word and Yukihisa\'s formal explanation rather than stranding of extraordinary skill after A. No source meaning, native control or glyph exemption.'),
    }
    for ident,rule in rules.items():
        row=rows[ident];assert row['kind']=='progressive'
        rule['bindings']={k:digest_bytes(row[k].encode()) for k in ['source_hex','current_hex','english']}
        pref['records'][ident]=rule
    pref.update(previous_preferences=str(initial),previous_preferences_sha256=digest(initial),
        source_manuscript=str(doc_path),source_manuscript_sha256=digest(doc_path),
        ordinary_soft_wrap_policy='docs/editorial_localization_and_layout_standard.md',
        no_QA_waivers_no_authored_breaks_no_prose_changes=True,new_credit=0)
    save(path,pref)
    print('Saved two source-bound ordinary soft-wrap trials; reviewed prose, widths and native checks unchanged.')

def digest_bytes(raw):
    from hashlib import sha256
    return sha256(raw).hexdigest()

if __name__=='__main__':main()
