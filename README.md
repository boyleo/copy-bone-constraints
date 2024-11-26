# Blender Copy Bone Constraints Addon

This Blender addon allows you to copy bone constraints from a source armature to a target armature with matching bone names. It provides options to filter bones by prefix or suffix, and to remove existing constraints before copying new ones.

## Features

- **Copy Bone Constraints:** Copy constraints from a source armature to a target armature with matching bone names.
- **Filter by Prefix/Suffix:** Filter bones by prefix or suffix in their names.
- **Remove Existing Constraints:** Option to remove existing constraints from matching bones or all bones in the target armature before copying new ones.
- **User-Friendly UI:** Simple and intuitive user interface for selecting armatures and configuring options.

## Usage

1. **Open the Addon Panel:**
   - In the 3D Viewport, go to the `Tool` tab in the UI region.
   - You should see a panel labeled "Copy Bone Constraints".

2. **Select Armatures:**
   - Use the dropdown fields to select the source and target armatures. Only armature type objects will be shown.

3. **Configure Options:**
   - **Remove Constraints from Target Bones First:** Check this option to remove constraints from matching bones in the target armature before copying new ones.
   - **Remove Constraints from All Bones:** Check this option to remove constraints from all bones in the target armature before copying. This option is a subset of the "Remove Constraints from Target Bones First" option.
   - **Filter by Prefix:** Enter a prefix to filter bones by their names.
   - **Filter by Suffix:** Enter a suffix to filter bones by their names.

4. **Copy Constraints:**
   - Click the "Copy Bone Constraints" button to copy the constraints.


## Troubleshooting

- **Armatures Not Found:** Ensure that both the source and target armatures are selected and exist in the scene.
- **Constraints Not Copied:** Check the filtering options to ensure the correct bones are being processed.
