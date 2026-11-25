"""Save the complete retirement/farewell exchange before prior English exposure."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B151_B170_clean_20261102')
MEANINGS = [
    'Respectfully addresses {MACRO:FA}; His Majesty the King is waiting.',
    'The king praises {MACRO:FA} for the achievement, declaring that the country’s prosperity is now assured.',
    'Appoints him supreme commander of the navy and expects the national navy to develop further and distinguish itself.',
    'An impressed aside or exclamation.',
    'An aside saying that no appointment could suit the admiral better.',
    'Repeats the appointment, supreme commander, reflectively.',
    'The king also offers whatever further reward he wishes and asks what he wants.',
    'A silent pause before replying.',
    'Formally asks permission to state his wish.',
    'The king grants permission and tells him to speak without reserve.',
    'Begins to make the request.',
    'Formally expresses deep gratitude for the appointment as supreme commander, but trails into a reservation.',
    'The king reacts questioningly.',
    'Another observer reacts questioningly.',
    'If such a selfish request can be forgiven, he wishes to retire from the navy.',
    'The king reacts in astonishment.',
    'An astonished aside.',
    'A stammered, astonished aside asking what was said.',
    'The king demands an explanation.',
    'Says this is something he has considered for some time.',
    'The king pauses silently.',
    'He was fortunate to have excellent subordinates and, however imperfectly, accomplished the great undertaking of building the strongest navy.',
    'Formally credits the king’s kindness in employing someone of his limited ability and gives heartfelt thanks, then introduces a further objection.',
    'Says he lacks the talent to sustain that achievement, discipline the many future recruits and make the royal navy endure.',
    'The king counters that merely having him at the navy’s head frightens other countries and inspires the troops.',
    'Respectfully disagrees: that is precisely what worries him most.',
    'The king asks what he means.',
    'Presumptuously warns that needlessly alarming enemies will eventually isolate the country, while pride in being the world’s strongest will cause a grave future mistake.',
    'Argues that his absence will instead lower foreign countries’ guard and give the nation’s officers and troops a necessary sense of danger.',
    'The king gives a thoughtful or reluctant murmur.',
    'Wants nothing else; begs the king’s mercy in permitting this personal wish.',
    'The king pauses before deciding.',
    'Reluctantly accepts: it is deeply regrettable, but there is little choice if this is his earnest wish.',
    'Formally thanks the king for granting it.',
    'A silent observer’s reaction.',
    'A subdued aside addressing the admiral.',
    'Gerhard is silent.',
    'Sera asks {MACRO:FI} whether he will not come to her country.',
    'He says it seems he is the sort of person who can live only at sea.',
    'Although it may sound cold, he believes her people must rebuild their homeland by their own efforts.',
    'She hesitantly insists that she wants {MACRO:FI} to come.',
    'He tells Sera that he is no legendary king.',
    'She says that does not matter and struggles to express what she wants or feels.',
    'A silent pause.',
    'He explicitly contrasts her being a princess with his now being merely a retired serviceman; their stations are too far apart.',
    'A silent pause in the farewell.',
    'Tells her not to look like that; this need not be an eternal parting.',
    'The source explicitly labels Sera as she asks whether they can meet again.',
    'The source explicitly labels {MACRO:FI}; he answers that of course they can.',
    'A pause explicitly under Sera’s source heading.',
    'Under the {MACRO:FI} heading, he assures her it is true: he is now free to go where he wishes.',
    'Under the {MACRO:FI} heading, he promises to visit from time to time to see her country coming back to life.',
    'Under Sera’s source heading, she quietly agrees.',
    'Asks シルウド to take care of Sera.',
    'The reply is halting: he can be relied on to do so.',
    'Realizes Sera has taught him to speak this way and looks forward to the next meeting.',
    'Sera calls {MACRO:FI} emotionally.',
    'Another silent pause.',
    'She asks him to be sure to come.',
    'He promises that he will.',
    'A silent pause.',
    'He addresses Sera softly.',
    'Acknowledges it will be difficult for her and wishes her well.',
    'She nods.',
    'Promises another meeting and says farewell.',
    'Afterward, wonders where he should go.',
    'Gerhard calls out that they can set sail whenever the admiral wishes.',
    'He is surprised to see Gerhard.',
    'Gerhard asks for orders.',
    'He demands to know what Gerhard is doing.',
    'Gerhard blandly explains that he has procured the admiral’s new ship and arranged all supplies and departure preparations.',
    'That is not what he meant: he had responsible posts arranged for every one of his subordinates.',
    'Gerhard says Charles is now director of the Royal Academy’s research institute and was delighted at unlimited access to research equipment.',
    'Tries to interrupt: he is not talking about Charles.',
    'Gerhard continues that Manuel is chairman of the maritime technology committee and was studying new ship designs with an unusually grave expression.',
    'Forcefully clarifies that Gerhard himself was entrusted with the grave responsibilities of supreme commander of the navy.',
    'Gerhard quietly declines, saying it is not his calling and asking to be excused.',
    'Rebukes him: the choice accounted for all his ability, experience and the confidence others place in him.',
    'Gerhard says it is unfair to burden someone else with such responsibilities while the admiral alone enjoys an easy retirement.',
    'A momentary, discomfited hesitation.',
    'Gerhard says the country’s own people should be responsible for national defense; an outsider such as himself should not interfere.',
    'Besides, without the admiral he has no reason to remain in this country; he will accompany him anywhere.',
    'A silent reaction.',
    'Dryly remarks that it looks as though this will be a voyage without much romance or feminine company.',
    'Gerhard laughs and boasts that wherever two such fine men go, the ladies will never leave them alone.',
    'A dry, fondly exasperated aside about Gerhard’s blithe optimism or self-satisfaction.',
]


def main():
    path = ROOT / 'B156_86_clean_meanings_before_English.json'
    assert not path.exists()
    packet_path = ROOT / 'clean_source_packet.json'
    packet = load(packet_path)
    group = next(g for g in packet['groups'] if g['block'] == 156)
    assert len(group['records']) == len(MEANINGS) == 86
    rows = []
    for i, (source, meaning) in enumerate(zip(group['records'], MEANINGS, strict=True)):
        context = ('Royal audience: surprise appointment, deliberate refusal, strategic explanation and reluctant permission to retire.' if i < 37 else
                   'Farewell: Sera pleads for his company; he distinguishes a legendary king from himself and explicitly acknowledges her princess status. Promises of future visits soften the separation; source headings/left-right staging identify cinematic turns.' if i < 65 else
                   'Departure coda: Gerhard evades the retirement question with news of the others’ posts, refuses his own appointment and insists on accompanying him. Their closing flirtation joke restores familiar warmth after the farewell.')
        rows.append(dict(id=source['id'], file_path=source['file_path'], block=156,
            source_reference=source['source_reference'], source_hex=source['source_hex'], source_Japanese=source['source_Japanese'],
            source_selector=source['source_selector'], source_complete_preamble_hex=source['source_complete_preamble_hex'],
            source_0100_ancestors=source['source_0100_ancestors'], source_macros=source['source_macros'],
            source_meaning=meaning, exchange_context=context, earlier_English_unconsulted=True,
            native_speaker_item_terms_localization_andformatting_pending=True, new_credit=0))
    save(path, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()), records=rows,
        source_meanings=86, complete_exchange=156, not_final_localized_English_orfive_gate_approval=True,
        source_fidelity_notes=[
            'The king explicitly grants a supreme naval command;the retirement and later assignment to Gerhard are actual source facts,not invented promotions.',
            'Sera’s princess status is explicit here. Do not preempt the reveal in earlier exchanges or invent a marriage,engagement orroyal genealogy.',
            'Gerhard describes himself as an outsider;do not replace that with an unsupported nationality.',
            'Cinematic FE bodies contain leading empty rows,full-width staging spaces andexplicit Sera/FI headings. Their actual consumer/geometry andspeaker continuity need source-qualified display review before formatting;do not automatically reuse the ordinary FE layout or treat spatial staging as encoding damage.',
            'The final joke is playful confidence about women/romance,followed by a dry aside;do not flatten it into a generic dull voyage or invent hostility.'],
        earlier_English_unconsulted=True, new_credit=0, producer_sha256=sha(Path(__file__).read_bytes())))
    print('Saved86 clean-first meanings for the complete retirement/farewell;128 ordinary meanings now saved;no prior English,drafts orcredit.')


if __name__ == '__main__':
    main()
