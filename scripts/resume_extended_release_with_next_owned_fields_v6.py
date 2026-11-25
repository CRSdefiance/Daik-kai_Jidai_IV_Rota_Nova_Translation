"""Expose the original next_owned_fields stage through the qualified final check."""
from scripts.registered_canonical_extension_resume_v6 import run_driver

def main():
    run_driver('next_owned_fields',__file__)

if __name__=='__main__':main()
