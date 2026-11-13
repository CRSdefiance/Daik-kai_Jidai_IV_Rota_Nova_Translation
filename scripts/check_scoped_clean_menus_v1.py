"""Apply the qualified complete two/three-choice checks to an explicit Maria batch."""
import argparse
import inspect
from pathlib import Path
from scripts import check_maria390_menus_v1 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--expected-menus',type=int,required=True);ap.add_argument('--expected-captions',type=int,required=True)
    args=ap.parse_args();doc=load(args.root/'formatting_v1/formatting_input.json')
    assert doc['runtime']['captain']==3 and doc['file_path']=='/data/SC3.DK4'
    groups={}
    for row in doc['records']:
        if row['kind']=='typed-choice-label':groups.setdefault((row['block'],row['source_command_offset']),[]).append(row)
    counts=[len(v) for v in groups.values()]
    assert len(counts)==args.expected_menus and sum(counts)==args.expected_captions and set(counts)<={2,3}
    bridges=sum(18 if c==2 else 24 for c in counts);negatives=sum(7 if c==2 else 8 for c in counts)
    source=checked_text(inspect.getsource(previous.main),{
        'assert len(groups)==8 and sum(map(len,groups.values()))==17':
            f'assert len(groups)=={len(counts)} and sum(map(len,groups.values()))=={sum(counts)}',
        'menus=8,captions=17,native_provider_alignments=48,bridged_modal_returns=150,':
            f'menus={len(counts)},captions={sum(counts)},native_provider_alignments={6*len(counts)},bridged_modal_returns={bridges},',
        'current_andtarget_normal_highlight_planes=68,target_normal_highlight_planes=34,':
            f'current_andtarget_normal_highlight_planes={4*sum(counts)},target_normal_highlight_planes={2*sum(counts)},',
        'compiler_negatives=57,':f'compiler_negatives={negatives},',
        'PASS8 menus/17 captions/48 alignments/150 bridged returns/68 planes;direct review andactual controller pending.':
            f'PASS{len(counts)} menus/{sum(counts)} captions/{6*len(counts)} alignments/{bridges} bridged returns/{4*sum(counts)} planes;direct review andactual controller pending.',
    })
    env={**vars(previous),'ROOT':args.root,'__file__':__file__}
    exec(compile(source,__file__+'::same-native-choice-provider-indices-pixels-canaries-and-rejection-contract','exec'),env)
    env['main']()


if __name__=='__main__':main()
