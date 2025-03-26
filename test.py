import subprocess   
import os 
if __name__ == '__main__':
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = "2,3"
    # Take the chair and compute the 3d object for diffusion_step from 10 to 150 and see the differences (compute videos)
    for i in range(10, 151, 10):
        print(f"Computing for diffusion_step = {i}")
        subprocess.run(['.venv/bin/python', "convert.py", "--input_path", "chair.png", "--output_path", f".temps/diff_{i}.", "--diffusion_step", str(i), "--save_video", "--export_texmap"])