"""Exercise the registered mixed-menu transaction's source, display and order rejection guards."""
from scripts.qualify_rafael_B181_B200_registered_successor_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source=checked_text(previous,{
    'changed-Aziza-panel-selector':'changed-signature-panel-selector',
    'DK4_MES_B187_R0015':'DK4_MES_B216_R0074',
    'DK4_MES_B181_R0005':'DK4_MES_B201_R0006',
    "set(config['blocks'])|{201}":"set(config['blocks'])|{221}",
    "doc['records'][0]['english'] += ' Changed.'":
        "next(r for r in doc['records'] if r['kind']=='typed-choice-label' and r['block']==209 and r['source_index']==2)['english'] += ' Changed.'",
    'changed-logical-prose':'changed-three-choice-caption',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-ten-semantic-and-order-rejections','exec'),globals())

