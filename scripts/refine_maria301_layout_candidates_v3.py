"""Keep a genuine one-page result andrestore two-page clauses where four rows fail orwarn."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/Maria_B0_B32_clean_20261109/formatting_v1')


def main():
    out=ROOT/'preferences_v5.json';assert not out.exists()
    preferences=deepcopy(load(ROOT/'preferences_v4_onepage_trials.json'))
    first=load(ROOT/'preferences_v3_candidates.json')['records']
    for key in ['DK4_MES_B4_R0009','DK4_MES_B8_R0005','DK4_MES_B18_R0036','DK4_MES_B30_R0020']:
        preferences['records'][key]=deepcopy(first[key])
    preferences['records']['DK4_MES_B4_R0009']['required_pairs']=[['telling','you'],['i','certainly'],['certainly','miscalculated']]
    preferences['records']['DK4_MES_B30_R0020']['required_pairs']=[['ming','government'],['of','isolation']]
    preferences['records']['DK4_MES_B24_R0011']['reason']=(
        'The unchanged127-character paragraph fits four physical rows; keep the full taunt andHavana destination on one page rather than an isolated second-page destination. Native verification remains required.')
    preferences['records']['DK4_MES_B29_R0134']['reason']+=(
        ' A short opening line is justified by the explicit source shriek; the complete indignant question follows intact.')
    save(out,preferences)
    print('Saved35 scoped preferences:one page reclaimed,three impossible four-row trials restored,two better predicate originals retained;no warnings waived.')


if __name__=='__main__':main()
