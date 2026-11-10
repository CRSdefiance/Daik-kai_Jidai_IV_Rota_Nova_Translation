"""Check the three retained native ellipses alongside the exact ordered body and header pixels."""
from scripts import analyze_rafael_B168_B169_actual_v1 as prior


prior.SPECIAL = {ident: '8163' for ident in (
    'DK4_MES_B183_R0014', 'DK4_MES_B187_R0029', 'DK4_MES_B187_R0147',
)}
prior.PIXEL_COUNTS = {ident: 6 for ident in prior.SPECIAL}

if __name__ == '__main__':
    globals()['exact_masks'] = prior.exact_masks
    exec(compile(prior.SOURCE, __file__ + '::same-ordered-check-retained-source-ellipses', 'exec'), globals())
