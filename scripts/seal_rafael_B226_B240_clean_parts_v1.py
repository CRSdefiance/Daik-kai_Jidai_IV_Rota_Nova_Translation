"""Bind clean-first prose to the original speech, style and caption references."""
import argparse
from pathlib import Path
import re

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


ROOT = Path('work/analysis/Rafael_B221_B240_clean_20261106')
PACKET = ROOT / 'clean_source_packet.json'
STYLES = ROOT / 'clean_style_objects.json'
CHOICES = ROOT / 'clean_choice_objects.json'


def clean_keys(row):
    if row.get('kind') == 'typed-choice-label':
        return f"C{row['source_command_offset']}.{row['source_index']}"
    if row.get('kind') == 'actor-style-alternative':
        _, command, offset = row['id'].rsplit('_', 2)
        return f'V{command}.{offset}'
    return str(row['source_reference']['record_index'])


def read_prose(path):
    contexts, drafts = {}, {}
    block = None
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        if line.startswith('@'):
            number, context = line[1:].split('|', 1)
            block = int(number)
            assert block not in contexts and context.strip()
            contexts[block] = context.strip()
            continue
        label, meaning, draft = (field.strip() for field in line.split('|', 2))
        assert block is not None and (block,label) not in drafts and meaning and draft
        drafts[block,label] = meaning,draft
    return contexts,drafts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prose', type=Path, required=True)
    parser.add_argument('--first', type=int, required=True)
    parser.add_argument('--last', type=int, required=True)
    parser.add_argument('--expected', type=int, required=True)
    args=parser.parse_args()
    contexts,drafts=read_prose(args.prose)
    blocks=list(range(args.first,args.last+1))
    assert list(contexts)==blocks
    out=ROOT/f'B{args.first}_B{args.last}_clean_drafts_v1.json'
    assert not out.exists()
    packet,styles,choices=map(load,(PACKET,STYLES,CHOICES))
    rows=[row for g in packet['groups'] for row in g['records']]+styles['records']+choices['records']
    selected=sorted((row for row in rows if row['block'] in contexts),
        key=lambda row:(row['block'],row['source_reference']['offset']))
    assert len(selected)==len(drafts)==args.expected
    records=[]
    for original in selected:
        block=original['block']
        meaning,draft=drafts.pop((block,clean_keys(original)))
        assert original['earlier_English_unconsulted']
        is_style=original.get('kind')=='actor-style-alternative'
        is_caption=original.get('kind')=='typed-choice-label'
        raw=bytes.fromhex(original['source_hex'])
        if not (is_style or is_caption):
            assert raw[0]==original['source_selector']
            raw=raw[1:]
        macros=re.findall(rb'F[A-Z]',raw)
        assert [m.decode() for m in macros]==re.findall(r'\bF[AIOTU]\b',draft),original['id']
        assert not any(t in draft for t in ('{LB','{ALIGN','{PAD}'))
        records.append({**original,'source_meaning':meaning,'independent_English':draft,'context':contexts[block],
            'speaker':('Player choice' if is_caption else 'Runtime-selected crew voice' if is_style else
                       f"Native source selector {original['source_selector']}"),
            'review':dict(source=False,context=False,localization=False,naturalness=False,formatting=False),
            'current_English_comparison_pending':True,'approved_names_terms_titles_andruntime_substitutions_pending':True,
            'native_literal_token_counts':{m.decode():macros.count(m) for m in set(macros)},'new_credit':0})
    assert not drafts
    n_styles=sum(row.get('kind')=='actor-style-alternative' for row in records)
    n_captions=sum(row.get('kind')=='typed-choice-label' for row in records)
    evidence={str(p):sha(p.read_bytes()) for p in (PACKET,STYLES,CHOICES,args.prose,Path(__file__))}
    save(out,dict(records=records,records_count=len(records),ordinary_speeches=len(records)-n_styles-n_captions,
        typed_captions=n_captions,physical_style_alternatives=n_styles,complete_blocks=blocks,source_contexts=contexts,
        all_five_gates_pending=True,no_current_English_extracted_for_this_intake_before_drafts=True,
        all_source_literal_F_tokens_preserved=True,no_blanket_claim_of_historical_unexposure=True,
        no_ROM_or_registry_changes=True,new_credit=0,guide_photos=False,evidence=evidence))
    print(f'Sealed {len(records)} clean drafts across B{args.first}–B{args.last}, including {n_styles} styles and {n_captions} captions.')


if __name__=='__main__':
    main()

