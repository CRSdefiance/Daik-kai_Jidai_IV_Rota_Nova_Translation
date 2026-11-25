"""Expose the original owned_names stage through the qualified final check."""
from scripts.registered_canonical_extension_resume_v6 import run_driver

def main():
    run_driver('owned_names',__file__)

if __name__=='__main__':main()
