"""Expose the original reviewed_text_data_v3 stage through the qualified final check."""
from scripts.registered_canonical_extension_resume_v6 import run_driver

def main():
    run_driver('reviewed_text_data_v3',__file__)

if __name__=='__main__':main()
