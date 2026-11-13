"""Keep the laugh/question/realization beats coherent before Escante’s second-page contrast."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/Maria_B0_B32_clean_20261109/formatting_v1')


def main():
    out=ROOT/'preferences_v6.json';assert not out.exists()
    doc=deepcopy(load(ROOT/'preferences_v5.json'))
    row=doc['records']['DK4_MES_B4_R0009']
    row['required_pairs'].extend([['what','has'],['has','maldonado']])
    row['reason']+=(
        ' The explicit source laugh may occupy a short opening row; keep the complete question opener andtelling-you phrase, then the complete realization. The alternative put a bare What at a short row end.')
    doc['records']['DK4_MES_B18_R0036']['reason']+=(
        ' The explicit poem permits shorter verse-like statement pairs on the first page, followed by the complete remembered-heartbeat simile; no ordinary authored line breaks are inserted.')
    doc['records']['DK4_MES_B30_R0020']['reason']+=(
        ' The first page carries the complete explanatory sentence, keeping Ming government andisolation-policy terms together; the second carries his complete boast. This is preferable to a detached than-I-expected fragment.')
    save(out,doc)
    print('Refined one remaining first-page question layout;documented two source-supported long-page choices;no prose changes.')


if __name__=='__main__':main()
