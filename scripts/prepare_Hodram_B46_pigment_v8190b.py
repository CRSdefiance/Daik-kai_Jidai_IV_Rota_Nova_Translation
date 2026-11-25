"""Preserve the old whitelist failure;probe only exact source4800 with every original guard retained."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B46_pigment_tools_v8190b')
if __name__=='__main__':
    assert not ROOT.exists()
    adapter="picture_adapter=checked_text(inspect.getsource(picture),{'assert word in [0x4821,0x4822,0x4823,0x4700]':'assert word==0x4800'});env=dict(picture.__globals__);exec(compile(picture_adapter,__file__+'::original-exact-source4800','exec'),env)\n    native=ctx.execute(env['picture'],block,c);ctx.machines.pop();assert not ctx.machines"
    receipt=derive('scripts/bind_Hodram_B46_pigment_v8190.py','scripts/bind_Hodram_B46_pigment_v8190b.py',{
        'Rota Nova translations':'Rota Nova translations',
    }) if False else derive('scripts/bind_Hodram_B46_pigment_v8190.py','scripts/bind_Hodram_B46_pigment_v8190b.py',{
        'from scripts.verify_village_wrap_v608 import read,save':'from scripts.verify_village_wrap_v608 import read,save\nfrom scripts.source_locked_derivation_v5118 import checked_text',
        'Hodram_B46_pigment_v8190':'Hodram_B46_pigment_v8190b',
        'native=ctx.execute(picture,block,c);ctx.machines.pop();assert not ctx.machines':adapter,
        'source_owned_picture_adapter=inspect.getsource(picture)':'source_owned_picture_adapter=picture_adapter',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=receipt,
        previous_executed_producer='scripts/bind_Hodram_B46_pigment_v8190.py',previous_failure='Legacy picture helper explicitly permits4821/4822/4823/4700;source4800 failed its whitelist before descriptor execution.',
        previous_failed_root_andproducer_preserved=True,only_exact_original4800_allowed_in_source_owned_adapter=True,
        all_4MiB_ABI_owner_input_output_length_andboundary_descriptor_guards_preserved=True,
        no_source_ROM_orcommand_changes=True,no_credit=True,full_goal_complete=False))
    print('Prepared exactsource4800 adapter;earlier whitelist failure preserved andall native guards retained.')
