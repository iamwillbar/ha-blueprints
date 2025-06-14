#!/usr/bin/env python3
"""
Home Assistant YAML Loader Utility

Provides a custom YAML loader that handles Home Assistant specific tags like
!input, !include, !secret, and !env_var.
"""

import yaml


class HomeAssistantLoader(yaml.SafeLoader):
    """Custom YAML loader that handles Home Assistant specific tags"""
    pass


def input_constructor(loader, node):
    """Handle !input tags"""
    if isinstance(node, yaml.ScalarNode):
        return f'INPUT:{loader.construct_scalar(node)}'
    elif isinstance(node, yaml.MappingNode):
        return {f'INPUT:{k}': v for k, v in loader.construct_mapping(node).items()}
    elif isinstance(node, yaml.SequenceNode):
        return [f'INPUT:{item}' for item in loader.construct_sequence(node)]
    return loader.construct_object(node)


def include_constructor(loader, node):
    """Handle !include tags"""
    return f'INCLUDE:{loader.construct_scalar(node)}'


def secret_constructor(loader, node):
    """Handle !secret tags"""
    return f'SECRET:{loader.construct_scalar(node)}'


def env_var_constructor(loader, node):
    """Handle !env_var tags"""
    return f'ENV_VAR:{loader.construct_scalar(node)}'


# Register constructors for Home Assistant tags
HomeAssistantLoader.add_constructor('!input', input_constructor)
HomeAssistantLoader.add_constructor('!include', include_constructor)
HomeAssistantLoader.add_constructor('!secret', secret_constructor)
HomeAssistantLoader.add_constructor('!env_var', env_var_constructor)


def load_ha_yaml(content):
    """Load YAML content with Home Assistant tag support"""
    return yaml.load(content, Loader=HomeAssistantLoader)


def load_ha_yaml_file(filepath):
    """Load YAML file with Home Assistant tag support"""
    with open(filepath, 'r') as f:
        content = f.read()
    return load_ha_yaml(content)
