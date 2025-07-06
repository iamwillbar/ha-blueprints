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
- **main_config**: Core configuration (sensors, devices, targets) - Use purpose-specific icon (e.g., mdi:thermometer, mdi:door-closed, mdi:air-filter). Required sensors first, then optional sensors clearly marked as optional.
- **threshold_config**: Timing thresholds, delays, and trigger conditions - Use icon: `mdi:tune` (expanded by default)
- **notification_config**: Basic notification settings - Use icon: `mdi:bell-alert`
- **critical_notification_config**: Critical alert settings (when applicable) - Use icon: `mdi:bell-alert-outline`
- **notification_content_config**: Notification titles and messages - Use icon: `mdi:message-text` (collapsed by default), titled "Customize Notification Content (Optional)"
- **advanced_settings**: Optional settings - Use icon: `mdi:cog` (collapsed by default)

#### Notification Configuration Standards

**Core Principle: Template-Based Notifications**
- NO hardcoded notification titles or messages in action sections
- ALL notification content must be configurable through input templates
- Use placeholders (e.g., `{entity}`, `{level}`, `{limit}`, `{unit}`) for dynamic content
- Templates should support multiple entities with consistent placeholder patterns

**notification_config Section:**
- Always use icon: `mdi:bell-alert`
- For blueprints where notifications are optional: Include `send_notifications` boolean toggle
- For blueprints where notifications are the primary purpose: No send_notifications toggle needed
- Always include `notification_service` with select selector and custom_value: true
- Standard notification service options: `notify.notify`, `notify.mobile_app`, `notify.persistent_notification`

**Standard Notification Timing Settings (use consistently across blueprints):**
- `send_notifications`: "Send Notifications" - Enable/disable notifications (when optional)
- `initial_notification_delay`: "Initial Notification Delay" - Time before first notification (0-60 minutes)
- `send_reminders`: "Send Reminder Notifications" - Enable/disable reminder notifications
- `reminder_interval`: "Reminder Interval" - Time between reminders (1-480 minutes)
- `max_reminder_count`: "Maximum Reminder Count" - Limit reminders (0 = unlimited, 1-50)
- `send_resolution_notification`: "Send Resolution Notification" - Notify when resolved

**critical_notification_config Section (for blueprints with critical alerts):**
- Place immediately after `notification_config` section
- Always use icon: `mdi:bell-alert-outline`
- Title: "Critical Alert Settings"
- Include separate `critical_notification_service` (optional, falls back to standard service)
- Include separate timing settings for critical alerts:
  - `critical_reminder_interval`: Typically shorter intervals (1-30 minutes)
  - `critical_max_reminder_count`: Often unlimited (0) for safety

**notification_content_config Section:**
- Always use icon: `mdi:message-text` and collapsed: true
- Always titled "Customize Notification Content (Optional)"
- Sequence notification inputs in temporal order: initial → reminder → resolution → critical
- Always include `notification_title` before any message fields
- Group related title and message pairs together
- Use consistent naming patterns:
  - `notification_title`, `notification_message` (initial/main alerts)
  - `reminder_title`, `reminder_message` (reminder alerts)
  - `resolution_title`, `resolution_message` (resolution alerts)
  - `critical_title`, `critical_message` (critical alerts)
- All notification titles should start with relevant emojis
- Use markdown lists for placeholder documentation in descriptions
- Ensure titles and messages support the same placeholders consistently

**Placeholder Documentation Format:**
Use markdown lists in input descriptions:
```yaml
description: |
  Custom message template. Available variables:
  - `{entity}`: Entity name or friendly name
  - `{level}`: Current sensor reading
  - `{limit}`: Configured threshold value
  - `{unit}`: Unit of measurement
  - `{location}`: Device location
```

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
- Expand `threshold_config` sections by default for easier access
- Collapse `notification_content_config` and `advanced_settings` sections by default
- Use consistent icons: `mdi:tune` for threshold_config, `mdi:bell-alert` for notification_config, `mdi:bell-alert-outline` for critical_notification_config, `mdi:message-text` for notification_content_config, `mdi:cog` for advanced_settings

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
