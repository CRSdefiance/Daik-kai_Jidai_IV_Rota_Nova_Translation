"""Expose the callable original next_owned_fields stage to the registered chain."""
from scripts.registered_canonical_extension_resume_v5 import run_driver

def main():
    run_driver('next_owned_fields',__file__)

if __name__=='__main__':main()
