import os
import shutil

def set_vim_config():
    """
    Copy the enhanced VimTeX configuration file as .vimrc to the user's home directory.
    Creates a backup of existing .vimrc if it exists.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the enhanced VimTeX config template
    source_config = os.path.join(script_dir, '..', 'templates', 'enhanced_vimtex_config.vim')
    source_config = os.path.abspath(source_config)
    
    # Path to the user's home directory .vimrc
    home_dir = os.path.expanduser('~')
    target_vimrc = os.path.join(home_dir, '.vimrc')
    
    # Check if source file exists
    if not os.path.exists(source_config):
        print(f"Error: Source configuration file not found at {source_config}")
        return False
    
    # Create backup if .vimrc already exists
    if os.path.exists(target_vimrc):
        backup_path = target_vimrc + '.backup'
        try:
            shutil.copy2(target_vimrc, backup_path)
            print(f"Created backup of existing .vimrc at {backup_path}")
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")
    
    # Copy the enhanced VimTeX config as .vimrc
    try:
        shutil.copy2(source_config, target_vimrc)
        print(f"Successfully copied enhanced VimTeX configuration to {target_vimrc}")
        print("Your Vim is now configured for enhanced LaTeX editing!")
        return True
    except Exception as e:
        print(f"Error copying configuration file: {e}")
        return False

def main():
    """Main function to run the vim configuration setup."""
    print("Setting up enhanced VimTeX configuration...")
    print("=" * 50)
    
    success = set_vim_config()
    
    if success:
        print("\nConfiguration complete!")
        print("\nNext steps:")
        print("1. Install required Vim plugins (VimTeX, UltiSnips)")
        print("2. Install Zathura PDF viewer")
        print("3. Restart Vim to load the new configuration")
        print("\nPlugin installation commands:")
        print("  For vim-plug: Add the following to your .vimrc and run :PlugInstall")
        print("    Plug 'lervag/vimtex'")
        print("    Plug 'SirVer/ultisnips'")
        print("    Plug 'honza/vim-snippets'")
    else:
        print("\nConfiguration failed. Please check the error messages above.")

if __name__ == "__main__":
    main()

