"""Preserve full source/current bytes, original end and two-byte source tail."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_relocation_tools_v7148')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/research_lil_B220_relocation_v6940.py';b='scripts/research_lil_B224_relocation_v7148.py'
    c={'B220':'B224','relocation_v6940':'relocation_v7148','blocks[220]':'blocks[224]','block=220':'block=224','block220_RESEARCH':'block224_RESEARCH','[220]':'[224]',
      'len(source)==1280 and 8+struct.unpack_from(\'<H\',source,4)[0]==1280 and source[1280:]==bytes(0)':'len(source)==960 and 8+struct.unpack_from(\'<H\',source,4)[0]==958 and source[958:]==bytes(2)',
      'len(patches)==17':'len(patches)==15','source[last:1280]':'source[last:958]','mapped(1280)':'mapped(958)','len(commands)==20 and len(speeches)==17':'len(commands)==18 and len(speeches)==15',
      '1266':'944','1274':'952','1276':'954','00a0ffff43000110':'00a0ffff46000110',
      "struct.pack_into('<H',restored,4,1272)":"struct.pack_into('<H',restored,4,950)",
      'bytes(restored)+source[1280:]==source':'bytes(restored)+source[958:]==source',
      'source_bytes=1280,source_logical_end=1280,source_tail_bytes=0':'source_bytes=960,source_logical_end=958,source_tail_bytes=2',
      'inverse_recovers_every_original1280_byte':'inverse_recovers_every_original960_byte','all20_original_commands':'all18_original_commands',
      'all17_objects20_commands_full1280_inverse_RESEARCH':'all15_objects18_commands_full960_inverse_RESEARCH','all17_exact_source_current_compiled_and_research_references_bound':'all15_exact_source_current_compiled_and_research_references_bound',
      'source=1280,target=':'source=960,target=','seventeen speech C strings':'fifteen speech C strings','complete1280-byte inverse':'complete960-byte inverse'}
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);row=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_relocation.json',dict(tool=row,original_source_logical958_stored960_tail2_and_end954_preserved=True,all_native_high_integer_constants_and_multiplicity_preserved=True,no_old_prose_or_ROM_overwritten=True,new_credit=0,full_goal_complete=False))
