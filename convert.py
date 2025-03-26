import argparse
from pathlib import Path
import subprocess
import os 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a text file to a different format')
    parser.add_argument('--input_path', help='The file to convert', type = str)
    parser.add_argument('--output_path', help='The output directory', type = str, default= "3DObject/")
    parser.add_argument('--gpus', help='The device to use', type = int, nargs = "+", default=[2,3])
    parser.add_argument('--config', type=str, help='Path to config file.', default='InstantMesh/configs/instant-mesh-base.yaml')
    parser.add_argument('--diffusion_steps', type=int, default=75, help='Denoising Sampling steps.')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for sampling.')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale of generated object.')
    parser.add_argument('--distance', type=float, default=4.5, help='Render distance.')
    parser.add_argument('--view', type=int, default=6, choices=[4, 6], help='Number of input views.')
    parser.add_argument('--no_rembg', action='store_true', help='Do not remove input background.')
    parser.add_argument('--export_texmap', action='store_false', help='Export a mesh with texture map.')
    parser.add_argument('--save_video', action='store_true', help='Save a circular-view video.')
    args = parser.parse_args()

    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = ",".join([str(gpu) for gpu in args.gpus])

    Path(args.output_path).mkdir(parents=True, exist_ok=True) 
    
    
    subprocess.run([
        '.venv/bin/python', 'InstantMesh/run.py',
        "--input_path", str(args.input_path),
        '--output_path', args.output_path,
        '--config', args.config,
        '--diffusion_steps', str(args.diffusion_steps),
        '--seed', str(args.seed),
        '--scale', str(args.scale),
        '--distance', str(args.distance),
        '--view', str(args.view),
        '--export_texmap', 
        '--no_rembg',
    ])

    # Move the files in the meshes folder to output_path folder
     
    for file in Path("3DObject").glob(f"*/*/meshes/*"):
        os.system(f"mv {file} {args.output_path}")
    
    # Delete the other folders
    for folder in Path("3DObject").glob(f"*/*/"):
        # If is a directory, delete it.
        if folder.is_dir():
            os.system(f"rm -r {folder}")
        
    print("finished")
    