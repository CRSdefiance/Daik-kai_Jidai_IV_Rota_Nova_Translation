"""Prepare the clean-source Square rumor revisions with the original portrait formatter."""

from inspect import getsource
from pathlib import Path

from scripts import register_square_country_briefings_20261115 as parent
from scripts import stage_square_country_briefings_20261115 as template
from scripts.prepare_regional_rumors_v749 import MEANINGS
from scripts.source_locked_derivation_v5118 import checked_text


base = parent.base
ARM, COMMON, CLEAN, GATES = template.ARM, template.COMMON, template.CLEAN, template.GATES
ROOT = Path('work/square_rumors_20261115_v3')
ROM = ROOT / 'Square_Rumors_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/square_rumors_context_20261115_v3.json')
NUMBERS = range(709, 730)
MEANING = MEANINGS | {
    718: 'Admiral Hayreddin inherited his name from a man he regarded as his father. The Ottomans made that earlier man Sultan of Algiers.',
}
PROSE = {
    709: "Clifford used to be a pirate. Now he's a naval admiral, and I hear the Queen's made him a knight.",
    712: "They say Sweden's new naval fleet makes a point of paying its own way through trade and privateering.",
    713: "They say Admiral Albuquerque's ancestor made his name long ago, commanding Portuguese fleets in the Indian Ocean.",
    716: 'Athens still has plenty of goods to trade at a profit.',
    719: "Silveira's far richer than we are. And what a penny-pincher!",
    720: "Espinosa's crimes are countless. We all look the other way. Who knows what he'd do if we crossed him...",
    724: "Kuhn will do anything for profit. Oh, keep that between us, please...",
    725: "They say an empress would ruin China. I don't buy it. If only that female admiral who routs Japanese pirates ruled here...",
    726: "Hideyoshi or Kurushima? I'll drive them off every time they come!",
    729: "Governor Escante's set to become viceroy of Mexico and Peru, I hear.",
}
EXPECTED = {
    712: ("They say Sweden's new naval fleet", 'makes a point of paying its own way', 'through trade and privateering.'),
    724: ('Kuhn will do anything for profit.', 'Oh, keep that between us, please...'),
    729: ("Governor Escante's set to become", 'viceroy of Mexico and Peru, I hear.'),
}
NOTES = {
    709: 'Keep the former pirate, current rank and royal honor. The speaker repeats news of the honor without assigning a reason to the Queen.',
    710: 'Keep the speaker’s surprise that young women now go to sea to trade. The closing expression gives that reaction its own beat.',
    711: 'Retain the speaker’s respect for Speyer’s effort and the softer wish that he face the League’s decline.',
    712: 'Paying its own way expresses the fleet’s stated policy. Keep both sources of funds and use privateering for authorized raiding.',
    713: 'Made his name is more natural in conversation than distinguished himself. Keep the hearsay, ancestor, Portuguese fleets and Indian Ocean.',
    714: 'Keep Valdes’s rank, the fleet’s strength and the in-world epithet Invincible Armada.',
    715: 'Keep the company’s name, past reach and the vivid claim that it behaved as though it owned the Mediterranean.',
    716: 'Describe the profitable goods in terms the shopkeeper would use. Still preserves the longstanding trade advantage.',
    717: 'Keep control of the eastern Mediterranean as a clear, direct statement.',
    718: 'Keep the established Hayreddin spelling and the distinction between the current admiral and the earlier sultan. The father wording leaves the exact non-birth relationship open.',
    719: 'Penny-pincher carries the speaker’s indignation after the pointed comparison with local people’s means.',
    720: 'Keep the crimes, the community’s silence and fear of what Espinosa might do in retaliation. The pause leaves the threat unspecified.',
    721: 'Keep the speaker’s emphatic confidence. More than hold his own preserves the claim that Uddin can meet or surpass the European powers, and They say keeps the royal background as hearsay.',
    722: 'Keep the image of Nagalpur sitting back while the money rolls in, followed by the speaker’s frank envy.',
    723: 'Keep the contrast between Pereira’s loyalty to his country and ruthlessness toward people outside his circle.',
    724: 'Keep the blunt accusation about profit, then let the shopkeeper make a softer request for discretion.',
    725: 'Let the speaker reject the saying in their own voice and wish the admiral who drives off the pirates were in power. Keep her identity implicit.',
    726: 'Keep the two opponents and the speaker’s promise to repel them every time. Use a short question to set up the defiant reply.',
    727: 'Keep the reported defeat and the reason Kurushima became obsessed with ironclads. The speaker gives no technical explanation.',
    728: 'Keep gold and anything that glitters as the shopkeeper’s vivid description of Maldonado’s weakness.',
    729: 'Put the expected appointment in everyday speech, mark it as hearsay, and keep Mexico and Peru in the same phrase.',
}
SOURCE_RANGES = ((0x5F9B8, 0x5FB54), (0xB4A88, 0xB4AD4), (0xB51B4, 0xB51CC), (0xB5690, 0xB56A8))


def main():
    source = getsource(template.main).replace('def main():', 'def stage_review():', 1)
    lo = source.index('    guarded_wrap = ')
    hi = source.index('    assert all(body !=', lo)
    source = source[:lo] + "    edited = {n: compile_paragraph(text) for n, text in PROSE.items()}\n" + source[hi:]
    lo = source.index('        context = (')
    hi = source.index('        records.append', lo)
    source = source[:lo] + (
        "        context = ('An independent local rumor selected by the original Square shopkeeper after the town share check. '\n"
        "                   'The current company has no market share. The original selector adds the town region to 709.')\n"
    ) + source[hi:]
    source = checked_text(source, {
        '    business = selectors(arm)\n    assert len(business) == 13 and business == selectors(clean_arm)\n': '',
        'original_shop_condition_selectors=business, records=records': 'records=records',
    })
    scope = vars(template) | globals()
    exec(compile(source, __file__ + '::stage-reviewed-portrait', 'exec'), scope)
    scope['stage_review']()


if __name__ == '__main__':
    main()
