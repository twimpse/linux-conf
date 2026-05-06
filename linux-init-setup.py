#!/usr/bin/python3
import os
import subprocess
import re
import argparse
import sys
from pathlib import Path

def setup_bashrc():
    """Add ls alias to .bashrc if missing"""
    bashrc_path = os.path.expanduser("~/.bashrc")
    alias_line = "alias ls='ls --color=auto'"
    
    try:
        with open(bashrc_path, 'r') as file:
            content = file.read()
        
        if "alias ls=" in content and "--color" in content:
            print("✓ Found ls alias with color in .bashrc")
            return True
        else:
            print("No color alias found for ls in .bashrc, adding...")
            with open(bashrc_path, 'a') as file:
                file.write(f"\n{alias_line}  # Added by linux-conf\n")
            print("✓ Added ls alias to .bashrc")
            return True
    except FileNotFoundError:
        print(f"File not found: {bashrc_path}, creating...")
        with open(bashrc_path, 'w') as file:
            file.write(f"# .bashrc created by linux-conf\n{alias_line}  # Added by linux-conf\n")
        print("✓ Created .bashrc and added alias")
        return True
    except Exception as e:
        print(f"Error with .bashrc: {e}")
        return False

def setup_ssh_authorized_keys():
    """Add keys from conf.d/authorized_keys to .ssh/authorized_keys"""
    source_keys = "conf.d/authorized_keys"
    ssh_dir = os.path.expanduser("~/.ssh")
    dest_keys = os.path.join(ssh_dir, "authorized_keys")
    
    # Check if source file exists
    if not os.path.exists(source_keys):
        print(f"Source key file not found: {source_keys}")
        return False
    
    # Create .ssh directory if it doesn't exist
    if not os.path.exists(ssh_dir):
        print(f"Creating .ssh directory: {ssh_dir}")
        os.makedirs(ssh_dir, mode=0o700)
    
    # Read source keys
    try:
        with open(source_keys, 'r') as src:
            source_content = src.read()
        
        # Check if dest file exists and contains these keys
        if os.path.exists(dest_keys):
            with open(dest_keys, 'r') as dest:
                dest_content = dest.read()
            
            if source_content.strip() in dest_content:
                print("✓ SSH keys already present in authorized_keys")
                return True
        
        # Append keys to authorized_keys
        with open(dest_keys, 'a') as dest:
            dest.write(f"\n# Keys added by linux-conf\n{source_content}\n")
        
        # Set proper permissions
        os.chmod(dest_keys, 0o600)
        print("✓ Added SSH keys to authorized_keys")
        return True
        
    except Exception as e:
        print(f"Error setting up SSH keys: {e}")
        return False

def install_packages(package_type):
    """Install packages based on server/client role"""
    # Common packages for both
    common_packages = [
        "vim",
        "htop"
    ]
    
    # Server-specific packages
    server_packages = [
        "openssh-server",
        "bmon",
        "iptables-persistent"
    ]
    
    # Client-specific packages
    client_packages = [
        "irssi"
    ]
    
    packages = common_packages.copy()
    if package_type == "server":
        packages.extend(server_packages)
        print("\nInstalling SERVER packages...")
    else:
        packages.extend(client_packages)
        print("\nInstalling CLIENT packages...")
    
    # Update package list
    print("Updating package list...")
    try:
        subprocess.run(["sudo", "apt", "update"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error updating packages: {e}")
        return False
    
    # Install packages
    print(f"Installing {len(packages)} packages...")
    try:
        subprocess.run(["sudo", "apt", "install", "-y"] + packages, check=True)
        print(f"✓ Successfully installed {package_type} packages")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False

def prompt_user_interactive():
    """Ask user for configuration choices interactively"""
    print("\n" + "="*50)
    print("System Configuration Setup")
    print("="*50)
    
    while True:
        role = input("\nIs this a [s]erver or [c]lient setup? (s/c): ").lower()
        if role in ['s', 'server']:
            return 'server'
        elif role in ['c', 'client']:
            return 'client'
        else:
            print("Please enter 's' for server or 'c' for client")
    
    return None

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Linux system configuration script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --role server --no-ssh
  %(prog)s --role client --packages-only
  %(prog)s --role server --skip-packages
        """
    )
    
    parser.add_argument(
        '--role', '-r',
        choices=['server', 'client'],
        help='Set system role (server or client)'
    )
    
    parser.add_argument(
        '--skip-bashrc',
        action='store_true',
        help='Skip .bashrc configuration'
    )
    
    parser.add_argument(
        '--skip-ssh',
        action='store_true',
        help='Skip SSH key setup'
    )
    
    parser.add_argument(
        '--skip-packages',
        action='store_true',
        help='Skip package installation'
    )
    
    parser.add_argument(
        '--packages-only',
        action='store_true',
        help='Only install packages (skip bashrc and SSH setup)'
    )
    
    parser.add_argument(
        '--non-interactive',
        action='store_true',
        help='Run in non-interactive mode (requires --role)'
    )
    
    return parser.parse_args()

def main():
    print("Main Setup Starting")
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Check for non-interactive mode
    if args.non_interactive and not args.role:
        print("Error: --role is required when using --non-interactive")
        sys.exit(1)
    
    # Determine role
    role = None
    if args.role:
        role = args.role
        print(f"Role set to: {role} (from command line)")
    elif not args.packages_only:
        role = prompt_user_interactive()
    
    # Run configuration based on flags
    success_count = 0
    total_tasks = 0
    
    # Setup bashrc
    if not args.skip_bashrc and not args.packages_only:
        total_tasks += 1
        if setup_bashrc():
            success_count += 1
    
    # Setup SSH authorized_keys
    if not args.skip_ssh and not args.packages_only:
        total_tasks += 1
        if setup_ssh_authorized_keys():
            success_count += 1
    
    # Install packages
    if not args.skip_packages and role:
        total_tasks += 1
        if install_packages(role):
            success_count += 1
    elif not args.skip_packages and not role and not args.packages_only:
        print("\nNo role specified, skipping package installation")
    elif args.packages_only and role:
        total_tasks += 1
        if install_packages(role):
            success_count += 1
    
    # Summary
    print("\n" + "="*50)
    print("Setup Complete!")
    print(f"✓ {success_count}/{total_tasks} tasks completed successfully")
    
    if not args.skip_bashrc and not args.packages_only:
        print("\nTo apply .bashrc changes, run: source ~/.bashrc or logout and login again")
    
    if role == "server" and not args.skip_packages:
        print("\n💡 Server setup notes:")
        print("   - Configure firewall: sudo ufw enable")
        print("   - Check SSH status: sudo systemctl status ssh")

if __name__ == "__main__":
    main()
