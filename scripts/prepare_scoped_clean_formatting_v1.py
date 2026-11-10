"""Prepare fresh mixed-object layouts while reusing exact compatible macro proofs."""
import argparse
from pathlib import Path
from scripts import prepare_maria330_formatting_v1 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['root','prose','prior-macros']:ap.add_argument('--'+key,type=Path,required=True)
    args=ap.parse_args();doc=load(args.prose);objects=load(args.root/'current_objects_v1/current_objects.json')
    assert doc['all_individual_four_prose_gates_pass'] and doc['all_fifth_formatting_gates_pending']
    rows=doc['records'];total=len(rows);progressive=sum(r['kind']=='progressive' for r in rows)
    fe=sum(r['kind']=='system-FE' for r in rows);choices=sum(r['kind']=='typed-choice-label' for r in rows)
    styles=sum(r.get('native_object_kind')=='4100-style-alternative' for r in rows)
    macros=sum(sum(r['source_macros'].values()) for r in rows)
    assert styles==len(objects['style_records']) and choices==len(objects['choice_records'])
    source=checked_text(previous.source,{
        'from scripts.meaning_maria330_clean_v1 import ROOT':f'ROOT=Path({str(args.root)!r})',
        "Path('translations/maria_B96_B124_contextual_review_v2.json')":f'Path({str(args.prose)!r})',
        "Path('work/Maria_B73_B95_clean_20261109/formatting_v1/native_macro_measurements.json')":f'Path({str(args.prior_macros)!r})',
        "len(rows) == 330 and sum(r['kind']=='progressive' for r in rows) == 320":f"len(rows) == {total} and sum(r['kind']=='progressive' for r in rows) == {progressive}",
        "sum(r['kind']=='system-FE' for r in rows) == 8 and sum(r['kind']=='typed-choice-label' for r in rows) == 2 and tokens == 23":
            f"sum(r['kind']=='system-FE' for r in rows) == {fe} and sum(r['kind']=='typed-choice-label' for r in rows) == {choices} and tokens == {macros}",
        "'physical_speech_objects':328,'ordinary_speech_objects':293,'style_physical_speech_objects':35,'style_command_objects':6":
            f"'physical_speech_objects':{total-choices},'ordinary_speech_objects':{total-choices-styles},'style_physical_speech_objects':{styles},'style_command_objects':{len(objects['style_objects'])}",
        "'typed_choice_objects':2,'typed_choice_commands':1":f"'typed_choice_objects':{choices},'typed_choice_commands':{len(objects['choice_objects'])}",
        'Prepared328 bodies/two captions/23 FI-FA-FO tokens':f'Prepared{total-choices} bodies/{choices} captions/{macros} macro tokens',
    })
    exec(compile(source,__file__+'::same-current-dependency-controls-default-expansions-andfresh-input-contract','exec'),
        {'__file__':__file__,'__name__':'__main__'})


if __name__=='__main__':main()
