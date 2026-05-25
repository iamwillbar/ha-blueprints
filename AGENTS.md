# AGENTS.md

This file provides guidance to coding agents and contributors working in this Home Assistant blueprints repository.

## Repository Overview

This repository provides high-quality, validated Home Assistant blueprints for automations, scripts, and templates. It includes automated validation, semantic versioning, and a GitHub Pages catalog for blueprint discovery and installation.

## Development Commands

### Validation

```bash
# Validate YAML syntax for a blueprint
python -c "import yaml; yaml.safe_load(open('blueprints/path/to/blueprint.yaml'))"
```

### Testing

No formal test suite is present. Validation is performed through:

- YAML syntax validation
- Home Assistant blueprint schema validation via GitHub Actions
- Manual testing in Home Assistant environments

## Architecture and Structure

### Core Structure

```text
blueprints/
├── automations/
│   ├── maintenance/     # Maintenance-related automations
│   └── safety/          # Safety and monitoring automations
├── script/              # Reusable script blueprints
└── template/            # Template blueprints
```

### Blueprint Categories

- **Safety**: Air quality monitoring, temperature monitoring, security alerts
- **Maintenance**: Equipment maintenance reminders, filter replacements

## Blueprint Development Standards

### Required Metadata Structure

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

### Input Organization Pattern

Use sectioned inputs. Sectioned inputs require Home Assistant 2024.6.0 or later.

Use this order when the sections apply:

1. **main_config**: Core configuration such as sensors, devices, and targets.
   - Use a purpose-specific icon, such as `mdi:thermometer`, `mdi:door-closed`, or `mdi:air-filter`.
   - List required sensors first.
   - Clearly mark optional sensors as optional.
2. **threshold_config**: Timing thresholds, delays, and trigger conditions.
   - Use icon: `mdi:tune`.
   - Expanded by default.
3. **notification_config**: Basic notification settings.
   - Use icon: `mdi:bell-alert`.
4. **critical_notification_config**: Critical alert settings, when applicable.
   - Use icon: `mdi:bell-alert-outline`.
5. **notification_content_config**: Notification titles and messages.
   - Use icon: `mdi:message-text`.
   - Title: "Customize Notification Content (Optional)".
   - Collapsed by default.
6. **advanced_settings**: Optional settings.
   - Use icon: `mdi:cog`.
   - Collapsed by default.

### Notification Configuration Standards

#### Core Principle: Template-Based Notifications

- Do not hardcode notification titles or messages in action sections.
- All notification content must be configurable through input templates.
- Use placeholders, such as `{entity}`, `{level}`, `{limit}`, and `{unit}`, for dynamic content.
- Templates should support multiple entities with consistent placeholder patterns.

#### `notification_config` Section

- Always use icon: `mdi:bell-alert`.
- For blueprints where notifications are optional, include a `send_notifications` boolean toggle.
- For blueprints where notifications are the primary purpose, no `send_notifications` toggle is needed.
- Always include `notification_service` with a select selector and `custom_value: true`.
- Standard notification service options:
  - `notify.notify`
  - `notify.mobile_app`
  - `notify.persistent_notification`

#### Standard Notification Timing Settings

Use these names consistently across blueprints:

- `send_notifications`: "Send Notifications" — enable or disable notifications when optional.
- `initial_notification_delay`: "Initial Notification Delay" — time before first notification, typically 0-60 minutes.
- `send_reminders`: "Send Reminder Notifications" — enable or disable reminder notifications.
- `reminder_interval`: "Reminder Interval" — time between reminders, typically 1-480 minutes.
- `max_reminder_count`: "Maximum Reminder Count" — limit reminders, where 0 means unlimited and 1-50 is the typical range.
- `send_resolution_notification`: "Send Resolution Notification" — notify when resolved.

#### `critical_notification_config` Section

Use this section for blueprints with critical alerts.

- Place it immediately after `notification_config`.
- Always use icon: `mdi:bell-alert-outline`.
- Title: "Critical Alert Settings".
- Include a separate `critical_notification_service`, optional and falling back to the standard service when unset.
- Include separate timing settings for critical alerts:
  - `critical_reminder_interval`: typically shorter intervals, such as 1-30 minutes.
  - `critical_max_reminder_count`: often unlimited (`0`) for safety.

#### `notification_content_config` Section

- Always use icon: `mdi:message-text` and `collapsed: true`.
- Always title it "Customize Notification Content (Optional)".
- Sequence notification inputs in temporal order: initial, reminder, resolution, then critical.
- Always include `notification_title` before message fields.
- Group related title and message pairs together.
- Use consistent naming patterns:
  - `notification_title`, `notification_message` for initial or main alerts.
  - `reminder_title`, `reminder_message` for reminder alerts.
  - `resolution_title`, `resolution_message` for resolution alerts.
  - `critical_title`, `critical_message` for critical alerts.
- Notification titles should start with relevant emojis.
- Use markdown lists for placeholder documentation in descriptions.
- Ensure titles and messages support the same placeholders consistently.

#### Placeholder Documentation Format

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

### Naming Conventions

- **Blueprint names**: Title case, descriptive, under 50 characters.
- **Input keys**: snake_case, such as `motion_sensor` or `delay_time`.
- **File names**: kebab-case, such as `motion-activated-light.yaml`.

### Essential Blueprint Patterns

- Use `!input` for referencing inputs.
- Define a `variables` section for commonly used values.
- Use appropriate selectors with filters for better UX.
- Provide sensible defaults for all optional inputs.
- Use `mode: single` for single-entity automations, such as one door or one sensor.
- Use `mode: parallel` only for multi-entity automations that can safely run simultaneously.
- Always include `max_exceeded: silent` to prevent log spam.
- Use `threshold_config` for timing-related settings such as delays, intervals, and thresholds.
- Expand `threshold_config` sections by default for easier access.
- Collapse `notification_content_config` and `advanced_settings` sections by default.
- Use consistent icons:
  - `mdi:tune` for `threshold_config`.
  - `mdi:bell-alert` for `notification_config`.
  - `mdi:bell-alert-outline` for `critical_notification_config`.
  - `mdi:message-text` for `notification_content_config`.
  - `mdi:cog` for `advanced_settings`.

### Home Assistant Integration

- Blueprints are designed for ESPHome integration, especially air quality sensors.
- Support standard Home Assistant notification services.
- Use domain-specific device classes, such as motion and temperature, when applicable.

### Automation Mode Selection

- **single**: Use for single-entity automations, such as one sensor or one device.
- **parallel**: Use only for multi-entity automations that can safely run concurrently.
- Always include `max_exceeded: silent`.

## Semantic Versioning

Commit messages determine version bumps:

- **Major** (`x.0.0`): `breaking change`, `breaking:`, `major:`, `!:`, `incompatible`
- **Minor** (`1.x.0`): `feat:`, `feature:`, `add:`, `new:`, `enhancement`
- **Patch** (`1.0.x`): `fix:`, `patch:`, `bug:`, `hotfix:`, `chore:`, `docs:`, `style:`

## Blueprint Quality Standards

### Validation Requirements

All blueprints must pass:

- YAML syntax validation
- Home Assistant blueprint schema compliance
- Best practice compliance checks

### User Experience Standards

- Clear, helpful descriptions with markdown formatting.
- Appropriate input selectors with domain and device class filters.
- Logical input grouping with descriptive sections.
- Sensible default values for all optional inputs.
- Recovery or clear notifications for alert-based automations.

### Critical Safety Patterns

For safety-critical blueprints, such as CO monitoring:

- Implement repeated alerts for critical conditions.
- Use appropriate alert priorities and actions.
- Provide clear action guidance in notifications.
- Include clear thresholds based on safety standards.

## Development Workflow

1. Create the blueprint in the appropriate category folder.
2. Follow naming conventions and metadata requirements.
3. Validate YAML locally before committing.
4. Use conventional commit messages for proper versioning.
5. GitHub Actions handles validation and publishing automatically.
6. Blueprints are published to the GitHub Pages catalog with import buttons.

## Important Files

- `README.md`: Repository documentation and setup instructions.
- `.github/workflows/validate-and-publish.yml`: Validation, versioning, catalog generation, and publishing workflow.
- `.github/scripts/`: Helper scripts for validation, processing, and site generation.
- Individual blueprint files contain extensive inline documentation.
