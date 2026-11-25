"""Expose the callable original Fernan_field stage to the registered chain."""
from scripts.registered_canonical_extension_resume_v5 import run_driver

def main():
    run_driver('Fernan_field',__file__)

if __name__=='__main__':main()
