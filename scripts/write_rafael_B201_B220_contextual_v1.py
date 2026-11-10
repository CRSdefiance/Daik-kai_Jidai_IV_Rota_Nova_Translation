"""Record the complete contextual decisions and scoped names for Rafael B201–B220."""
from copy import deepcopy
import inspect
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts import write_rafael_B177_B180_contextual_v1 as workflow
from scripts.audit_story_glyph_consistency import load, save
from scripts.seal_rafael_B201_B220_clean_v1 import OUT as SOURCE
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('work/analysis/Rafael_B201_B220_current2549_20261106')
CURRENT = ROOT/'current_effective.json'
OBJECTS = ROOT/'objects/current_objects.json'
IDENTITY = ROOT/'names_and_terms_v1.json'
DRAFTS = SOURCE/'sealed_drafts.json'
DECISIONS = [Path(f'translations/rafael_{label}_contextual_decisions_v1.txt')
             for label in ('B201_B208','B209_B214','B215_B220')]
OUT = Path('translations/rafael_B201_B220_contextual_review_v1.json')
LABELS = Path('translations/rafael_B201_B220_scoped_names_review_v1.json')
BLOCKS = list(range(201,221))
NAMES = {
    0: ('Rafael Castor', 'Keep the established public name and the FI address used by Julio and Claudio.'),
    5: ('Claudio Manaus', 'Keep the established nameplate. Rafael addresses him familiarly as Clau.'),
    6: ('Julio Erneco', 'Keep his established name in the sake aside and his private advice in the bargain.'),
    7: ('Cristina Erneco', 'Keep the approved Cristina spelling in the plate, dialogue and Charm notice.'),
    11: ('Jam Ludwyan', 'Keep the short public plate and the distinct full catalogue and signed Jam Jack Ludwyan.'),
    12: ('Yukihisa Shiraki', 'Keep the short spoken nameplate and the distinct full catalogue with Genjo.'),
    14: ('Emilio Ferog', 'Keep his established name for the exchange about the Minotaur’s Axe.'),
    15: ('Angelo Puccini', 'Keep the established nameplate. Mamma mia and the parrot echo are in dialogue.'),
    18: ('Charles Rochefort', 'Keep his public plate distinct from the full Charles Jean Rochefort form.'),
    19: ('Carlo Sinat', 'Keep the established public name and the shorter given name in his stat notices.'),
    20: ('Fernando Dias', 'Keep the established name for the two private price reactions.'),
    21: ('Ian Dukov', 'Keep his name distinct from the separate seller role and use Ian in the Charm notice.'),
    25: ('Yifa Sol', 'Keep her approved name for the private urge to bargain harder.'),
    75: ('Hans Letzel', 'Keep the established spelling. His familiarity and interest in the book remain in the dialogue.'),
    82: ('Shopkeeper', 'Keep the square shop role for the collector who wants to see the china.'),
    86: ('Shopkeeper', 'Keep the role for the hesitant buyer in the dye discussion, with no invented kinship.'),
    92: ('Barkeep', 'Keep the occupational label for the cheese dish’s cook and seller in the tavern.'),
    103: ('Patron', 'Keep the tavern role for the second diner, distinct from the port worker.'),
    104: ('Trader', 'Keep the source occupation. His private sales talk supplies the unscrupulous characterization.'),
    105: ('Trader', 'Keep the source occupation during the mast-rope bargaining.'),
    113: ('Port Worker', 'Keep the occupational label for the accomplice who suggests approaching the collectors.'),
    115: ('Port Worker', 'Keep the occupational label for the speaker pressing his friend to try tobacco.'),
    117: ('Port Worker', 'Keep the occupation for the second man in the sake exchange.'),
    119: ('Port Worker', 'Keep the same occupation in the Havana rumor and Veracruz food exchange.'),
    124: ('Guard', 'Keep the source role for the castle messenger without adding a rank.'),
    130: ('Daimyo', 'Keep the source title for the Japanese lord. Jam’s letter uses a direct salutation.'),
    140: ('Innkeeper', 'Keep the source occupation when the portrait dispute attracts attention.'),
    145: ('Innkeeper', 'Keep the occupation for the woman who directs Jam to the castle.'),
    147: ('Guildmaster', 'Keep the role when the character discusses china and in the separate chase.'),
    153: ('Sailor', 'Keep the established public sailor label and separate Retainer catalogue for the tobacco exchange.'),
    154: ('Sailor', 'Keep the public sailor label and separate Retainer catalogue during the dye disagreement.'),
    156: ('Sailor', 'Keep the public sailor label and separate Retainer catalogue in the sake exchange.'),
    157: ('Sailor', 'Keep the public sailor label and separate Retainer catalogue for the stranger with the book.'),
    159: ('Sailor', 'Keep the public sailor label and separate Retainer catalogue for the Havana rumor.'),
    166: ('Lady', 'Keep the individual polite-role selector for the diner who asks about the secret and cost.'),
    167: ('Lady', 'Keep the individual polite-role selector for the second diner who offers thanks.'),
    168: ('Lady', 'Keep the individual polite-role selector for the diner who offers to teach her friends.'),
    169: ('Alluring Woman', 'Keep the descriptive public label for the flirtatious seller without disclosing her possible identity.'),
    170: ('Mysterious Old Man', 'Keep the established broad role for the two gift and rumor exchanges.'),
    172: ('Stranger', 'Keep the source-bound public label. Carlo and the person he rescues meet as strangers.'),
    173: ('Shady Man', 'Keep the approved short label for the bargaining and earrings pitches.'),
}
FULL = {11:'Jam Jack Ludwyan',12:'Yukihisa Genjo Shiraki',18:'Charles Jean Rochefort',
        **dict.fromkeys((153,154,156,157,159),'Retainer')}
ECHO = {13:9,20:17,33:29,41:37,65:61}


def digest(path):
    return sha(path.read_bytes())


def read_decisions():
    decisions={}
    for path in DECISIONS:
        block=None
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line or line.startswith('#'):
                continue
            if line.isdigit():
                block=int(line)
                assert block in BLOCKS
                continue
            key,replacement,finding=line.split('|',2)
            assert block is not None and finding.strip()
            if key.startswith('C'):
                offset,index=map(int,key[1:].split('.'))
                lookup=block,'choice',offset,index
            else:
                lookup=block,'speech',int(key)
            assert lookup not in decisions
            decisions[lookup]=replacement.strip(),finding.strip()
    return decisions


def presentation(row):
    if row['kind']!='system-FE':
        return
    block,index=row['block'],row['source_record_index']
    if block in range(201,208):
        role='Commodity-fashion forecast'
    elif block==210:
        role='Namahage voice'
    elif block==216:
        role='Jam Ludwyan’s letter'
    elif block==217 and index in ECHO:
        role='Parrot'
    elif (block,index) in {(211,55),(212,5),(217,5),(217,52)}:
        role='Sound effect'
    else:
        role='Stat notice'
    row.update(speaker=role,source_FE_presentation_kind=role,
        FE_is_not_an_ordinary_actor_nameplate=True,native_FE_presentation_binding_pending=True)
    if (block,index)==(216,74):
        assert row['source_Japanese'].splitlines()[1].lstrip()=='ジャム・ジャック・ルドワイヤン'
        row['source_signature_presentation_pending']=True
        row['source_letter_signature_separate_native_row']=True


def main():
    assert not OUT.exists() and not LABELS.exists()
    drafts,current,objects,identity=map(load,(DRAFTS,CURRENT,OBJECTS,IDENTITY))
    assert identity['runtime']==current['runtime']==objects['runtime']
    assert drafts['complete_blocks']==[g['block'] for g in current['groups']]==BLOCKS
    rows=[r for g in current['groups'] for r in g['records']]
    assert len(rows)==382 and len(objects['choice_records'])==21 and len(objects['choice_objects'])==10
    assert not objects['style_records']
    current_by_id={r['id']:r for r in rows+objects['choice_records']}
    assert len(current_by_id)==len(drafts['records'])==403
    assert set(NAMES)=={r['source_selector'] for r in rows}-{254}
    evidence={str(p):digest(p) for p in (DRAFTS,CURRENT,OBJECTS,IDENTITY,*DECISIONS,Path(workflow.__file__),Path(__file__))}
    labels=[]
    for binding in identity['name_bindings']:
        actor=binding['actor_ID']
        label,reason=NAMES[actor]
        forms={r['consumer']:r for r in binding['current_consumers']}
        assert forms['progressive-nameplate']['text']==label and forms['full-catalogue']['text']==FULL.get(actor,label)
        fields=[f['source'] for f in binding['source_andcurrent_fields']]
        labels.append(dict(id=f'ACTOR{actor}_RAFAEL201_220_NAME',actor_ID=actor,kind='progressive-nameplate',
            english=label,speaker=label,source_meaning=fields[0]['text'],context='Public name or role in Rafael SC0 B201–B220.',
            decision='retention',retention_reason=reason,finding=reason,localization_note=reason,
            source_reference=dict(actor_ID=actor,fields=fields),current_reference=dict(actor_ID=actor,consumer='progressive-nameplate',
                text_hex=forms['progressive-nameplate']['text_hex']),current_consumers=binding['current_consumers'],
            review={g:g!='formatting' for g in workflow.GATES},new_credit=0))
    contexts={int(k):v for k,v in drafts['source_contexts'].items()}
    code=checked_text(inspect.getsource(workflow.review_record),{
        "assert draft['source_word'] == current['source_word'] == 0x2100":
            "assert draft['source_word'] == current['source_word'] and draft['source_word'] in (0x2100,0x2200)",
        "lookup = (block, 'choice', draft['source_index'])":
            "lookup = (block, 'choice', draft['source_command_offset'],draft['source_index'])",
    })
    env={**workflow.review_record.__globals__,'CONTEXTS':contexts}
    exec(compile(code,__file__+'::same-reviewed-record-contract-exact-menu-offsets','exec'),env)
    decisions=read_decisions()
    records=[]
    for draft in drafts['records']:
        row=env['review_record'](draft,current_by_id[draft['id']],{a:v[0] for a,v in NAMES.items()},decisions)
        presentation(row)
        records.append(row)
    assert not decisions
    assert sum(r['kind']=='system-FE' for r in records)==34 and sum(r['kind']=='typed-choice-label' for r in records)==21
    assert sum(r['native_literal_tokens'].count('FI') for r in records)==6
    glyphs=[r['id'] for r in records if r.get('current_unintended_glyphs')]
    assert glyphs==['DK4_MES_B204_R0030','DK4_MES_B206_R0052','DK4_MES_B213_R0031']
    b217={r['source_record_index']:r['english'] for r in records if r['block']==217}
    assert all(b217[echo] in b217[spoken] for echo,spoken in ECHO.items())
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=workflow.GATES,file_path='/data/SC0.DK4',blocks=BLOCKS,records=records,
        source_objects=403,ordinary_speech_objects=382,typed_choice_objects=21,typed_choice_commands=10,
        **{k:current[k] for k in ('current_ROM','current_ROM_sha256','current_archive_sha256','runtime')},
        proposed_revisions=sum(r['decision']=='revision' for r in records),justified_retentions=sum(r['decision']=='retention' for r in records),
        current_glyph_defect_records=glyphs,punctuation_consistency_revisions=['DK4_MES_B205_R0021','DK4_MES_B214_R0025','DK4_MES_B215_R0035'],
        all_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,new_credit=0,evidence=evidence)
    projected=deepcopy(doc)
    projected['translation_policy']='natural-dialogue-v1'
    validate_natural_dialogue_batch(projected)
    save(LABELS,dict(format='dk4-scoped-name-contextual-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=workflow.GATES,records=labels,runtime=current['runtime'],
        all_name_formatting_gates_pending=True,no_global_name_table_changes=True,new_credit=0,evidence=evidence))
    doc['evidence'][str(LABELS)]=digest(LABELS)
    save(OUT,doc)
    print(f"{len(records)} contextual decisions, {doc['proposed_revisions']} revisions, {doc['justified_retentions']} retentions, 41 scoped labels.")


if __name__=='__main__':
    main()
