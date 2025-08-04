# TBSE Body Kit - Blender Addon

A Blender addon for FFXIV character modeling and body modification. Provides tools for managing TBSE body shapes, gear, and piercings.

## Installation

### Method 1: ZIP Installation (Recommended)
1. Go to the [releases page](https://github.com/UsrBern/Kharas-Blender-Menu/releases/tag/v0.0.0) and download the latest ZIP
2. In Blender: Edit → Preferences → Add-ons → Install
3. Select the ZIP file and click "Install Add-on"
4. Enable "TBSE Body Kit" in the addon list

### Method 2: Manual Installation
1. Download the addon folder
2. Copy it to your Blender addons directory:
   - Windows: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons\`
   - macOS: `~/Library/Application Support/Blender/[version]/scripts/addons/`
   - Linux: `~/.config/blender/[version]/scripts/addons/`
3. Restart Blender and enable the addon in Preferences

## Setup

1. Open your TBSE .blend file in Blender
2. Enable the addon (if not already enabled)
3. Go to 3D Viewport → Sidebar (N key) → Body Kit tab
4. Click **"Setup Models Data"** button (required for addon to work)

## Basic Usage

### Body Management
- **Body Shape**: Choose from TBSE, Slim, Type W, Chonk, etc.
- **Visibility**: Toggle hands, feet, legs, chest on/off
- **NSFW**: Show/hide adult content

### Gear System
- **Add Gear**: Select mesh objects → click "Add to [Body Part] Gear"
- **Remove Gear**: Select from list → click "Remove"
- **Import FBX**: Use the FBX import button for FFXIV-optimized settings

### Piercings
- **Chest Piercings**: Toggle nipple rings, navel piercings
- **AMAB Piercings**: Additional piercing options

## Requirements

- Blender 2.80+
- TBSE model collection (.blend file)
- The included "tbse models" data file

## Credits

- **Original Script**: Crow
- **Refactor**: UsrBern
- **TBSE System**: Tsar and community contributors