"""Keep the ten registered negatives and target the FI and stored refs in this batch."""
from scripts.qualify_rafael557_registered_successor_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'changed-FU-macro':'changed-FI-macro',
    "'{MACRO:FU}'":"'{MACRO:FI}'",
    "set(config['blocks'])|{140}":"set(config['blocks'])|{176}",
    'DK4_MES_B154_R0084':'DK4_MES_B177_R0180',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-ten-source-display-and-order-rejections','exec'),globals())
