from gdstorage.storage import GoogleDriveStorage

# Modification to google drive storage for embedding images
class ModifiedGoogleDriveStorage(GoogleDriveStorage):
    # Manipulate the URL for embedding the image
    def url(self, name):
        id = super().url(name)
        suffix = '&export=download'
        prefix = 'id='
        
        start_idx = id.find(prefix)
        if start_idx is None:
            start_idx = 0
        else:
            start_idx += len(prefix)
        
        end_idx = id.find(suffix)
        if end_idx is None:
            end_idx = len(id)
        
        id = id[start_idx:end_idx]
        return f'https://lh3.google.com/u/0/d/{id}'