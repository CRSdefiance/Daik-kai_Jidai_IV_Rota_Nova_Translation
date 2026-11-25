"""Read predecessor prose only after clean glosses,three roles and terms are bound."""
from scripts.source_locked_derivation_v5118 import derive

if __name__=='__main__':
    print(derive('scripts/compare_lil_B193_English_v5454.py','scripts/compare_lil_B195_English_v5548.py',{
        'B193':'B195','comparison_v5454':'comparison_v5548','source_v5447/all15':'source_v5541/all20',
        'terms_v5453/three_Ladies_Seoul_Chili_and_cooking_friendship_reconciliation':
        'terms_v5547/three_roles_both_Veracruz_aliases_Cheese8_and_unnamed_specialty_reconciliation',
        'voices_v5448':'voices_v5542','dispatches_v5449/all15':'dispatches_v5543/all20',
        'names_v5452':'names_v5546','controls_v5451':'controls_v5545','all15':'all20',
    }))
