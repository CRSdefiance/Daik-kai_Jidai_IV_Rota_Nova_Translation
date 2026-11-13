"""Second English editorial pass; retain the earlier draft and its evidence."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

MANUSCRIPT=Path('translations/tavern_schemes_editorial_manuscript_v2.json')
CHANGES={
    940:"You want us to lure a fleet from %s to %s, correct?",
    941:"You'd like us to lure a fleet from %s to %s. Is that correct?",
    942:"So, we're drawing a fleet from %s out to %s?",
    945:"We're luring a fleet from %s to %s. Have I got that right?",
    946:"You want a fleet from %s to come out to %s, right?",
    947:"We'll lure a fleet from %s to %s. Is that correct?",
    950:"So, we're getting %s and %s to fight?",
    954:"You want %s and %s to quarrel with each other?",
}


def main():
    source=Path('translations/tavern_schemes_editorial_manuscript_v1.json')
    doc=read(source)
    for row in doc['records']:
        n=row['message_id']
        if n in CHANGES:
            row['english']=CHANGES[n]+'{PAD}'
            row['localization_note']+=' Second English pass: make the confirmation a direct question about the captain\'s intent. Preserve each voice\'s formality and the complete faction/fleet/destination or faction-conflict facts; the older voice uses a natural check of shared understanding. No authored line breaks or positional spacing.'
            assert row['english'].count('%s')==2
            assert row['review']['source'] and row['review']['context']
            row['review']['formatting']=False
    doc['previous_draft']={'path':str(source),'sha256':sha(source.read_bytes())}
    doc['editorial_revision']='V775 direct confirmations and conversational voice;new layout verification required.'
    doc['producer_sha256']=sha(Path(__file__).read_bytes())
    save(MANUSCRIPT,doc)
    print('Eight confirmation wordings revised;all56 records remain unapproved for formatting/integration.',flush=True)


if __name__=='__main__':main()
