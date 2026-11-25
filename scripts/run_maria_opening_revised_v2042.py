"""Same ordinary Maria inputs and existing system-unlock save on the research ROM."""
from pathlib import Path
SOURCE=Path('scripts/run_maria_opening_context_v2035.py')
if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'work/analysis/maria_opening_context_v2035':'work/analysis/maria_opening_revised_v2042',
        'maria_opening_context_v2035_V2030':'maria_opening_revised_v2042_RESEARCH',
        "ROM=Path('out/all_routes_combined_v2030_candidate.nds')":"ROM=Path('work/analysis/maria_opening_relocation_v2040/maria_opening_V2030_derived_RESEARCH_ONLY.nds')",
        "assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']":"assert digest==read('work/analysis/maria_opening_relocation_v2040/complete_B33_CS0101_typed_relocation_research.json')['research_ROM_sha256']",
        "journal.write_text('',encoding='utf-8')":"journal.write_text('{\"stop\":true}\\n',encoding='utf-8')",
    }
    for old,new in changes.items():assert old in text,old;text=text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
