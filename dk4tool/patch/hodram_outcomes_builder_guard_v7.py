"""Permit preserved builders or one additive B51 stage after compatible outcomesv7/B49v4/B50v2,with full original inverse."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v6 import BUILDER,STAGE_V6,STAGE_B49_V3,STAGE_B50,validate_builder_bytes as previous_validate
from scripts.source_locked_derivation_v5118 import checked_text

STAGE_V7=checked_text('if True:\n'+STAGE_V6,{'hodram_outcomes_editorial_v6':'hodram_outcomes_editorial_v7'}).split('\n',1)[1]
STAGE_B49_V4=checked_text('if True:\n'+STAGE_B49_V3,{'hodram_B49_editorial_v3':'hodram_B49_editorial_v4'}).split('\n',1)[1]
STAGE_B50_V2=checked_text('if True:\n'+STAGE_B50,{'hodram_B50_editorial_v1':'hodram_B50_editorial_v2'}).split('\n',1)[1]
STAGE_B51="    hodram_B51_editorial_config = profile_config.get('hodram_B51_editorial')\n    if hodram_B51_editorial_config:\n        from dk4tool.patch.hodram_B51_editorial_v1 import apply_release as apply_hodram_B51_editorial\n\n        hodram_B51_editorial_report = apply_hodram_B51_editorial(candidate, baseline, hodram_B51_editorial_config)\n        for hodram_B51_file in hodram_B51_editorial_report['files']:\n            hodram_B51_path = hodram_B51_file['file_path']\n            grouped.setdefault(hodram_B51_path, [])\n            changed_records.setdefault(hodram_B51_path, []).extend(row['id'] for row in hodram_B51_file['changed_records'])\n            relocation_checks.setdefault(hodram_B51_path, {})['hodram_B51_editorial'] = {\n                'release_config': hodram_B51_editorial_config,\n                'release_config_sha256': sha256(Path(hodram_B51_editorial_config).read_bytes()),\n                'proof': hodram_B51_editorial_report}\n        for hodram_B51_manuscript in hodram_B51_editorial_report['manuscripts']:\n            more_batch = Path(hodram_B51_manuscript)\n            if more_batch in release_batches:\n                raise ValueError('Hodram B51 stage must run once after the complete V8543 stack')\n            release_batches.append(more_batch)\n\n"

def validate_builder_bytes(raw,digest):
    if not isinstance(raw,bytes):raise ValueError('Hodram builder guard: complete builder bytes required')
    predecessor,prior,B50,addition=STAGE_V7.encode(),STAGE_B49_V4.encode(),STAGE_B50_V2.encode(),STAGE_B51.encode()
    present=any(stage in raw for stage in [predecessor,prior,B50,addition]);normalized=raw
    if present:
        if any(raw.count(stage)!=1 for stage in [predecessor,prior,B50]) or raw.count(addition)>1:
            raise ValueError('Hodram builder guard: complete compatible outcomesv7/B49v4/B50v2 stages once required')
        if any(stage.encode() in raw for stage in [STAGE_V6,STAGE_B49_V3,STAGE_B50]):
            raise ValueError('Hodram builder guard: mixed owned versions forbidden')
        boundary=b'    # Lexically valid "% o"'
        if raw.count(boundary)!=1 or not raw.index(predecessor)<raw.index(prior)<raw.index(B50)<raw.index(boundary):
            raise ValueError('Hodram builder guard: original predecessor order before final percent safety required')
        if addition in raw:
            if not raw.index(B50)+len(B50)<=raw.index(addition)<raw.index(boundary):
                raise ValueError('Hodram builder guard: B51 must follow complete B50 before final percent safety')
            normalized=normalized.replace(addition,b'',1)
        normalized=normalized.replace(predecessor,STAGE_V6.encode(),1).replace(prior,STAGE_B49_V3.encode(),1).replace(B50,STAGE_B50.encode(),1)
    proof=previous_validate(normalized,digest);compile(raw,str(BUILDER),'exec')
    return {**proof,'compatible_v7_predecessors':present,'B50_stage_module_version':2 if present else 1,'B51_additive_stage_present':addition in raw}

def checked_dependency(path,digest):
    path=Path(path)
    if path.resolve()==BUILDER:validate_builder_bytes(path.read_bytes(),digest)
    elif sha(path.read_bytes())!=digest:raise ValueError('Native dependency changed:'+str(path))
    return True
