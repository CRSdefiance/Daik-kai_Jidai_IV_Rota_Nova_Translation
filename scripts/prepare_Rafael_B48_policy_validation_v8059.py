"""Prepare meaningful changed-input policy challenges for all B48 records and FE consumers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
SEMANTIC=[
    ('invented-fixed-addressee',38,'Why are you','Cesare, why are you'),
    ('wrong-regional-artifact',71,'Proof of Conquest','Royal Decree'),
    ('lost-free-passage-condition',144,'free ride','paid voyage'),
    ('invented-captain-decision',159,"Then we'll decide.","You are already our admiral."),
    ('wrong-name-spelling',164,'Hans Letzel','Hans Retzel'),
    ('wrong-occupation',164,'naturalist','navigator'),
    ('invented-kinship',192,'Hans, join us.','Grandpa, join us.'),
    ('invented-gender-reveal',217,'young... man. Ahem.','young woman in disguise.'),
    ('invented-middle-name-in-introduction',221,'Arcadius Eudoxios','Arcadius Eirene Eudoxios'),
    ('lost-navigation-modesty',250,'a little','for many decades'),
    ('invented-family-relationship',324,'an acquaintance','my brother'),
    ('lost-source-question',331,'Interested?','Not interested.'),
    ('lost-hearsay',336,'said to be claimed','guaranteed to be claimed'),
    ('lost-uncertainty',339,'I think we may have a lead','I know exactly'),
    ('wrong-treasure-count',347,'seven treasures','eight treasures'),
    ('wrong-ancient-sages',347,'Seven Sages','Seven Kings'),
    ('lost-reported-prophecy',350,"That's what it says.",'That is certainly true.'),
    ('changed-FI-substitution',370,'{MACRO:FI}','{MACRO:FA}'),
    ('wrong-geography',406,'southern Africa','northern Europe'),
    ('invented-certain-location',414,'The rumor may be false','The rumor is certainly true'),
    ('truncated-joining-name',427,'Letzel','Letze'),
    ('reversed-navigator-restriction',431,"isn't a navigator","is a navigator"),
    ('reversed-Deck-restriction',431,"can't assign","can assign"),
    ('lost-item-information-role',435,'item information','naval ranks'),
    ('wrong-button',438,'Press X','Press Y'),
]
if __name__=='__main__':
    source=Path('scripts/validate_Rafael_B47_policy_v8005.py').read_text(encoding='utf8')
    a=source.index('SEMANTIC=[');b=source.index('\n\nif __name__',a)
    print(derive('scripts/validate_Rafael_B47_policy_v8005.py','scripts/validate_Rafael_B48_policy_v8059.py',{
        source[a:b]:'SEMANTIC='+repr(SEMANTIC),
        'B47':'B48','[47]':'[48]','R0053':'R0347','R53':'R347',
        'Rafael_B47_policy_validation_v8005':'Rafael_B48_policy_validation_v8059',
        'rafael_B47_editorial_manuscript_v3':'rafael_B48_editorial_manuscript_v4',
        'Rafael_B47_relocation_v7989/SC0_block47':'Rafael_B48_relocation_v8041/SC0_block48',
        "row['file_path'],'progressive'":"row['file_path'],'FE-paper' if row['source_selector']==254 else 'progressive'",
        "len(positive)==15":"len(positive)==91",
        "for x in positive)==16":"for x in positive)==92",
        "for x in positive for i in x['qa']['issues'])==6":"for x in positive for i in x['qa']['issues'])==37",
        '15_speech16_page':'91_speech92_page',
        'six_infos':'37_infos','four_native_only_speeches':'thirteen_native_only_speeches',
        '15 exact speech positives/16 pages':'91 exact speech positives/92 pages',
        '6 infos/2 narrow warning':'37 infos/2 narrow warning',
    }))
