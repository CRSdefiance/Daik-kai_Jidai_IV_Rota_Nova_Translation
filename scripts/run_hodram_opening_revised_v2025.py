"""Ordinary cold boot on the byte-proved research ROM, with recorded inputs."""
from pathlib import Path

SOURCE=Path('scripts/run_hodram_opening_context_v2018.py')

if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    changes={
        'work/analysis/hodram_opening_context_v2018':'work/analysis/hodram_opening_revised_v2025',
        'hodram_opening_context_v2018_V2013':'hodram_opening_revised_v2025_RESEARCH',
        "ROM=Path('out/all_routes_combined_v2013_candidate.nds')":
            "ROM=Path('work/analysis/hodram_opening_relocation_v2023/hodram_opening_V2013_derived_RESEARCH_ONLY.nds')",
        "assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']":
            "assert digest==read('work/analysis/hodram_opening_relocation_v2023/complete_three_block_typed_relocation_research.json')['research_ROM_sha256']",
        "journal.write_text('',encoding='utf-8')":
            "journal.write_text(''.join(line+'\\n' for line in Path('work/analysis/hodram_opening_context_v2018/navigation.jsonl').read_text(encoding='utf-8').splitlines() if json.loads(line).get('until',999999)<=20420),encoding='utf-8')",
    }
    for old,new in changes.items():
        assert old in text,old
        text=text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
