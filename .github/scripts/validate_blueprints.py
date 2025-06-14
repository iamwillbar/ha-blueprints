#!/usr/bin/env python3
"""
Home Assistant Blueprint YAML Validation Script

Validates YAML syntax and Home Assistant Blueprint schema compliance.
"""

import sys
import os
import glob
import yaml
from ha_yaml_loader import HomeAssistantLoader, load_ha_yaml_file


def validate_yaml_syntax():
    """Validate YAML syntax for all blueprint files"""
    print("🔍 Validating Home Assistant Blueprint YAML syntax...")
    
    blueprint_files = glob.glob('blueprints/**/*.yaml', recursive=True) + \
                     glob.glob('blueprints/**/*.yml', recursive=True)
    
    if not blueprint_files:
        print("⚠️  No blueprint files found in blueprints/ directory")
        return True
    
    all_valid = True
    
    for filepath in blueprint_files:
        print(f"Checking: {filepath}")
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Parse with Home Assistant loader
            yaml.load(content, Loader=HomeAssistantLoader)
            print(f'✅ Valid Home Assistant Blueprint YAML: {filepath}')
            
        except yaml.YAMLError as e:
            print(f'❌ Invalid YAML: {filepath} - Error: {e}')
            all_valid = False
        except Exception as e:
            print(f'❌ Error reading file: {filepath} - Error: {e}')
            all_valid = False
    
    return all_valid


def validate_blueprint_schema():
    """Validate Home Assistant Blueprint schema compliance"""
    print("🏠 Validating Home Assistant Blueprint schema...")
    
    blueprint_files = glob.glob('blueprints/**/*.yaml', recursive=True) + \
                     glob.glob('blueprints/**/*.yml', recursive=True)
    
    required_fields = ['name', 'domain']
    valid_domains = ['automation', 'script', 'template']
    all_valid = True
    
    for filepath in blueprint_files:
        print(f"Validating blueprint schema: {filepath}")
        try:
            data = load_ha_yaml_file(filepath)
            
            if not isinstance(data, dict):
                print(f'❌ Blueprint must be a YAML object: {filepath}')
                all_valid = False
                continue
            
            if 'blueprint' not in data:
                print(f'❌ Missing "blueprint" key: {filepath}')
                all_valid = False
                continue
            
            blueprint = data['blueprint']
            
            # Check required fields
            for field in required_fields:
                if field not in blueprint:
                    print(f'❌ Missing required field "{field}" in blueprint metadata: {filepath}')
                    all_valid = False
            
            # Validate domain
            if 'domain' in blueprint and blueprint['domain'] not in valid_domains:
                print(f'❌ Invalid domain "{blueprint["domain"]}". Must be one of {valid_domains}: {filepath}')
                all_valid = False
            
            # Validate name is a string and not empty
            if 'name' in blueprint:
                if not isinstance(blueprint['name'], str) or not blueprint['name'].strip():
                    print(f'❌ Blueprint name must be a non-empty string: {filepath}')
                    all_valid = False
            
            # Check for recommended fields
            recommended_fields = ['description', 'author']
            missing_recommended = [f for f in recommended_fields if f not in blueprint]
            if missing_recommended:
                print(f'⚠️  Missing recommended fields {missing_recommended}: {filepath}')
            
            if all_valid:
                print(f'✅ Valid blueprint schema: {filepath}')
            
        except yaml.YAMLError as e:
            print(f'❌ YAML error in: {filepath} - Error: {e}')
            all_valid = False
        except Exception as e:
            print(f'❌ Error validating: {filepath} - Error: {e}')
            all_valid = False
    
    return all_valid


def check_duplicate_names():
    """Check for duplicate blueprint names"""
    print("🔍 Checking for duplicate blueprint names...")
    
    blueprint_files = glob.glob('blueprints/**/*.yaml', recursive=True) + \
                     glob.glob('blueprints/**/*.yml', recursive=True)
    
    names = {}
    duplicates = []
    
    for filepath in blueprint_files:
        try:
            data = load_ha_yaml_file(filepath)
            
            if 'blueprint' in data and 'name' in data['blueprint']:
                name = data['blueprint']['name']
                if name in names:
                    duplicates.append((name, names[name], filepath))
                else:
                    names[name] = filepath
        except Exception as e:
            print(f'Error reading {filepath}: {e}')
    
    if duplicates:
        print('❌ Duplicate blueprint names found:')
        for name, file1, file2 in duplicates:
            print(f'  "{name}" in {file1} and {file2}')
        return False
    else:
        print('✅ No duplicate blueprint names found')
        return True


def main():
    """Main validation function"""
    if len(sys.argv) > 1:
        validation_type = sys.argv[1]
        
        if validation_type == 'syntax':
            success = validate_yaml_syntax()
        elif validation_type == 'schema':
            success = validate_blueprint_schema()
        elif validation_type == 'duplicates':
            success = check_duplicate_names()
        else:
            print(f"Unknown validation type: {validation_type}")
            print("Usage: python validate_blueprints.py [syntax|schema|duplicates]")
            sys.exit(1)
    else:
        # Run all validations
        syntax_ok = validate_yaml_syntax()
        schema_ok = validate_blueprint_schema()
        duplicates_ok = check_duplicate_names()
        success = syntax_ok and schema_ok and duplicates_ok
    
    if not success:
        sys.exit(1)
    
    print("🎉 All validations passed!")


if __name__ == '__main__':
    main()
