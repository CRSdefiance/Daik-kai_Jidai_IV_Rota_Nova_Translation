"""Trial full-width page continuity without changing a word,source control orQA rule."""
from copy import deepcopy
from hashlib import sha256
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    out = ROOT/'formatting_FE_v1/preferences_continuity_v1.json'
    assert not out.exists()
    doc_path = ROOT/'formatting_FE_v1/physical_manuscript.json'
    doc = load(doc_path)
    rows = {r['id']:r for r in doc['records']}
    before = ROOT/'formatting_FE_v1/preferences.json'
    preferences = deepcopy(load(before))
    rules = {
        'DK4_MES_B73_R0020':dict(one_page=True,required_pairs=[['how','mysterious']],reason='Trial one complete bee/amber reflection in the validated width,without leaving How mysterious alone after A.'),
        'DK4_MES_B74_R0043':dict(one_page=True,required_pairs=[['old',"man's"],["man's",'feelings']],reason='Trial a full panel that keeps Julio\'s old man\'s feelings phrase intact.'),
        'DK4_MES_B88_R0204':dict(one_page=True,required_pairs=[['uses','like'],['like','these']],reason='Trial the full gunpowder reveal without stranding uses like these after A.'),
        'DK4_MES_B89_R0030':dict(one_page=True,required_pairs=[['entrust','it'],['it','to'],['to','you']],reason='Trial the full lamp tradition andgift offer without isolating it to you after A.'),
        'DK4_MES_B94_R0073':dict(one_page=True,required_pairs=[['your','lives']],reason='Trial the complete journey warning without stranding the final life-risk phrase after A.'),
        'DK4_MES_B74_R0060':dict(required_pairs=[['around','there']],reason='A second panel is necessary for the full uncertain two-sea legend;keep around there together at the page boundary.'),
        'DK4_MES_B76_R0038':dict(required_pairs=[['hear','anything']],reason='A second panel is necessary for the full cooking joke andrumor offer;keep hear anything together across pagination.'),
        'DK4_MES_B77_R0012':dict(required_pairs=[['uneven','surface']],reason='A second panel is necessary for the full reported telescope claim;keep uneven surface together across pagination.'),
    }
    for ident, rule in rules.items():
        row = rows[ident]
        assert row['kind'] == 'progressive'
        rule['bindings'] = {k:sha256(row[k].encode()).hexdigest() for k in ['source_hex','current_hex','english']}
        preferences['records'][ident] = rule
    preferences.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),
        source_manuscript=str(doc_path),source_manuscript_sha256=digest(doc_path),
        unchanged_native_widths_andunmodified_QA=True,no_prose_shortening_orauthored_breaks=True,new_credit=0)
    save(out,preferences)
    print('Saved eight full-width continuity trials;every word andall native/QA guards preserved.')


if __name__ == '__main__':
    main()
