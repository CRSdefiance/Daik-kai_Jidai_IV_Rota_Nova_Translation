"""Prepare the corrected registered profile using the eight retained exact stage references."""
from pathlib import Path

from scripts.prepare_rafael557_registered_successor_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


RETAINED=Path('work/analysis/Rafael_B201_B220_registered_preparation_v1_20261106')
source=checked_text(previous,{
    """        path = args.out/f'stage_{i}_RESEARCH_REFERENCE.nds'
        target.save(path)""":
        """        path = RETAINED/f'stage_{i}_RESEARCH_REFERENCE.nds'
        assert path.is_file() and path.read_bytes() == bytes(target.rom.save())""",
    'exact_unchanged_eight_final_stage_contracts_andinputs_qualified_by_dependency_reuse=stage_proofs,':
        "exact_unchanged_eight_final_stage_contracts_andinputs_qualified_by_dependency_reuse=stage_proofs,\n"
        "retained_exact_stage_references=str(RETAINED),",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-full-eight-stage-verification-reusing-immutable-references','exec'),globals())

