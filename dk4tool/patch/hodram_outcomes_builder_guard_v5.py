"""Permit only exact preserved stages or one source-locked corrected B49 stage after compatible V8377."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v4 import BUILDER,STAGE_V4,STAGE_B49,validate_builder_bytes as previous_validate
from scripts.source_locked_derivation_v5118 import checked_text

STAGE_V5=checked_text('if True:\n'+STAGE_V4,{'hodram_outcomes_editorial_v4':'hodram_outcomes_editorial_v5'}).split('\n',1)[1]
STAGE_B49_V2=checked_text('if True:\n'+STAGE_B49,{'hodram_B49_editorial_v1':'hodram_B49_editorial_v2'}).split('\n',1)[1]

def validate_builder_bytes(raw,digest):
    if not isinstance(raw,bytes):raise ValueError('Hodram builder guard: complete builder bytes required')
    stage,addition=STAGE_V5.encode(),STAGE_B49_V2.encode();normalized=raw
    if addition in raw and stage not in raw:raise ValueError('Hodram builder guard: corrected B49 requires complete compatible v5 predecessor')
    if stage in raw:
        if raw.count(stage)!=1 or STAGE_V4.encode() in raw or STAGE_B49.encode() in raw:
            raise ValueError('Hodram builder guard: one exact compatible v5 stage without mixed owned versions required')
        if raw.count(addition)>1:raise ValueError('Hodram builder guard: corrected B49 stage must occur once')
        normalized=normalized.replace(stage,STAGE_V4.encode(),1)
        if addition in raw:normalized=normalized.replace(addition,STAGE_B49.encode(),1)
    proof=previous_validate(normalized,digest);compile(raw,str(BUILDER),'exec')
    if stage in raw:
        inverse=raw.replace(stage,b'',1)
        if addition in inverse:inverse=inverse.replace(addition,b'',1)
        if sha(inverse)!=digest:raise ValueError('Hodram builder guard: every unowned original builder byte must invert exactly')
    return {**proof,'corrected_B49_stage_version':2 if addition in raw else None,'compatible_v5_predecessor':stage in raw}

def checked_dependency(path,digest):
    path=Path(path)
    if path.resolve()==BUILDER:validate_builder_bytes(path.read_bytes(),digest)
    elif sha(path.read_bytes())!=digest:raise ValueError('Native dependency changed:'+str(path))
    return True
