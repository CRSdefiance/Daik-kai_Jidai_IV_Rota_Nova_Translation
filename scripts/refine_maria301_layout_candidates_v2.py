"""Keep better original predicates andtest whether five weak page endings can fit one page."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/Maria_B0_B32_clean_20261109/formatting_v1')


def main():
    out=ROOT/'preferences_v4_onepage_trials.json'
    assert not out.exists()
    preferences=deepcopy(load(ROOT/'preferences_v3_candidates.json'))
    rows=preferences['records']
    for key in ['DK4_MES_B0_R0039','DK4_MES_B0_R0048']:
        rows.pop(key)
    additions={
        'DK4_MES_B19_R0040':[["you're",'going']],
        'DK4_MES_B19_R0202':[['everything','he'],['he','did']],
        'DK4_MES_B19_R0217':[['to','remember'],['remember','my'],['my','father'],['father','by']],
        'DK4_MES_B21_R0014':[["don't",'look']],
        'DK4_MES_B29_R0134':[["what's",'that']],
        'DK4_MES_B31_R0042':[["kuhn's",'disguised'],['disguised','fleet']],
    }
    for key,value in additions.items():rows[key]['required_pairs'].extend(value)
    rows['DK4_MES_B21_R0026']['ordinary_boundaries']=[['but','next']]
    for row in rows.values():
        if 'page_clause' not in row:continue
        row.pop('page_clause');row['one_page']=True
        row['reason']+=' Trial the same prose on four physical rows before choosing a two-page boundary.'
    save(out,preferences)
    print('Saved35 scoped preference trials;no prose orsource changes. Predicate originals retained;five page counts tested.')


if __name__=='__main__':main()
