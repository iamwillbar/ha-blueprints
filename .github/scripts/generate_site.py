#!/usr/bin/env python3
"""
GitHub Pages Site Generation Script

Generates a beautiful HTML catalog of Home Assistant Blueprints using Jinja2 templates.
"""

import yaml
import json
import os
from datetime import datetime
from urllib.parse import quote
from jinja2 import Environment, FileSystemLoader


def generate_site():
    """Generate the GitHub Pages site"""
    print("🌐 Generating GitHub Pages site...")
    
    # Load blueprint info
    # Get the repo root directory (go up two levels from .github/scripts)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))
    blueprint_info_path = os.path.join(repo_root, 'dist', 'blueprint_info.yaml')
    
    with open(blueprint_info_path, 'r') as f:
        blueprints = yaml.safe_load(f) or []
    
    # Get repository info from environment
    repo_owner = os.environ.get('GITHUB_REPOSITORY', '').split('/')[0] if os.environ.get('GITHUB_REPOSITORY') else 'your-username'
    repo_name = os.environ.get('GITHUB_REPOSITORY', '').split('/')[1] if '/' in os.environ.get('GITHUB_REPOSITORY', '') else 'ha-blueprints'
    
    # Group blueprints by category
    categories = {}
    for bp in blueprints:
        category = bp['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(bp)
    
    # Sort categories and blueprints
    sorted_categories = {}
    for category in sorted(categories.keys()):
        sorted_categories[category] = sorted(categories[category], key=lambda x: x['name'])
    
    # Calculate statistics
    stats = {
        'total_blueprints': len(blueprints),
        'total_categories': len(categories),
        'total_domains': len(set(bp['domain'] for bp in blueprints)),
        'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    }
    
    # Set up Jinja2 environment
    # Get the repo root directory (go up two levels from .github/scripts)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))
    template_dir = os.path.join(repo_root, '.github', 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Define custom filters
    def url_quote(text):
        return quote(text)
    
    def escape_html(text):
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;'))
    
    def truncate_description(text, length=200):
        if len(text) > length:
            return text[:length] + '...'
        return text
    
    def clean_description(text):
        return text.replace('\n', ' ').strip()
    
    env.filters['url_quote'] = url_quote
    env.filters['escape_html'] = escape_html
    env.filters['truncate_description'] = truncate_description
    env.filters['clean_description'] = clean_description
    
    # Load and render template
    template = env.get_template('index.html.j2')
    
    html_content = template.render(
        blueprints=blueprints,
        categories=sorted_categories,
        stats=stats,
        repo_owner=repo_owner,
        repo_name=repo_name
    )
    
    # Write HTML file
    output_path = os.path.join(repo_root, 'dist', 'index.html')
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    print(f'✅ Generated index.html with {len(blueprints)} blueprints')


def main():
    """Main generation function"""
    generate_site()


if __name__ == '__main__':
    main()
