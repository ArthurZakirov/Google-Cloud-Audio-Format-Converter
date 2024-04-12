def list_files_and_folders_in_root(service):
    query = "'root' in parents and trashed=false"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])
    
    # Initialize an empty list to hold the information about files and folders
    files_and_folders = []

    if not items:
        print('No files found in My Drive.')
    else:
        # Go through each item and add the details to the list
        for item in items:
            files_and_folders.append({'name': item['name'], 'id': item['id'], 'type': item['mimeType']})
            
    return files_and_folders

def get_folder_id_by_path(service, path):
    if path == '/':
        return 'root'
    elif not path.startswith('/'):
        raise ValueError("Path must start with '/'.")

    folder_id = 'root'
    parts = path.strip('/').split('/')
    
    for part in parts:
        response = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name='{part}' and '{folder_id}' in parents and trashed=false",
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name)').execute()
        files = response.get('files', [])
        
        if not files:
            raise ValueError(f"No folder with name '{part}'")
        folder_id = files[0]['id']
        
    return folder_id

def list_files_in_directory(service, path):
    folder_id = get_folder_id_by_path(service, path)
    query = f"'{folder_id}' in parents and trashed=false"
    response = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
    
    items = response.get('files', [])
    files_and_folders = [{'name': item['name'], 'id': item['id'], 'mimeType': item['mimeType']} for item in items]
    
    return files_and_folders