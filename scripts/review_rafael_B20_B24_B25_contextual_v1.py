"""Review three complete residual exchanges against the sealed Japanese-first drafts."""
from collections import Counter
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.seal_rafael_B0_B34_clean_v1 import ROOT, SEALED


CURRENT = ROOT / 'current_v1/current_effective.json'
OUT = Path('translations/rafael_B20_B24_B25_contextual_review_v1.json')
# None means the clean-first draft is adopted. Each retention binds the actual
# current paragraph rather than silently replacing good wording with a variant.
DECISIONS = {
    (20,5): (None, 'Restore the source stammer in the urgent warning; the existing report is clear but loses the sailor\'s startled delivery.'),
    (20,16): ('retain', 'The stammer and repeated-pirate question already convey Claudio\'s alarm naturally.'),
    (20,28): (None, 'Replace the clipped So busy with Julio\'s idiomatic complaint about one interruption after another.'),
    (20,46): ('retain', 'The squeal and Pirates are the worst preserve Cesare\'s exaggerated fear without requiring literal Japanese phrasing.'),
    (20,52): ('retain', 'Green brat and Easy prey are concise, natural pirate taunts that preserve the youth and inexperience insults.'),
    (20,55): ('retain', 'Damn you is a natural angry response to the insult and needs no stronger profanity.'),
    (20,59): (None, 'Restore Rafael\'s personal resolve; true sailors adds a particular qualification and the collective us weakens the character beat.'),
    (20,63): ('retain', 'Everyone! Battle stations! naturally rallies the crew; it is an order, not a claim that the player has assigned positions already.'),
    (20,67): (None, 'Replace the strained fragments been waiting and show my skill while retaining Claudio\'s boastful eagerness.'),
    (20,78): ('retain', 'The existing tutorial accurately warns of enemy numbers and tells the player to send the crew to battle stations. It already reads naturally.'),
    (24,5): (None, 'Replace No luck with Vels\'s idiomatic complaint about his own defeat and bad fortune.'),
    (24,8): ('retain', 'The abrupt name call correctly marks Gerhard\'s recognition before the personal confrontation.'),
    (24,12): ('retain', 'Vels\'s stammered recognition already carries his surprise at facing Gerhard.'),
    (24,16): ('retain', 'The current rebuke naturally links greed to Vels\'s return to piracy and keeps Gerhard\'s stern voice.'),
    (24,19): (None, 'Give Vels a connected, irritable rejection of the lecture and establish Give it a rest for Gerhard\'s immediate echo.'),
    (24,22): (None, 'Echo the wording of Vels\'s preceding dismissal, preserving the exchange\'s escalation in natural speech.'),
    (24,26): ('retain', 'Discipline and thrift? What fun is that? already expresses Vels\'s rejection of Gerhard\'s values in casual English.'),
    (24,30): ('retain', 'The short accusation directly answers Vels\'s reasoning and preserves Gerhard\'s blunt judgment.'),
    (24,34): ('retain', 'The incredulous outburst is complete and correctly positioned before Gerhard\'s unexpected praise.'),
    (24,38): ('retain', 'Seamanship accurately and idiomatically names the skill Gerhard concedes; the existing sentence suits his formal voice.'),
    (24,42): ('retain', 'The current rhetorical question precisely follows the admission that Vels\'s seamanship is superior.'),
    (24,45): (None, 'Replace fouled your heart with idiomatic speech and restore Gerhard\'s point that Vels does not recognize greed\'s effect.'),
    (24,49): (None, 'Replace My heart is foul with a natural echo of Gerhard\'s accusation of corruption.'),
    (24,53): (None, 'Restore when they first met and the comparison of heart with skill or strength; the existing not makes the contrast absolute.'),
    (24,56): (None, 'Restore the purpose of the training rather than claiming it successfully trained Vels\'s heart; connect it to discipline and thrift.'),
    (24,60): (None, 'Keep both the rejection of Gerhard\'s methods and the lion insult, with the concession to his reputation before the attack on his age.'),
    (24,63): (None, 'Restore first-person boasts. The current Take what you want reads as advice rather than Vels\'s account of his own conduct.'),
    (24,66): (None, 'Make Gerhard own his failed attempt to reason with Vels before disowning him; preserve both dismissal and anger.'),
    (24,69): (None, 'Keep Vels\'s angry rejection of the pupil relationship as his claim without erasing the established teacher-pupil history.'),
    (24,73): (None, 'Use a strained vocal reaction rather than adding a spoken curse; this is the turn from public anger to hurt.'),
    (24,77): ('retain', 'Rafael\'s quiet use of Gerhard\'s name lets the emotional change breathe without an invented explanation.'),
    (24,82): (None, 'Remove the invented judgment He deserved death. Gerhard says he meant to kill Vels but could not bring himself to do it.'),
    (24,86): ('retain', 'The existing admission and request for forgiveness preserve the explicit former-pupil relationship and Gerhard\'s lingering attachment.'),
    (24,89): ('retain', 'No, don\'t worry is an idiomatic reassurance and does not blame Gerhard for sparing Vels.'),
    (24,94): (None, 'Restore the full heart-versus-skill comparison and Rafael\'s firm personal agreement; keep the quotation consistent with Gerhard\'s revised line.'),
    (24,99): (None, 'Replace the literal Those words save me with natural English expressing the comfort Gerhard finds in Rafael\'s response.'),
    (25,7): ('retain', 'The simple victory acknowledgment sets up Claudio\'s boast and the contrast with Manuel\'s mourning.'),
    (25,12): ('retain', 'Heh, easy! is a natural short boast; the draft\'s alternative idiom would add no needed meaning.'),
    (25,16): (None, 'Restore the reflective correction from lives lost to returned to Mother Sea, rather than asserting that people physically fell overboard.'),
    (25,20): ('retain', 'Rafael\'s questioning address naturally notices Manuel\'s changed mood without adding dialogue.'),
    (25,25): ('retain', 'Let\'s soothe the souls of the fallen fits Manuel\'s poetic register and accurately introduces his tribute.'),
    (25,28): (None, 'Keep the puzzled reaction while normalizing unintended full-width question marks for this progressive ASCII dialogue; fresh glyph verification remains pending.'),
    (25,33): (None, 'Restore the lapping waves as a familiar sound recalling a mother\'s heartbeat; avoid the current ambiguity about a distant mother.'),
    (25,36): (None, 'Restore the repeated sea-and-mother refrain and reported they say while preserving the source\'s sound-and-writing comparison without naming a language.'),
    (25,40): (None, 'Remove the clumsy bind us in a bond redundancy while preserving lifelong continuity and closing the three-record quotation.'),
    (25,43): (None, 'Restore Rafael\'s offer to compose music himself; May it become a song omits his agency and sounds unnatural.'),
    (25,48): (None, 'Restore Claudio\'s spoken admission about his former impression of Manuel in a complete natural reply addressed to him.'),
    (25,52): (None, 'Preserve Manuel\'s wish that they can be as accepting as the sea; the current should turns the reflective hope into a directive.'),
    (25,55): (None, 'Preserve reflective silence using the batch\'s ASCII ellipsis form; the underlying controls remain untouched and rendering still needs checking.'),
}
SPEAKERS = {0:'Rafael Castor',4:'Janus Pasar',5:'Claudio Manaus',6:'Julio Erneco',
    13:'Cesare Tony',16:'Gerhard Adernkatz',23:'Manuel Almeida',61:'Vels Granat',
    151:'Sailor',176:'Privateers'}


def main():
    assert not OUT.exists()
    current, drafts = map(load, (CURRENT, SEALED/'sealed_drafts.json'))
    sealed = {r['id']:r for r in drafts['records']}
    rows = []
    for group in current['groups']:
        if group['block'] not in (20,24,25):
            continue
        for row in group['records']:
            before = sealed[row['id']]
            assert all(row[k] == before[k] for k in ('source_reference','source_hex','source_meaning','independent_English','context'))
            action, note = DECISIONS[(row['block'],row['source_reference']['record_index'])]
            english = row['current_comparison_paragraph'] if action=='retain' else row['independent_English']
            assert english.isascii() and note and row['source_selector'] in SPEAKERS
            decision = 'retention' if action=='retain' else 'revision'
            assert (english == row['current_comparison_paragraph']) == (decision=='retention')
            rows.append({**row,'english':english,'decision':decision,'finding':note,'localization_note':note,
                'speaker':SPEAKERS[row['source_selector']],
                'review':dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                'current_English_comparison_pending':False,'fresh_formatting_binding_pending':True,
                'registered_release_and_completion_credit_pending':True,'new_credit':0})
    assert len(rows) == len(DECISIONS) == 49
    counts = Counter(r['decision'] for r in rows)
    save(OUT,dict(format='dk4-contextual-editorial-prose-review-v1',translation_policy='natural-dialogue-v2',
        target_locale='en-US',records=rows,records_count=49,complete_blocks=[20,24,25],
        review_gates=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
        counts=dict(counts),remaining_current_comparisons=234,all_final_display_andname_gates_pending=True,
        evidence={str(p):digest(p) for p in (CURRENT,SEALED/'sealed_drafts.json',Path(__file__))},
        new_credit=0,full_goal_complete=False))
    print('Reviewed three complete exchanges:', dict(counts), '; 234 comparisons and fresh display checks remain.')


if __name__ == '__main__':
    main()
