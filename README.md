# TBSE Body Kit - Blender Addon

A Blender addon for FFXIV character modeling and body modification. This addon provides comprehensive tools for managing TBSE (The Body Shape Editor) body kits, gear, piercings, and shape keys within Blender.

## Overview

TBSE Body Kit is a refactor of Crow's original script, mainly focusing on modularity and maintainability. The addon specializes in FFXIV modding workflows, providing seamless integration with TBSE Upscale Kits and multiple body types.

## Features

### Body Management
- **Multiple Body Types**: Support for standard, XL, and Chonk body shapes
- **Shape Key Control**: Advanced shape key manipulation for body customization
- **Leg Shape Toggle**: Switch between different leg configurations
- **Visibility Controls**: Fine-grained control over body part visibility

### Gear System
- **Dynamic Gear Lists**: Manage chest, leg, hand, and feet gear collections
- **FBX Import/Export**: Streamlined workflow for importing and exporting gear models
- **Batch Operations**: Efficient batch processing for multiple gear items
- **Smart Naming**: Automatic model naming based on gear configurations

### Genital and Piercing Support
- **AMAB/AFAB Options**: Complete genital model management with multiple types
- **Piercing Systems**: Comprehensive piercing support for chest and AMAB configurations
- **BPF Integration**: Body Positive Female model support
- **NSFW Toggle**: Centralized adult content visibility control

### Advanced Features
- **Bone Layer Management**: Control visibility of different bone layers
- **Driver System**: Automated shape key drivers for dynamic body adjustments
- **Performance Optimization**: Efficient model loading and visibility management
- **Error Handling**: Robust error handling and user feedback

## Installation

1. Download the addon files
2. Place the entire folder in your Blender addons directory:
   - Windows: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons\`
   - macOS: `~/Library/Application Support/Blender/[version]/scripts/addons/`
   - Linux: `~/.config/blender/[version]/scripts/addons/`
3. Open Blender and go to Edit > Preferences > Add-ons
4. Search for "TBSE Body Kit" and enable the addon
5. The addon panel will appear in the 3D Viewport sidebar under "Body Kit"

## Requirements

- **Blender**: Version 2.80 or higher
- **TBSE Models**: Compatible TBSE model collection
- **JSON Configuration**: Properly configured model dictionary (included)

## Usage

### Basic Workflow

1. **Load TBSE Models**: Import your TBSE model collection into Blender
2. **Configure Body Type**: Select your desired body shape (Standard/XL/Chonk)
3. **Manage Visibility**: Use toggle controls to show/hide body parts
4. **Add Gear**: Import and manage gear items using the gear lists
5. **Apply Shape Keys**: Use the shape key controls for body customization

### Panel Location

The addon interface is located in:
**3D Viewport > Sidebar (N key) > Body Kit Tab**

### Key Controls

- **Body Toggles**: Show/hide hands, feet, legs, and other body parts
- **Gear Management**: Add, remove, and toggle gear visibility
- **Shape Controls**: Adjust body proportions using shape keys
- **NSFW Options**: Control adult content visibility
- **Bone Layers**: Manage skeleton visibility for rigging

## Configuration

The addon uses a JSON-based configuration system to manage model relationships and naming conventions. The model dictionary is automatically loaded and can be customized for different TBSE model collections.

### Model Groups

- **Body Parts**: hands, feet, legs, genitals
- **Gear Categories**: chest, legs, hands, feet
- **Piercings**: chest, AMAB-specific
- **Special Models**: BPF, NSFW variants