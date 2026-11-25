"""Preserve first drafts and seal source-reread improvements before current-English comparison."""
from copy import deepcopy
from pathlib import Path
import re
from collections import Counter
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B37_B50_clean_20261109')
SOURCE = ROOT/'all286_clean_meanings_andindependent_drafts_v1.json'
OUT = ROOT/'all286_clean_meanings_andindependent_drafts_v2.json'
REFINEMENTS = {
    (45,53):("Watch your mouth! We're the Espinosa Company! Our name alone scares people stiff! Get lost if you want to live!",
        'Localize the crying-child-silencing fear idiom by its threatening effect; avoid an unnatural literal boast about a child.'),
    (46,28):("The Western powers each have their own share of the world outside Europe. When one stumbles, another simply takes his place.",
        'The source distributes regions among powers; each does not individually control the whole non-European world. Keep the replacement argument as Clifford’s claim.'),
    (47,53):("You cheated my father out of his home and farmland! Now he and the rest of the family have vanished!",
        'Use natural distressed speech in place of household. The source explicitly supplies father and family, unlike unsupported kinship elsewhere; no deaths are invented.'),
    (47,185):("They know you fight for them, Admiral. Your concern for them has come through. Please, wave back to them.",
        'Express the emotion-reaching-people image naturally while retaining Ian’s polite alternative reassurance and request.'),
    (48,21):("She weakens her enemies with schemes and diplomacy, then wipes them all out the moment they let their guard down. Cross her, and you won't live to regret it.",
        'The multiple-lives idiom expresses extreme danger. Localize its effect in Clau’s rumor, rather than implying an actual extra-lives mechanic.'),
    (48,162):("I just want to see goods traded fairly from one region to another. Both buyers and sellers could gain a great deal.",
        'Replace the awkward goods-flow-fairly phrasing with Rafael’s clear ideal of fair exchange and mutual benefit, preserving the source’s substantial gain.'),
    (48,239):("Since their alliance with the Turks ended, their main forces seem to have withdrawn east. You don't see them around here anymore.",
        'Keep the inferred withdrawal and the complete reported absence distinct; hardly see weakened the latter. The shorter alternative remains separate.'),
    (49,167):("If I'm going to steal, I'd rather steal from a villain. I want to see my men's happy faces and that bastard Escante kicking himself.",
        'Use a natural English regret idiom for ほぞをかむ. Keep both the crew’s pleasure and Escante’s frustration without literal anatomy or a selfless-pirate rewrite.'),
    (50,43):("Had you been content to keep the wokou pirates in check in the Far East, England might have taken you on as a useful subordinate one day...",
        'Make the meaning of wokou clear in English while retaining the regional suppression, unrealized possibility and subordinate status. No nationality generalization is added.'),
    (50,57):("Spending time with a beautiful admiral like you was quite a pleasure.",
        'Preserve the farewell’s beauty remark and mocking pleasure without the possessive my, which could suggest unsupported intimacy.'),
}


def main():
    assert not OUT.exists()
    doc = deepcopy(load(SOURCE))
    assert doc['current_English_unconsulted'] and len(doc['records']) == 286
    rows = {(r['block'],r['source_record_index']):r for r in doc['records']}
    changes = []
    for key,(draft,reason) in REFINEMENTS.items():
        row = rows[key];previous = row['independent_English_draft']
        assert draft != previous
        row['independent_English_draft'] = draft
        row['source_reread_draft_refinement'] = reason
        changes.append(dict(id=row['id'],source_reference=row['source_reference'],source_Japanese=row['source_Japanese'],
            previous_draft=previous,refined_draft=draft,reason=reason))
    for row in doc['records']:
        text = row['independent_English_draft']
        assert text.isascii() and text == text.strip() and not any(x in text for x in ['\n','\r','\t','{LB','{ALIGN','{PAD'])
        assert dict(Counter(re.findall(r'F[A-Z]',text))) == row['source_macros']
        assert not any(row['review'].values()) and row['current_English_unconsulted']
    doc.update(previous_drafts=str(SOURCE),previous_drafts_sha256=digest(SOURCE),
        source_reread_refinements=changes,original_drafts_preserved=True,
        no_current_English_comparison_orreview_credit=True)
    doc['evidence'][str(Path(__file__))] = digest(Path(__file__))
    save(OUT,doc)
    print('Sealed10 source-reread draft improvements;all286 bindings and21 substitutions exact;current dialogue still unconsulted.')


if __name__ == '__main__':main()
