---
applyTo: '**'
---
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/c### Blueprint Quality Standards

## Repository Overview

This is a Home Assistant blueprints repository that provides high-quality, validated blueprints for automations, scripts, and templates. The repository includes automated validation, semantic versioning, and a GitHub Pages catalog for easy blueprint discovery and installation.

## Development Commands

### Validation
```bash
# Validate YAML syntax for a blueprint
python -c "import yaml; yaml.safe_load(open('blueprints/path/to/blueprint.yaml'))"
```

### Testing
No formal test suite is present. Validation is performed through:
- YAML syntax validation
- Home Assistant blueprint schema validation (via GitHub Actions)
- Manual testing in Home Assistant environments

## Architecture and Structure

### Core Structure
```
blueprints/
├── automations/
│   ├── maintenance/     # Maintenance-related automations
│   └── safety/         # Safety and monitoring automations
├── script/             # Reusable script blueprints
└── template/           # Template blueprints
```

### Blueprint Categories
- **Safety**: Air quality monitoring, temperature monitoring, security alerts
- **Maintenance**: Equipment maintenance reminders, filter replacements

### Blueprint Development Standards

#### Required Metadata Structure
```yaml
blueprint:
  name: "Descriptive Blueprint Name"
  description: |
    Brief description with features, requirements, and usage notes.
  domain: automation|script|template
  author: "Your Name"
  homeassistant:
    min_version: "2024.6.0"
```

#### Input Organization Pattern
Use sectioned inputs (requires HA 2024.6.0+) in this specific order:
- **main_config**: Core configuration (sensors, devices, targets)
- **threshold_config**: Timing thresholds, delays, and trigger conditions
- **notification_config**: Notification settings and services  
- **advanced_settings**: Optional settings (collapsed by default)

#### Naming Conventions
- **Blueprint names**: Title case, descriptive, under 50 characters
- **Input keys**: snake_case (e.g., `motion_sensor`, `delay_time`)
- **File names**: kebab-case (e.g., `motion-activated-light.yaml`)

#### Essential Blueprint Patterns
- Use `!input` for referencing inputs
- Define variables section for commonly used values
- Use appropriate selectors with filters for better UX
- Provide sensible defaults for all optional inputs
- Use `mode: single` for single-entity automations (one door, one sensor)
- Use `mode: parallel` only for multi-entity automations that can run simultaneously
- Always include `max_exceeded: silent` to prevent log spam
- Use `threshold_config` for timing-related settings (delays, intervals, thresholds)
- Collapse `threshold_config` and `advanced_settings` sections by default

#### Home Assistant Integration
- Blueprints are designed for ESPHome integration (especially air quality sensors)
- Support for standard HA notification services
- Compatible with domain-specific device classes (motion, temperature, etc.)

#### Automation Mode Selection
- **single**: For single-entity automations (one sensor, one device)
- **parallel**: Only for multi-entity automations that can safely run concurrently
- Always include `max_exceeded: silent`

## Semantic Versioning

Commit messages determine version bumps:
- **Major** (x.0.0): `breaking change`, `breaking:`, `major:`, `!:`, `incompatible`
- **Minor** (1.x.0): `feat:`, `feature:`, `add:`, `new:`, `enhancement`
- **Patch** (1.0.x): `fix:`, `patch:`, `bug:`, `hotfix:`, `chore:`, `docs:`, `style:`

## Blueprint Quality Standards

### Validation Requirements
All blueprints must pass:
- YAML syntax validation
- Home Assistant blueprint schema compliance
- Best practice compliance checks

### User Experience Standards
- Clear, helpful descriptions with markdown formatting
- Appropriate input selectors with domain/device_class filters
- Logical input grouping with descriptive sections
- Sensible default values for all optional inputs
- Recovery/clear notifications for alert-based automations

### Critical Safety Patterns
For safety-critical blueprints (like CO monitoring):
- Implement repeated alerts for critical conditions
- Use appropriate alert priorities and actions
- Provide clear action guidance in notifications
- Include clear thresholds based on safety standards

## Development Workflow

1. Create blueprint in appropriate category folder
2. Follow naming conventions and metadata requirements
3. Use conventional commit messages for proper versioning
4. GitHub Actions handles validation and publishing automatically
5. Blueprints are published to GitHub Pages catalog with import buttons

## Important Files

- `README.md`: Repository documentation and setup instructions
- Individual blueprint files contain extensive inline documentation
