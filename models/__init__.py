#!/usr/bin/python3
"""
This script initializes a storage engine based on the environment variable 'HBNB_TYPE_STORAGE'.
If 'HBNB_TYPE_STORAGE' is set to 'db', a database storage engine (DBStorage) is initialized.
Otherwise, a file storage engine (FileStorage) is initialized.
"""

from os import getenv

def initialize_storage():
    """
    Initializes a storage engine based on the value of the 'HBNB_TYPE_STORAGE' environment variable.
    """
    storage_type = getenv('HBNB_TYPE_STORAGE')
    
    if storage_type == 'db':
        from models.engine.db_storage import DBStorage
        storage_engine = DBStorage()
    else:
        from models.engine.file_storage import FileStorage
        storage_engine = FileStorage()
    
    storage_engine.reload()
    return storage_engine

if __name__ == "__main__":
    storage_instance = initialize_storage()
