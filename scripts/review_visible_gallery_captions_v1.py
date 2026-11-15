"""Contextual reread of all 164 visible Gallery event captions."""

from collections import Counter
from hashlib import sha256
from pathlib import Path

from dk4tool.patch.gallery_caption_bounds import validate
from scripts import register_visible_online_captions_v1 as parent
from scripts.inventory_common_scene_caption_duplicates import captions


base = parent.base
ROOT = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
OUTPUT = ROOT / 'visible_gallery_captions_context_v1.json'
HISTORICAL = Path('work/analysis/gallery_caption_v523/all_carousels_proof.json')
PRIOR = Path('translations/scene_caption_manuscript_v2.json')
CAPTAINS = ('Rafael', 'Hodram', 'Lil', 'Maria')

# Each position gets its own source or scene rationale. The carousel order is the
# native one; the retained historical image receipts provide the original art.
NOTES = (
    (
        'Keeps the first numbered port-town view without inventing a port.',
        'Clau is the shorter form in this source, while the later Arcadius series spells out Claudio.',
        'The dockyard picture supports the shorthand description of repairs.',
        'Preserves the side profile and the original large-art variant.',
        'Names the proprietor and keeps the shop type open.',
        'Keeps the nickname Raffy in the Japanese title and names Lil plainly.',
        'The ordinary room label fits the neutral, borrowed term in Japanese.',
        'Keeps the identity reveal and first numbered view.',
        'Matches the first identity caption and keeps the second index.',
        'Bustling conveys the crowd and activity around the bullring.',
        'The entrance is the event, and Matador preserves the specific role.',
        'The plain, spoken phrasing matches the brief injury caption.',
        'Sickroom describes the room rather than implying a hospital.',
        'Followers preserves Uddin’s group and the first frame number.',
        'Keeps the same group wording as the previous frame and retains the second index.',
        'Moonlit binds the instrument to the night scene and preserves Rafael and the variant number.',
        'The preceding violin scene supplies the instrument, and Up Close preserves the camera framing.',
        'Names Sera, her listening, and the matching close-up.',
        'Dejected conveys Raffy’s mood without specifying why Irene is with him.',
        'Names Charlotte’s entrance directly.',
        'Keeps the close-up distinct from the preceding entrance.',
        'Names the wilderness and the historical region used by the game.',
        'House preserves the place and the character without implying who else lives there.',
        'Offers captures her gesture with the flowers.',
        'The source uses Clau and depicts him with children without naming their relationship.',
        'Keeps Maria and the source nickname Raffy, as well as the number.',
        'Remains on Guard conveys the martial readiness implied by zanshin.',
        'This portrait title is the character’s established name.',
        'Docked describes the pictured ship at the dock without specifying a dry dock.',
        'The neutral pairing preserves both names without implying a relationship.',
        'Bustling describes the activity in the village scene.',
        'Names the flower crown and the fact that Charlotte is wearing it.',
        'The two figures and the torchlight are the focus, with their identities left open.',
        'Audience with the King conveys the formal meeting and its rank.',
        'The Japanese spells out Claudio here and identifies the first Arcadius frame.',
        'Full names and the second index match the surrounding series.',
        'Full names and the third index match the surrounding series.',
        'Companions retains the group and the Raffy nickname.',
        'In a Panic keeps the hurried reaction and preserves the Clau nickname.',
        'Keeps the character nickname and the first ending variant.',
        'Names both characters and their shared ending.',
        'Keeps the second ending variant in the same style as the first.',
        'Keeps the source nickname with Charlotte and leaves their relationship unstated.',
        'The title is about Clau’s happiness and retains his source nickname.',
        'Later On conveys the epilogue without specifying Janus’s fate.',
        'In Conversation describes the two figures’ exchange in a natural gallery title.',
    ),
    (
        'The exclamation and large-art marker retain the urgency and original variant.',
        'Names Hodram’s entrance in the series.',
        'The picture shows activity on deck. Bustle on Board describes the scene without specifying a kind of ship.',
        'Rises from His Seat preserves the deliberate action.',
        'Addresses His Crew conveys a formal exhortation in the shipboard context.',
        'The two names are presented as a pair without assigning a relationship.',
        'In Battle keeps Angelo’s participation and the compact action title.',
        'Loses is direct and conveys the informal defeat wording alongside the preceding fight.',
        'Keeps the fleet’s arrival as the event without naming an allegiance.',
        'Captive and Princess both come from the source title.',
        'Reaches Out keeps the visible gesture without naming its object.',
        'Wounded preserves that Hodram has been injured without suggesting how.',
        'Leaves the knife’s purpose open and names Sera.',
        'The two figures are left behind, with no relationship added.',
        'The simple possessive conveys the visible smile.',
        'Uses the same title for the same moonlit violin image in Rafael’s carousel.',
        'Keeps the listening close-up aligned with the identical Rafael-route caption.',
        'The sequence shows Hodram arriving for Sera. The title keeps both people and that purpose.',
        'Beloved preserves the affectionate description of the named ship Elysion.',
        'Versus preserves the direct confrontation with Escante.',
        'Homeland conveys Sera’s place of origin without asserting a political boundary.',
        'Keeps the approved Camille and Hodram spellings.',
        'Names both characters without adding a relationship.',
        'Making Up captures the reconciliation in idiomatic English.',
        'Ironclad is the established name for the armored ship.',
        'The picture shows Hayreddin wounded and Hodram standing beside him. The new order makes the injury’s subject clear.',
        'The source connects Sera with the rescue. The short possessive leaves the precise roles open.',
        'Reunite clearly describes the pair meeting again.',
        'Audience preserves the original formality and the king’s rank.',
        'Keeps the direction of the farewell and the first image in the series.',
        'Keeps the second farewell image and its shared wording.',
        'Keeps the third farewell image and its shared wording.',
        'Keeps the fourth farewell image and its shared wording.',
        'Keeps the fifth farewell image and its shared wording.',
        'Names Hodram and Gerhard without adding an action.',
        'The possessive naturally describes the expression.',
        'Sails Away conveys the original departure.',
        'Gazes at the Stars retains the reflective action.',
        'Matches Hodram’s stargazing title for the paired image.',
        'Preserves both Sera’s posture and position outside the window.',
        'The source calls it a portrait of the pair without naming them.',
    ),
    (
        'The deck image contrasts tired Camille and lively Lil. The revised adjectives carry the contrast and preserve both names.',
        'Keeps Lil looking back toward town from the ship’s deck.',
        'Sets Off is a natural title for the departure.',
        'Names Clifford’s entrance without adding a role.',
        'Keeps the dress and original large-art marker.',
        'Retains both names and leaves the relationship unspecified.',
        'Feast conveys the spread without specifying an occasion.',
        'Matches the identical pairing in Hodram’s carousel.',
        'The picture shows Lil actively throwing her arms around Camille.',
        'At a Loss conveys Ian’s uncertainty without adding an explanation.',
        'Misfortune conveys the source’s adversity without specifying its cause.',
        'The close-up presents Ian with elegance. The new caption expresses that admiring tone naturally.',
        'Names Lil and Samwell with the established spelling.',
        'Keeps the interior and the owner of the mansion.',
        'Matches the same Camille and Hodram pairing in Hodram’s carousel.',
        'Keeps Lil as the subject of the attack and leaves the assailant unspecified.',
        'Welcome Back preserves the source’s direct greeting.',
        'Keeps the locket and its family association without specifying who carries it.',
        'Keeps Jam’s exuberant “Yahoo!” and the first picture number.',
        'Matches the first Jam caption and retains the second picture number.',
        'Craze conveys the tomato’s sudden broad popularity.',
        'Story leaves open which events Julian recounts.',
        'Specifies that Clifford takes a hostage without naming the hostage.',
        'Keeps the burning ship and the large-art marker.',
        'Directly names Clifford’s death, as the source does.',
        'Keeps the sunset behind the figures without naming them.',
        'Bashful conveys Lil’s shy, fidgeting demeanor without adding a motive.',
        'Gazes describes Lil’s look toward Camille without interpreting her feelings.',
        'The Kiss is the conventional title for this event.',
        'Embrace keeps the mutual action without assigning identities or motives.',
        'Keeps Lil and the specific wedding dress without asserting ceremony details.',
        'Facing each other is the pictured position.',
        'The plain location title is faithful and already natural.',
        'Preserves the profusion of blooming tulips and the large-art marker.',
        'Keeps the two people and their shared action at the church doors.',
        'Names Lil and the rain without adding emotion.',
        'Raises Her Head conveys the change in posture.',
        'Keeps the house’s association with Camille and leaves other occupants open.',
        'First Meeting is the natural title for their encounter, with the approved name Camille.',
    ),
    (
        'Preserves the act of hearing a report and the large-art marker.',
        'Keeps Maria’s close-up distinct from the preceding wider scene.',
        'Names Ian and Maria without adding a relationship.',
        'Keeps both the flowers and birds and Maria’s conversation with them.',
        'Keeps the indoor room and the Chinese mansion setting.',
        'Names Yifa’s entrance without assigning a role.',
        'Taoist Magic preserves the tradition signaled by the Japanese and suits the illustrated action.',
        'Resolve expresses Maria’s determination.',
        'Keeps Carlo’s still posture and the grave without naming the deceased.',
        'Names both characters with the established spellings.',
        'Fleet Battle preserves the scale of the action at sea.',
        'In Profile clearly describes Maria’s framing.',
        'The source uses the short name Al here and shows his departure from the tavern.',
        'Names Aziza’s entrance directly.',
        'Breaks Out carries the sudden onset of the rebellion.',
        'The art shows three fighters coming to aid the others. Join the Fight conveys the help without implying a formal alliance.',
        'Encounter keeps Rafael and the original encounter without adding a first meeting.',
        'Keeps Janus and the ship without assigning ownership.',
        'Portrait identifies the artwork as a depiction of Rocco.',
        'This portrait title is the character’s name.',
        'The two names are kept with their current established spellings.',
        'Mansion conveys the residence and its association with Gerhard.',
        'Factory is the original place and Charles is its established owner name.',
        'Poor Mivor conveys the caption’s pity in an idiomatic title for the dejected figure.',
        'Dance names Cristina’s action. This is the same dancer as the next close-up.',
        'Uses the same Cristina spelling as the preceding dance title.',
        'Drowning identifies the child’s immediate danger.',
        'Keeps Cristina’s action of holding a child without inferring a family relationship.',
        'The encouragement and exclamation preserve the source’s direct appeal to Mivor.',
        'Good Match conveys the illustrated pair’s compatibility without adding a marriage or other relationship.',
        'Names Maria and Hodram without changing the source order.',
        'Keeps Richard’s action and the single rose.',
        'Final Moments conveys the approaching death without adding its cause.',
        'Retainers conveys the subordinate attendants gathered around Maria in the Japanese.',
        'Relaxed Smile conveys the unguarded expression.',
        'Grand Review retains the named event. Party includes the people with Maria and fits the original caption view.',
        'This portrait title is the character’s approved name.',
        'Portrait is a natural title for the illustrated depiction of Maria.',
    ),
)
REVISIONS = {
    (0, 15): ('Rafael and a Moonlit Violin 2', 'Rafael and a violin under the moon, second image.'),
    (0, 28): ('A Docked Ship', 'A ship at a dock.'),
    (0, 45): ('The Two in Conversation', 'Two people talking together.'),
    (1, 2): ('Bustle on Board', 'A busy, hurried scene aboard the ship.'),
    (1, 7): ('Angelo Loses', 'Angelo has lost the fight. The wording is informal.'),
    (1, 15): ('Rafael and a Moonlit Violin 2', 'Rafael and a violin under the moon, second image.'),
    (1, 25): ('Hodram with Injured Hayreddin', 'Hayreddin is injured, and Hodram is with him.'),
    (2, 0): ('Worn-Out Camille and Spirited Lil', 'Camille is worn out, and Lil is full of energy.'),
    (2, 11): ('The Elegant Ian', 'An admiring depiction of the beautiful Ian.'),
    (3, 15): ('Three Join the Fight', 'Three people arrive to aid the others in a fight.'),
    (3, 23): ('Poor Mivor', 'Mivor is in a pitiable state.'),
    (3, 33): ('Maria and the Assembled Retainers', 'Maria with her subordinates lined up around her.'),
    (3, 37): ('Portrait of Maria', 'An illustrated depiction of Maria.'),
}


def main():
    assert not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(parent.CLEAN) == release['clean_input_sha256']
    clean, arm = [base.NdsImage.open(path).read_file(parent.ARM) for path in (parent.CLEAN, parent.ROM)]
    source = {(r['route_index'], r['index']): r for r in captions(clean)}
    previous = {(r['route_index'], r['index']): r for r in base.load(PRIOR)['records']}
    history = base.load(HISTORICAL)
    assert base.digest(history['report']) == history['report_sha256']
    images = {(r['route'], case['position']): case for r in history['all164_original_Gallery_positions_and_four_wraps']
              for case in r['cases']}
    assert len(source) == len(previous) == len(images) == 164
    assert tuple(map(len, NOTES)) == (46, 41, 39, 38)
    records = []
    for current in validate(arm):
        route, pos = key = current['route'], current['position']
        original, older, scene = source[key], previous[key], images[key]
        assert original['source_hex'] == older['source_hex'] and original['pointer_field'] == current['field']
        assert scene['caption']['Japanese'] == original['japanese'] and scene['all49152_native_screen_pixels_exact']
        stored = current['English']
        english, gloss = REVISIONS.get(key, (stored, older['source_meaning']))
        assert (english != stored) == (key in REVISIONS)
        size = len(english.encode('ascii'))
        left = 128 - size * 5 // 2
        assert 32 <= left and left + 5 * size + 1 <= 224
        records.append(dict(id=older['id'], file_path=parent.ARM, route=route, position=pos,
            source_Japanese=original['japanese'], source_meaning=gloss,
            source_reference=dict(offset=original['offset'], original_hex=original['source_hex']),
            current_reference=dict(field=current['field'], pointer=current['pointer'],
                                   stored_hex=(stored.encode('ascii') + b'\0').hex()),
            current_English=stored, english=english, decision='revision' if key in REVISIONS else 'retention',
            context=f'{CAPTAINS[route]}’s Gallery event carousel, image {pos + 1}.',
            speaker='Gallery event caption', localization_note=NOTES[route][pos],
            original_substitution_count=0, output_bounds=[left, left + 5 * size + 1],
            original_scene_image=scene['source'], earlier_scene_capture=scene['image'],
            matching_COMMON_keys=older['matching_common_ids'],
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    assert Counter(row['decision'] for row in records) == {'revision': 13, 'retention': 151}
    base.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        records=records, current_ROM_sha256=release['candidate_sha256'],
        current_ARM9_sha256=sha256(arm).hexdigest(), clean_ROM_sha256=release['clean_input_sha256'],
        historical_scene_evidence={str(p): base.digest(p) for p in (HISTORICAL, PRIOR)},
        new_dialogue_credit=0, formatting_pending=True, registered=False))
    print('Reviewed all 164 visible Gallery captions: 13 proposed revisions and 151 justified retentions.')


if __name__ == '__main__':
    main()
