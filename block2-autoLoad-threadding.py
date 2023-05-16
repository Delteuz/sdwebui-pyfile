
#------------------------------------------------- START OF THREADING // OBSERVE OUTPUT FOLDER -----------------------------
# Check if the folder with the current date already exists
existing_folders2 = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

folder_count2 = 1
folder_name2 = f'batch output > {current_date} = {folder_count2}'

while True:
    match_found = False

    for folder in existing_folders2:
        if folder['title'] == folder_name2:
            folder_count2 += 1
            folder_name2 = f'{current_date} = {folder_count2}'
            match_found = True
            break

    if not match_found:
        break

# Create the folder in Google Drive
folder_metadata = {'title': folder_name2, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [{'id': folder_id}]}
folder = drive.CreateFile(folder_metadata)
folder.Upload()

# Get the ID of the created folder
created_folder_id2 = folder['id']
print(f"Folder created successfully. ID: {created_folder_id2}")

def upload_files2():
    while True:
        # Construct the file path pattern
        file_path_pattern2 = f'/content/output/*.png'
        

        # Retrieve file paths matching the pattern
        file_paths2 = glob.glob(file_path_pattern2)

        for file_path2 in file_paths2:
            # Check if the file has already been processed
            if file_path2 in processed_files:
                continue

            # Create a file instance
            file_drive = drive.CreateFile({'title': os.path.basename(file_path2), 'parents': [{'id': created_folder_id2}]})

            # Set the content of the file
            file_drive.SetContentFile(file_path2)

            # Upload the file to Google Drive
            file_drive.Upload()

            # Print the link to the uploaded file in Google Drive
            print('File uploaded successfully. Link:', file_drive['alternateLink'])

            # Add the file to the processed set
            processed_files.add(file_path2)

        # Save the processed files to the text file
        save_processed_files(processed_files)

        # Sleep for 10 seconds before checking for new files again
        time.sleep(10)


# Create a thread for file upload
upload_thread2 = threading.Thread(target=upload_files2)
#upload_thread2.start()
#------------------------------------------------- END OF THREADING // OBSERVE OUTPUT FOLDER -----------------------------






# ---------------------------------------------------- LAUNCH THE WEB UI -------------------------------------
upload_thread.start()
upload_thread2.start()
