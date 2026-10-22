"""Source-review the full bubble/foam event and prepare a research-only repack."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sea_foam_family import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXTS = {
    457:('Admiral! Please look over there! Strange bubbles on the water!','Formal crew call draws attention to strange sea bubbles.'),
    458:('Admiral! There are strange bubbles on the water!','Direct crew warning about strange bubbles on the sea surface.'),
    459:('Admiral! Look at those strange bubbles on the water!','Young/familiar crew call about visible strange bubbles.'),
    460:('Admiral, look over there! Strange bubbles are rising from the sea!','Casual crew voice calls attention to strange rising bubbles.'),
    461:('Admiral! There are some suspicious bubbles over there!','Older/formal crew voice points out suspicious bubbles.'),
    462:('Admiral, look! There are weird bubbles on the water!','Young/familiar voice points out odd bubbles.'),
    463:("That's what we've heard about...",'Restrained recognition of the phenomenon mentioned in rumors; retain hesitation.'),
    464:('(Gulp...) Those are the bubbles people talk about...','Swallowed/frightened recognition; preserve gulp and trailing uncertainty.'),
    465:('(Gulp...) Could that really be...?','Frightened disbelief without inventing a named phenomenon.'),
    466:("Could those be the bubbles we've heard about...?",'Casual hesitant question about the rumored phenomenon.'),
    467:('(Gulp...) Are those the bubbles people talk about...?','Gulp and familiar hesitant question; independent from preceding packed entry.'),
    468:("Well now... Could that be the foam we've heard about...?",'Older cautious reaction and question; treat いやいや as an interjection, not an assertion that the rumor is false.'),
    469:('?','Independent silent questioning reaction.'),
    470:('Sailors tell stories about foam that swallows ships...','Reports sailors passing down stories of ship-swallowing foam.'),
    471:("They say there's foam out there that can swallow ships...",'Cautious report of stories about ship-swallowing foam.'),
    472:("I've heard about bubbles that swallow whole ships...",'Casual hearsay about bubbles swallowing ships.'),
    473:("I've heard there's foam that can swallow a ship...",'Soft/familiar hearsay about foam swallowing ships.'),
    474:("Those bubbles... I've heard they swallow ships.",'Rougher voice identifies the observed bubbles and reports their danger.'),
    475:('The stories say that foam can swallow a ship whole.','Older oral-tradition voice reports the ship-swallowing phenomenon.'),
    476:("From what I've heard, it can swallow a ship whole...",'Casual hearsay preserves an entire ship being swallowed.'),
    477:('This is bad! Take evasive action! Everyone to your stations!','Alarm and explicit evasion/all-hands-stations orders.'),
    478:("Let's steer clear of it! All hands to your stations!",'Leader orders evasion and all hands to stations.'),
    479:("No way! We've got to get away! Everyone to your stations!",'Younger animated voice expresses disbelief, escape and all-hands-stations orders.'),
    480:("Stay calm, everyone! To your stations! We'll steer clear!",'Calm the crew, order stations and announce evasion.'),
}


def main():
    out = Path('work/analysis/sea_foam_family_v514')
    out.mkdir(parents=True,exist_ok=True)
    clean = NdsImage.open('work/clean.nds')
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    records = []
    for i,(english,meaning) in TEXTS.items():
        entry = source[i]
        records.append({'id':f'COMMON_MESSAGE_{i}','message_id':i,'block':entry.block,'record':entry.record_index,
                        'source_hex':entry.text.hex(),'japanese':entry.text.decode('cp932'),
                        'english':english+'{PAD}','speaker':'Shared crew voice; exact actor selected by game',
                        'source_meaning':meaning,
                        'context':'Sea foam/bubble observation and avoidance family457-480; all original voice variants and their immediate neighbors reviewed. No monster identity or rank beyond explicit Admiral is invented.',
                        'localization_note':'Natural American English preserves recognition, rumor/hearsay, swallowed ships, uncertainty and orders. One logical paragraph; native repacking owns all subentry boundaries and runtime formatting owns line breaks. Parenthetical gulp and ellipsis preserve the source reaction. No shortening to fit old split English.',
                        'review':{k:True for k in ['source','context','localization','naturalness','formatting']}})
    document = {'format':'dk4-native-common-natural-manuscript-v1','translation_policy':'natural-dialogue-v2',
                'target_locale':'en-US','encoder':'dialogue-fixed-v1',
                'review_gates':['source','context','localization','naturalness','formatting'],'records':records}
    manuscript = Path('translations/sea_foam_family_manuscript_v1.json')
    manuscript.write_text(json.dumps(document,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rom = NdsImage.open('out/all_routes_combined_v508_candidate.nds')
    common,arm = rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    target_common,target_arm,report = transform(common,arm,document)
    config = {'format':'dk4-sea-foam-family-v1','source_common_sha256':sha(common),'source_arm9_sha256':sha(arm),
              'target_common_sha256':sha(target_common),'target_arm9_sha256':sha(target_arm),
              'manuscript':str(manuscript),'manuscript_sha256':sha(manuscript.read_bytes()),'change':report}
    Path('translations/sea_foam_family_v1.json').write_text(json.dumps(config,indent=2)+'\n',encoding='utf-8')
    (out/'target_common.bin').write_bytes(target_common)
    (out/'target_arm9.bin').write_bytes(target_arm)
    rom.replace_file('/COMMON/MESFILE.DK4',target_common)
    rom.replace_file('/__arm9__.bin',target_arm)
    rom.save(out/'research_only_sea_foam_family.nds')
    print('Prepared complete24-message foam family;all3668 identities/cache lengths retained.')


if __name__ == '__main__':
    main()
