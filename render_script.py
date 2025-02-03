import bpy
import os

#not necessary --------------
def print_colored(text, color_code):
    """Print text with color"""
    print(f"\033[{color_code}m{text}\033[0m")
#not necessary --------------

def render_animation(blend_file_path):
    try:
        # Print "Starting rendering..." in green
        print_colored("Starting rendering...", 32)

        # Open the specified Blender file
        bpy.ops.wm.open_mainfile(filepath=blend_file_path)

        # Ensure the output path is set in the .blend file
        output_path = bpy.context.scene.render.filepath
        if not output_path:
            raise ValueError("Output path is not set in the Blender file.")

        # If no output path is set, set it to the current directory with frame numbering
        if not os.path.isdir(os.path.dirname(output_path)):
            output_path = os.path.join(os.path.dirname(blend_file_path), "rendered_frames", "frame_####.png")
            bpy.context.scene.render.filepath = output_path

        # Frame details
        total_frames = bpy.context.scene.frame_end - bpy.context.scene.frame_start + 1

        # Render the animation
        bpy.ops.render.render(animation=True)

        # Print progress in the format: "Rendering X/Y frames"
        print(f"\033[32mRendering completed! {total_frames} frames rendered.\033[0m")  # Green text for progress
        print_colored(f"Output saved to: {os.path.dirname(output_path)}", 32)

    except Exception as e:
        # Print errors in red
        print_colored(f"Error occurred: {e}", 91)  # Red text for errors
      

if __name__ == "__main__":
    # Ask the user for the .blend file path
    blend_file_path = input("\033[33mEnter your .blend file path: \033[0m").strip()
    #blend_file_path = input("\033[33mEnter your .blend file path: \033[0m").strip()

    # Validate the file path
    if not os.path.exists(blend_file_path):
        print_colored("Error: The file does not exist. Please provide a valid .blend file path.", 91)
        exit(1)

    render_animation(blend_file_path)
