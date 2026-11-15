"""Challenge the unchanged source, staged control and exact target guards."""
from scripts.qualify_rafael_B161_B165_registered_successor_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'DK4_MES_B162_R0006':'DK4_MES_B166_R0797',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-ten-semantic-and-order-rejections','exec'),globals())
