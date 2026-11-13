"""Expose the original static_text stage through the qualified final check."""
from scripts.registered_canonical_extension_resume_v6 import run_driver

def main():
    run_driver('static_text',__file__)

if __name__=='__main__':main()
