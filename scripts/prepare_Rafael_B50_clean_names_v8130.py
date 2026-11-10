"""Read B50's three clean static identities before new body/name comparison."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/read_Rafael_B49_clean_names_v8074.py','scripts/read_Rafael_B50_clean_names_v8130.py',{
        'Rafael_B49_clean_names_v8074':'Rafael_B50_clean_names_v8130',
        'Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json':'Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json',
        '[0,2,4,5,6,8,9]':'[0,2,9]',
        'seven_clean_static_identity_fields_before_current_English.json':'three_clean_static_identity_fields_before_current_English.json','B49':'B50',
    }))
