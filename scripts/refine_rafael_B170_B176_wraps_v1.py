"""Guide the formatter around name, tag and phrase splits found in the initial plan."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B170_B176_display_v1 import FORMATTING, PREFERENCES, ROOT
from dk4tool.patch.grand_race_menu_release import sha


OUT = ROOT / 'ordinary_visual_preferences_v2.json'
PHRASES = {
    170: {
        40: ("I can't win with you.",),
        50: ('go to bed early tonight.',),
        53: ('I really do feel a chill.',),
        59: ('Sorry, folks.', 'come back tomorrow, too?'),
        65: ('came to trade, right?',),
        95: ("isn't feeling well.",),
        120: ('Just to be on the safe side.',),
        127: ("hadn't spoken up yesterday...",),
        135: ('thank these travelers.',),
        145: ("You're in a hurry, aren't you?",),
        159: ('a day this good for business?',),
        167: ("Just don't overdo it today.",),
        171: ('maybe tomorrow.', 'these travelers, will you?'),
        174: ('take care of yourselves.',),
        201: ('look out for people.',),
        206: ('talk that price down',),
        232: ("don't have one anymore.",),
        241: ('the sickness', 'wrapped up in work', "I didn't take"),
        244: ('My wife caught it, too...',),
        253: ('ahead of my family',),
        256: ('went out of your way',),
        266: ('happy memories', 'live there alone.'),
        312: ('Glad to be sailing with you.',),
    },
    171: {
        5: ('a lot to drink.',),
        10: ('A man of the sea', "She's doing just fine."),
        22: ('some fire to it.',),
        68: ('I love this tune.',),
        103: ('old man\'s granddaughter.', 'From here on out,'),
    },
    172: {
        11: ('in the middle of the road!',),
        14: ("back home, isn't it?",),
        19: ('See anything you like?', "It's all good stuff!"),
        22: ('travelers, right?',),
        25: ("I'm tired of looking at elephants.", 'How about it?'),
        33: ("at sea, doesn't it?",),
        44: ('good instincts, you know.',),
        62: ("I'm young.", "I'll get the hang of it.", "I've got good instincts."),
        99: ("I pass. How's that?",),
        114: ('nasty, is it?', '(Munch, munch.)'),
        141: ('Samwell da Khan.', 'Glad to meet you!'),
    },
    173: {
        29: ('the departure office, quick!',),
        95: ('the same thing.',),
        99: ('setting sail all by himself...',),
        103: ('ask around town.', 'catch that ship thief!'),
    },
    174: {6: ("hasn't come back.",)},
    175: {6: ("hasn't come back.",)},
    176: {
        13: ('No mistaking it!',),
        18: ('Wide open!',),
        40: ('all lonely and abandoned!',),
        44: ('picked it up.', "That's Jam, J-A-M."),
        47: ('all by yourself, right?',),
        52: ('a little of that...', 'winged it.'),
        60: ('if it sank?',),
        68: ("Where there's a will, there's a way!",),
        86: ("there's a way, huh...",),
        91: ('Life should be big and short!',),
        95: ('a small, long life?',),
        98: ('Turn him over to the guards?',),
        102: ("Let's ask him to join us!",),
        109: ('all by himself!',),
        119: ('What to do...', 'two seconds to think!'),
        131: ('See you!',),
        140: ('hoping for!',),
        148: ('Jam Jack Ludwyan!',),
    },
}


def main():
    assert not OUT.exists()
    doc, prefs = map(load, (FORMATTING, PREFERENCES))
    for row in doc['records']:
        phrases = PHRASES.get(row['block'], {}).get(row['source_record_index'])
        if phrases:
            prefs['records'][row['id']] = dict(line_phrases=phrases,
                reason='Keep the identified phrase, name or short question tag together in the native row.',
                bindings={k: sha(row[k].encode('utf-8')) for k in ('source_hex','current_hex','english')})
    assert len(prefs['records']) == sum(map(len, PHRASES.values()))
    save(OUT, prefs)


if __name__ == '__main__':
    main()
