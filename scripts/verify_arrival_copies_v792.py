"""Complete original native copies for every entry in six repacked blocks."""

from pathlib import Path
from types import FunctionType

from dk4tool.patch.arrival_notices_editorial import ROOT
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_schemes_copies_v776 as original
from scripts.verify_village_wrap_v608 import read,save


if __name__=='__main__':
    common=(ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes();arm=(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes()
    (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').write_bytes(arm)
    plan=read(ROOT/'prospective_repack.json')
    save(ROOT/'prospective_common_repack.json',{**plan,'target_COMMON_sha256':sha(common),'target_ARM9_sha256':sha(arm)})
    FunctionType(original.main.__code__,{**original.__dict__,'SOURCE':ROOT,'ROOT':ROOT/'native_copies',
        '__file__':str(Path(__file__).resolve())})()
