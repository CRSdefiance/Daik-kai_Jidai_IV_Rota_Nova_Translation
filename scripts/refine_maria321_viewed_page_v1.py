"""Keep the observed strength-of-mind phrase intact across the native page turn."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B196_B215_clean_20261110')


def main():
    prior = ROOT/'formatting_v1/page_phrase_preferences_v4.json'
    target = ROOT/'formatting_v1/page_phrase_preferences_v5_viewed.json'
    assert not target.exists()
    prefs = load(prior)
    key = 'DK4_MES_B200_R0015'
    nativepath = ROOT/'native_body_v1'/('complete_'+key+'.json')
    native = load(nativepath)['record']
    oldplan = next(r for r in load(ROOT/'plan_v4/automatic_plans.json')['records'] if r['id'] == key)
    assert native['compiled_hex'] == oldplan['encoded_hex']
    assert oldplan['lines'][3].endswith('the strength') and oldplan['lines'][4].startswith('of mind')
    assert len(native['complete_native_English_display']['pages']) == 2
    entry = prefs['records'][key]
    entry['page_clause'] = 'the strength of mind'
    entry['required_pairs'] += [['strength', 'of'], ['of', 'mind']]
    entry['reason'] = 'The directly viewed B200 page turn separates strength from of mind. Keep the complete noun phrase together, preserving every word, full native width and all original display guards.'
    prefs.update(previous_preferences=str(prior), previous_preferences_sha256=digest(prior),
        direct_viewed_native_finding=str(nativepath), direct_viewed_native_finding_sha256=digest(nativepath),
        no_prose_native_width_font_orengine_changes=True,
        evidence={str(p): digest(p) for p in [prior, nativepath, ROOT/'native_body_v1/B200_part1.png', Path(__file__)]})
    save(target, prefs)
    print('Bound one directly viewed strength-of-mind page finding; fresh plan and native verification pending.')


if __name__ == '__main__':
    main()
