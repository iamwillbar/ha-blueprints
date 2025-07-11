#!/usr/bin/env python3
"""
Blueprint Processing Script

Generates semantic versions for blueprints based on commit history and
processes them for deployment.
"""

import os
import yaml
import subprocess
import glob
from pathlib import Path
from ha_yaml_loader import HomeAssistantLoader, load_ha_yaml_file


def get_git_commits_for_file(filepath):
    """Get commit history for a specific file"""
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', '--follow', '--', filepath],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []


def calculate_semver(commits, filepath):
    """Calculate semantic version based on commit messages"""
    # Start with version 1.0.0
    major = 1
    minor = 0
    patch = 0
    
    # If no commits, return initial version
    if not commits or len([c for c in commits if c.strip()]) == 0:
        return '1.0.0'
    
    # Process commits from oldest to newest (reverse the list)
    is_first_commit = True
    for commit in reversed(commits):
        if not commit.strip():
            continue
        
        # Skip incrementing for the first commit - it establishes the base version 1.0.0
        if is_first_commit:
            is_first_commit = False
            continue
        
        commit_msg = commit.split(' ', 1)[1] if ' ' in commit else commit
        commit_lower = commit_msg.lower()
        
        # Major version indicators
        major_keywords = ['breaking change', 'breaking:', 'major:', '!:', 'incompatible']
        minor_keywords = ['feat:', 'feature:', 'add:', 'new:', 'minor:', 'enhancement']
        
        if any(keyword in commit_lower for keyword in major_keywords):
            # Major: increment major, reset minor and patch to 0
            major += 1
            minor = 0
            patch = 0
        elif any(keyword in commit_lower for keyword in minor_keywords):
            # Minor: increment minor, reset patch to 0
            minor += 1
            patch = 0
        else:
            # All other commits (including patch keywords and unmatched): increment patch
            patch += 1
    
    return f"{major}.{minor}.{patch}"


def process_blueprints():
    """Process all blueprints and generate versioned copies"""
    print("📝 Generating semantic versions based on commit history...")
    
    # Get the repo root directory (go up two levels from .github/scripts)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))
    
    # Create output directory
    dist_dir = os.path.join(repo_root, 'dist', 'blueprints')
    os.makedirs(dist_dir, exist_ok=True)
    
    blueprint_info = []
    blueprints_dir = os.path.join(repo_root, 'blueprints')
    blueprint_files = glob.glob(os.path.join(blueprints_dir, '**/*.yaml'), recursive=True) + \
                     glob.glob(os.path.join(blueprints_dir, '**/*.yml'), recursive=True)
    
    for filepath in blueprint_files:
        try:
            # Parse with Home Assistant loader
            data = load_ha_yaml_file(filepath)
            
            if 'blueprint' not in data:
                continue
            
            # Get commit history and calculate version
            commits = get_git_commits_for_file(filepath)
            version = calculate_semver(commits, filepath)
            # Extract latest commit hash from the first commit in the list
            latest_commit = commits[0].split(' ')[0] if commits and commits[0].strip() else None
            
            # Create versioned blueprint
            original_name = data['blueprint']['name']
            data['blueprint']['name'] = f'{original_name} v{version}'
            
            # Preserve relative directory structure
            rel_path = os.path.relpath(filepath, blueprints_dir)
            output_path = os.path.join(dist_dir, rel_path)
            
            # Create output directory
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write versioned blueprint (preserve original format)
            with open(filepath, 'r') as f:
                original_content = f.read()
            
            # Simple string replacement to update the name while preserving format
            updated_content = original_content.replace(
                f'name: {original_name}',
                f'name: {original_name} v{version}',
                1  # Only replace first occurrence
            )
            # Also handle quoted names
            updated_content = updated_content.replace(
                f'name: "{original_name}"',
                f'name: "{original_name} v{version}"',
                1
            )
            updated_content = updated_content.replace(
                f"name: '{original_name}'",
                f"name: '{original_name} v{version}'",
                1
            )
            
            with open(output_path, 'w') as f:
                f.write(updated_content)
            
            # Collect info for index
            blueprint_info.append({
                'name': original_name,
                'versioned_name': data['blueprint']['name'],
                'version': version,
                'domain': data['blueprint']['domain'],
                'description': data['blueprint'].get('description', ''),
                'author': data['blueprint'].get('author', ''),
                'file_path': rel_path,
                'min_version': data['blueprint'].get('homeassistant', {}).get('min_version', ''),
                'category': os.path.dirname(rel_path) if os.path.dirname(rel_path) else 'General',
                'latest_commit': latest_commit
            })
            
            print(f'✅ Processed {filepath} -> v{version}')
            
        except Exception as e:
            print(f'❌ Error processing {filepath}: {e}')
            continue
    
    # Save blueprint info for index generation
    blueprint_info_path = os.path.join(repo_root, 'dist', 'blueprint_info.yaml')
    with open(blueprint_info_path, 'w') as f:
        yaml.dump(blueprint_info, f, default_flow_style=False)
    
    print(f'📦 Processed {len(blueprint_info)} blueprints')
    return blueprint_info


def main():
    """Main processing function"""
    process_blueprints()


if __name__ == '__main__':
    main()
