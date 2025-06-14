# 🏠 Home Assistant Blueprints

A comprehensive collection of high-quality Home Assistant blueprints with automated validation, semantic versioning, and easy installation.

## 🌟 Features

- **📋 Comprehensive Validation**: All blueprints are automatically validated for YAML syntax and Home Assistant schema compliance
- **🎯 Home Assistant YAML Support**: Full support for `!input`, `!include`, `!secret`, and `!env_var` tags
- **🔢 Semantic Versioning**: Each blueprint gets automatic version numbers based on commit history using conventional commits
- **🚀 Easy Installation**: One-click import buttons that work directly with Home Assistant
- **📚 Beautiful Catalog**: Auto-generated GitHub Pages site showcasing all blueprints
- **🔄 Automated Publishing**: GitHub Actions workflow handles everything automatically

## 🎯 Quick Start

### Browse Available Blueprints

Visit our **[Blueprint Catalog](https://YOUR_USERNAME.github.io/ha-blueprints/)** to see all available blueprints with easy import buttons.

### Install a Blueprint

1. **Easy Method**: Click the "🚀 Import to HA" button on any blueprint in our catalog
2. **Manual Method**: 
   - Copy the raw YAML URL from our GitHub Pages site
   - Go to Home Assistant → Settings → Automations & Scenes → Blueprints
   - Click "Import Blueprint" and paste the URL

### Example Import URL Format
```
https://YOUR_USERNAME.github.io/ha-blueprints/blueprints/automation/lighting/motion-activated-light.yaml
```

## 📂 Repository Structure

```
ha-blueprints/
├── .github/workflows/
│   └── validate-and-publish.yml    # GitHub Actions workflow
├── blueprints/
│   ├── automation/
│   │   ├── lighting/
│   │   │   └── motion-activated-light.yaml
│   │   └── security/
│   │       └── door-window-monitor.yaml
│   └── script/
│       └── notifications/
│           └── smart-notification-center.yaml
├── .copilot-instructions.md         # Development guidelines
└── README.md
```

## 🔧 Development Guidelines

All blueprints in this repository follow strict quality standards:

### Required Metadata
```yaml
blueprint:
  name: "Descriptive Blueprint Name"
  description: |
    Clear description of what the blueprint does.
    Include features, requirements, and usage notes.
  domain: automation|script|template
  author: "Your Name"
  homeassistant:
    min_version: "2024.6.0"
```

### Best Practices
- ✅ Use appropriate selectors for better UX
- ✅ Provide sensible default values
- ✅ Group related inputs using sections
- ✅ Include helpful descriptions
- ✅ Follow semantic versioning conventions
- ✅ Test thoroughly before submitting

See [`.copilot-instructions.md`](.copilot-instructions.md) for comprehensive development guidelines.

## 🤖 Automated Workflow

### On Pull Requests
- ✅ YAML syntax validation with Home Assistant tag support (`!input`, `!include`, `!secret`, `!env_var`)
- ✅ Home Assistant blueprint schema validation
- ✅ Duplicate name checking
- ✅ Best practice compliance

### On Main Branch Push
- ✅ All validation checks
- 🔢 Semantic version generation based on commit history
- 📦 Blueprint processing with version injection (preserves Home Assistant tags)
- 🌐 GitHub Pages site generation with import buttons
- 🚀 Automatic deployment

### Semantic Versioning Rules

Version numbers are calculated from commit messages:

- **Major** (x.0.0): `breaking change`, `breaking:`, `major:`, `!:`, `incompatible`
- **Minor** (1.x.0): `feat:`, `feature:`, `add:`, `new:`, `minor:`, `enhancement`
- **Patch** (1.0.x): `fix:`, `patch:`, `bug:`, `hotfix:`, `chore:`, `docs:`, `style:`

Example commit messages:
```bash
git commit -m "feat: add illuminance threshold to motion light blueprint"     # Minor version bump
git commit -m "fix: correct condition logic in security monitor"             # Patch version bump
git commit -m "breaking: change input structure for better organization"     # Major version bump
```

## 📋 Available Blueprints

### 💡 Lighting
- **Motion-Activated Light Control**: Smart motion-based lighting with illuminance detection
- More coming soon...

### 🔒 Security  
- **Door/Window Security Monitor**: Comprehensive security monitoring with notifications
- More coming soon...

### 📱 Scripts
- **Smart Notification Center**: Centralized notification system with multiple delivery methods
- More coming soon...

## 🤝 Contributing

We welcome contributions! Here's how to add a new blueprint:

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/ha-blueprints.git
cd ha-blueprints
```

### 2. Create Your Blueprint
- Place it in the appropriate category folder under `blueprints/`
- Follow the naming convention: `kebab-case.yaml`
- Ensure it follows our quality guidelines

### 3. Test Locally
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('blueprints/path/to/your-blueprint.yaml'))"
```

### 4. Submit Pull Request
- Use conventional commit messages
- Provide a clear description of the blueprint's functionality
- Include any special requirements or setup instructions

### 5. Automated Processing
Once merged, the GitHub Actions workflow will:
- Assign a semantic version based on your commit messages
- Validate the blueprint thoroughly
- Publish it to the catalog with import buttons

## 🛠️ Setup Instructions

### For Repository Owners

1. **Enable GitHub Pages**:
   - Go to Settings → Pages
   - Source: "GitHub Actions"

2. **Configure Repository Settings**:
   - Ensure Actions have write permissions
   - Enable "Allow GitHub Actions to create and approve pull requests"

3. **Update URLs**:
   - Replace `YOUR_USERNAME` in this README with your GitHub username
   - Update repository name if different from `ha-blueprints`

### Required Repository Structure
The workflow expects blueprints to be in the `blueprints/` directory with the following structure:
- `blueprints/automation/` - Automation blueprints
- `blueprints/script/` - Script blueprints  
- `blueprints/template/` - Template blueprints

## 🐛 Troubleshooting

### Common Issues

**Blueprint not appearing on catalog**: 
- Ensure it's in the correct `blueprints/` subdirectory
- Check that the YAML is valid
- Verify all required metadata is present

**Import button not working**:
- Confirm GitHub Pages is enabled and deployed
- Check that the blueprint passed validation
- Ensure Home Assistant can access GitHub Pages

**Version not updating**:
- Use conventional commit messages
- Ensure commits modify the blueprint file
- Check the GitHub Actions logs for errors

## 📜 License

This repository is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Home Assistant community for inspiration and best practices
- Contributors who make this project better
- GitHub for providing free hosting and automation tools

---

**Happy Automating! 🏠✨**

*Made with ❤️ for the Home Assistant community*
