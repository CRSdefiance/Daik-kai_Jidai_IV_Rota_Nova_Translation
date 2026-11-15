"""Keep useful phrase/page repairs and retain better full-width original layouts."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B196_B215_clean_20261110')


def main():
    prior = ROOT/'formatting_v1/page_phrase_preferences_v2.json'
    target = ROOT/'formatting_v1/page_phrase_preferences_v3.json'
    assert not target.exists()
    prefs = load(prior)
    entries = prefs['records']
    retained = []
    for key, reason in {
        'DK4_MES_B197_R0025': 'Retain the ordinary Medusa/Shield soft wrap: forcing the whole item name adds an unnecessary page. The complete installed name and all prose remain intact.',
        'DK4_MES_B198_R0043': 'Retain the ordinary Charles/Martel soft wrap. Joining the name creates a weaker of/Charles boundary; the full historical identity remains clear.',
        'DK4_MES_B202_R0019': 'Retain the original Giant/Tortoise Shield soft wrap. Joining the whole title creates sparse shell and called rows with no reduction in page count.',
        'DK4_MES_B211_R0061': 'Retain the ordinary Jutland/Peninsula soft wrap. Joining the whole place name makes a sparse opening row.',
        'DK4_MES_B215_R0158': 'Retain the original worked/out soft wrap. Enforcing the phrasal verb adds a third row and makes the complete blessing less readable.',
    }.items():
        entries[key]['required_pairs'] = []
        entries[key]['reason'] = reason
        entries[key]['justified_original_layout_retention'] = True
        retained.append(dict(id=key, reason=reason))
    for key, reason in {
        'DK4_MES_B200_R0015': 'Do not force the entire closing explanation onto one page: it creates a sparse hesitation row and seven rows overall. Keep move in together and inspect the resulting ordinary page boundary.',
        'DK4_MES_B206_R0039': 'Retain the original page boundary before do look for it, a complete imperative. Forcing the preceding conditional onto the same page creates a sparse used to build row and an extra row.',
        'DK4_MES_B209_R0045': 'Keep come in handy together rather than forcing the whole closing question onto a page and creating sparse preceding rows.',
        'DK4_MES_B212_R0109': 'Keep jade or crystal together rather than forcing the whole prices clause onto a page and creating sparse preceding rows.',
    }.items():
        del entries[key]['page_clause']
        entries[key]['reason'] += ' ' + reason
        retained.append(dict(id=key, reason=reason))
    entries['DK4_MES_B209_R0045']['required_pairs'] = [['come', 'in'], ['in', 'handy']]
    entries['DK4_MES_B212_R0109']['required_pairs'] = [['jade', 'or'], ['or', 'crystal']]
    entries['DK4_MES_B208_R0043']['required_pairs'].append(['spanish', 'navy'])
    prefs.update(previous_preferences=str(prior), previous_preferences_sha256=digest(prior),
        contextual_layout_retentions=retained,
        no_prose_native_width_font_orengine_changes=True,
        evidence={str(p): digest(p) for p in [prior, ROOT/'plan_v2/automatic_plans.json', ROOT/'plan_v2/diagnostics.json', Path(__file__)]})
    save(target, prefs)
    print('Retained five better original phrase layouts, relaxed four overconstrained page clauses and refined two closing phrases; fresh plan pending.')


if __name__ == '__main__':
    main()
