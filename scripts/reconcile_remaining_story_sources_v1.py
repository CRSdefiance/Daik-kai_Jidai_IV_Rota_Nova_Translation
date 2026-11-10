"""Census exact clean native dialogue/credit bindings for an unfinished storyline scope."""
import argparse
import inspect
from pathlib import Path
from scripts import reconcile_rafael_source_coverage_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

RELEASE=Path('work/hodram_residual_release_v1/registered_release_verification.json')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--route',type=int,choices=[0,2,3],required=True);a=p.parse_args()
    route=a.route;root=Path(f'work/story_source_coverage_20261109_SC{route}_v1')
    source=checked_text(inspect.getsource(previous.main),{
        '== 16748':'== 19161',
        "Path('work').glob('Rafael_*/clean_source_packet.json')":"Path('work').glob('*/clean_source_packet.json')",
        "Path('work/analysis').glob('Rafael_*/clean_source_packet.json')":"Path('work/analysis').glob('*/clean_source_packet.json')",
        "{Path('work/analysis/Rafael_source_coverage_20261106_v1/residual_clean_source_packet.json')}":
            "set(Path('work').glob('*/residual_clean_source_packet.json')) | set(Path('work/analysis').glob('*/residual_clean_source_packet.json'))",
        "f'SC0_B{n}_STYLE_":f"f'SC{route}_B{{n}}_STYLE_",
        "f'SC0_B{n}_CHOICE_":f"f'SC{route}_B{{n}}_CHOICE_",
        "f'SC0 {n}/":f"f'SC{route} {{n}}/",
        'dict(route=0, file_path=ARCHIVE':f'dict(route={route}, file_path=ARCHIVE',
    })
    env={**vars(previous),'ROOT':root,'RELEASE':RELEASE,'ARCHIVE':f'/data/SC{route}.DK4','__file__':__file__}
    exec(compile(source,__file__+f'::unchanged-clean-source-inventory-andexact-credit-binding-SC{route}','exec'),env)
    env['main']()

if __name__=='__main__':main()
