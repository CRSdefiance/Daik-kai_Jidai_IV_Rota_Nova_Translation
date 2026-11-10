"""Permit only the two extra glyphs in one exact source-restored opaque cry."""
import linecache
from scripts import plan_hodram_B0_B41_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


def restore_source_alphabet(adapter):
    return checked_text(adapter,{
        "c in '…？！○×Ｉ'":
            "(c in '…？！○×Ｉ' or row['id']=='DK4_MES_B40_R0092' and c in 'ーッ')",
    })


source=checked_text(prior.source,{
    'adapter=checked_text(previous.ADAPTER,{':'adapter=checked_text(restore_source_alphabet(previous.ADAPTER),{',
})
env={**prior.main.__globals__,**globals(),'__file__':__file__}
filename=__file__+'::same-native-layout-one-exact-source-alphabet-extension'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']

if __name__=='__main__':main()
