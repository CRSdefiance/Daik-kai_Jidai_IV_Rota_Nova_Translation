"""Permit exact preserved builders or one additive B50 stage after compatible outcomesv6/B49v3,with full original inverse."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v5 import BUILDER,STAGE_V5,STAGE_B49_V2,validate_builder_bytes as previous_validate
from scripts.source_locked_derivation_v5118 import checked_text

STAGE_V6=checked_text('if True:\n'+STAGE_V5,{'hodram_outcomes_editorial_v5':'hodram_outcomes_editorial_v6'}).split('\n',1)[1]
STAGE_B49_V3=checked_text('if True:\n'+STAGE_B49_V2,{'hodram_B49_editorial_v2':'hodram_B49_editorial_v3'}).split('\n',1)[1]
STAGE_B50="    hodram_B50_editorial_config = profile_config.get('hodram_B50_editorial')\n    if hodram_B50_editorial_config:\n        from dk4tool.patch.hodram_B50_editorial_v1 import apply_release as apply_hodram_B50_editorial\n\n        hodram_B50_editorial_report = apply_hodram_B50_editorial(candidate, baseline, hodram_B50_editorial_config)\n        for hodram_B50_file in hodram_B50_editorial_report['files']:\n            hodram_B50_path = hodram_B50_file['file_path']\n            grouped.setdefault(hodram_B50_path, [])\n            changed_records.setdefault(hodram_B50_path, []).extend(row['id'] for row in hodram_B50_file['changed_records'])\n            relocation_checks.setdefault(hodram_B50_path, {})['hodram_B50_editorial'] = {\n                'release_config': hodram_B50_editorial_config,\n                'release_config_sha256': sha256(Path(hodram_B50_editorial_config).read_bytes()),\n                'proof': hodram_B50_editorial_report}\n        for hodram_B50_manuscript in hodram_B50_editorial_report['manuscripts']:\n            more_batch = Path(hodram_B50_manuscript)\n            if more_batch in release_batches:\n                raise ValueError('Hodram B50 stage must run once after the complete V8475 stack')\n            release_batches.append(more_batch)\n\n"

def validate_builder_bytes(raw,digest):
    if not isinstance(raw,bytes):raise ValueError('Hodram builder guard: complete builder bytes required')
    predecessor,prior,addition=STAGE_V6.encode(),STAGE_B49_V3.encode(),STAGE_B50.encode()
    present=any(s in raw for s in [predecessor,prior,addition]);normalized=raw
    if present:
        if raw.count(predecessor)!=1 or raw.count(prior)!=1 or raw.count(addition)>1:
            raise ValueError('Hodram builder guard: complete compatible v6 andB49v3 stages once required')
        if STAGE_V5.encode() in raw or STAGE_B49_V2.encode() in raw:
            raise ValueError('Hodram builder guard: mixed owned versions forbidden')
        if raw.index(predecessor)>=raw.index(prior):raise ValueError('Hodram builder guard: original predecessor stage order required')
        if addition in raw:
            boundary=b'    # Lexically valid "% o"'
            if raw.count(boundary)!=1 or not raw.index(prior)+len(prior)<=raw.index(addition)<raw.index(boundary):
                raise ValueError('Hodram builder guard: B50 must follow complete B49 before final percent safety')
            normalized=normalized.replace(addition,b'',1)
        normalized=normalized.replace(predecessor,STAGE_V5.encode(),1).replace(prior,STAGE_B49_V2.encode(),1)
    proof=previous_validate(normalized,digest);compile(raw,str(BUILDER),'exec')
    return {**proof,'compatible_v6_predecessor':present,'corrected_B49_stage_version':3 if present else proof.get('corrected_B49_stage_version'),'B50_additive_stage_present':addition in raw}

def checked_dependency(path,digest):
    path=Path(path)
    if path.resolve()==BUILDER:validate_builder_bytes(path.read_bytes(),digest)
    elif sha(path.read_bytes())!=digest:raise ValueError('Native dependency changed:'+str(path))
    return True
