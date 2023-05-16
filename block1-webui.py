import threading
import time
from pydrive.auth import GoogleAuth
from google.colab import drive
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
import glob
import os
import datetime

# Set the ID of the destination folder in Google Drive
folder_id = '1hXC9J55AUnwnz0_1-p_8wjIvMELmM42G'  # ID of the destination folder in Google Drive

# Authenticate and create GoogleDrive instance
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)


# Get the current date
current_date = datetime.date.today().strftime('%Y-%m-%d')

# Set the path for the processed files text file
processed_files_path = '/content/processed_files.txt'

# Create the processed files text file if it doesn't exist
if not os.path.exists(processed_files_path):
    with open(processed_files_path, 'w') as file:
        pass

def load_processed_files():
    processed_files = set()
    if os.path.exists(processed_files_path):
        with open(processed_files_path, 'r') as file:
            for line in file:
                processed_files.add(line.strip())
    return processed_files

def save_processed_files(processed_files):
    with open(processed_files_path, 'w') as file:
        for file_path in processed_files:
            file.write(file_path + '\n')

processed_files = load_processed_files()

############################################### THREADING ##########################################


## UPLOAD IMAGES TO KURUSHIMI GDRIVE (MUST SIGNED IN FIRST) = FOLDER > AI OUTPUTS FOLDER
# Check if the folder with the current date already exists
existing_folders = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

folder_count = 1
folder_name = f'txt2img > {current_date} = {folder_count}'

while True:
    match_found = False

    for folder in existing_folders:
        if folder['title'] == folder_name:
            folder_count += 1
            folder_name = f'{current_date} = {folder_count}'
            match_found = True
            break

    if not match_found:
        break

# Create the folder in Google Drive
folder_metadata = {'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [{'id': folder_id}]}
folder = drive.CreateFile(folder_metadata)
folder.Upload()

# Get the ID of the created folder
created_folder_id = folder['id']
print(f"Folder created successfully. ID: {created_folder_id}")

def upload_files():
    while True:
        # Construct the file path pattern
        file_path_pattern = f'/content/sd-webui/outputs/txt2img-images/{current_date}/*.png'
        #file_path_pattern = f'/content/test_folders/*.png'

        # Retrieve file paths matching the pattern
        file_paths = glob.glob(file_path_pattern)

        for file_path in file_paths:
            # Check if the file has already been processed
            if file_path in processed_files:
                continue

            # Create a file instance
            file_drive = drive.CreateFile({'title': os.path.basename(file_path), 'parents': [{'id': created_folder_id}]})

            # Set the content of the file
            file_drive.SetContentFile(file_path)

            # Upload the file to Google Drive
            file_drive.Upload()

            # Print the link to the uploaded file in Google Drive
            print('File uploaded successfully. Link:', file_drive['alternateLink'])

            # Add the file to the processed set
            processed_files.add(file_path)

        # Save the processed files to the text file
        save_processed_files(processed_files)

        # Sleep for 10 seconds before checking for new files again
        time.sleep(10)


# Create a thread for file upload
upload_thread = threading.Thread(target=upload_files)
#upload_thread.start()



######################################################## END OF THREADING ################################################################



!curl -Lo memfix.zip https://github.com/nolanaatama/sd-webui/raw/main/memfix.zip
!unzip /content/memfix.zip
!apt install -qq libunwind8-dev
!dpkg -i *.deb
%env LD_PRELOAD=libtcmalloc.so
!rm *
!pip install --upgrade fastapi==0.90.1
!pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 torchtext==0.14.1 torchdata==0.5.1 --extra-index-url https://download.pytorch.org/whl/cu116 -U


!curl -Lo sd-webui.zip https://huggingface.co/nolanaatama/webui/resolve/main/sd-webui.zip
!unzip /content/sd-webui.zip


!git clone https://github.com/nolanaatama/sd-webui-tunnels /content/sd-webui/extensions/sd-webui-tunnels
!git clone https://github.com/Mikubill/sd-webui-controlnet /content/sd-webui/extensions/sd-webui-controlnet
!git clone https://github.com/fkunn1326/openpose-editor /content/sd-webui/extensions/openpose-editor
!git clone https://github.com/hnmr293/posex /content/sd-webui/extensions/posex
!git clone https://github.com/DominikDoom/a1111-sd-webui-tagcomplete /content/sd-webui/extensions/a1111-sd-webui-tagcomplete
!git clone https://github.com/hako-mikan/sd-webui-supermerger /content/sd-webui/extensions/sd-webui-supermerger
!git clone https://github.com/Delteuz/sd-webui-wd14-tagger-copyonly /content/sd-webui/extensions/sd-webui-wd14-tagger-copyonly


!curl -Lo /content/sd-webui/extensions/sd-webui-images-browser.zip https://huggingface.co/nolanaatama/webui/resolve/main/sd-webui-images-browser.zip
%cd /content/sd-webui/extensions
!unzip /content/sd-webui/extensions/sd-webui-images-browser.zip
%cd /content


# ControlNet

!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11e_sd15_ip2p.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11e_sd15_ip2p_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11e_sd15_shuffle.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11e_sd15_shuffle_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11p_sd15_canny.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11p_sd15_canny_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11f1p_sd15_depth.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11p_sd15_depth_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11p_sd15_inpaint.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11p_sd15_inpaint_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11p_sd15_lineart.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11p_sd15_lineart_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11p_sd15_mlsd.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11p_sd15_mlsd_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11p_sd15_normalbae.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11p_sd15_normalbae_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11p_sd15_openpose.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11p_sd15_openpose_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11p_sd15_scribble.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11p_sd15_scribble_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11p_sd15_seg.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11p_sd15_seg_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11p_sd15_softedge.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11p_sd15_softedge_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11p_sd15s2_lineart_anime.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11p_sd15s2_lineart_anime_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/control_v11u_sd15_tile.safetensors https://huggingface.co/nolanaatama/models/resolve/main/control_v11u_sd15_tile_fp16.safetensors
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/t2iadapter_canny_sd14v1.pth https://huggingface.co/nolanaatama/models/resolve/main/t2iadapter_canny_sd14v1.pth
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/t2iadapter_color_sd14v1.pth https://huggingface.co/nolanaatama/models/resolve/main/t2iadapter_color_sd14v1.pth
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/t2iadapter_depth_sd14v1.pth https://huggingface.co/nolanaatama/models/resolve/main/t2iadapter_depth_sd14v1.pth
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/t2iadapter_keypose_sd14v1.pth https://huggingface.co/nolanaatama/models/resolve/main/t2iadapter_keypose_sd14v1.pth
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/t2iadapter_openpose_sd14v1.pth https://huggingface.co/nolanaatama/models/resolve/main/t2iadapter_openpose_sd14v1.pth
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/t2iadapter_seg_sd14v1.pth https://huggingface.co/nolanaatama/models/resolve/main/t2iadapter_seg_sd14v1.pth
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/t2iadapter_sketch_sd14v1.pth https://huggingface.co/nolanaatama/models/resolve/main/t2iadapter_sketch_sd14v1.pth
!curl -Lo /content/sd-webui/extensions/sd-webui-controlnet/models/t2iadapter_style_sd14v1.pth https://huggingface.co/nolanaatama/models/resolve/main/t2iadapter_style_sd14v1.pth


import shutil
shutil.rmtree('/content/sd-webui/embeddings')
!rm sd-webui.zip
!rm sd-webui-images-browser.zip
%cd /content/sd-webui
!git clone https://huggingface.co/nolanaatama/embeddings
%cd /content/sd-webui/models
!git clone https://huggingface.co/nolanaatama/ESRGAN
%cd /content/sd-webui
