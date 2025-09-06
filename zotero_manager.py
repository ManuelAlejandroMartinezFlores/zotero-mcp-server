from pyzotero import zotero
from dotenv import load_dotenv
import os

class ZoteroBibliographyManager:
    def __init__(self, library_id, library_type, api_key):
        """
        Initialize Zotero API connection
        
        Args:
            library_id (str): Your Zotero library ID
            library_type (str): 'user' or 'group'
            api_key (str): Your Zotero API key
        """
        self.zot = zotero.Zotero(library_id, library_type, api_key)
        
    def get_all_items(self):
        """Retrieve all items from your library"""
        items = self.zot.everything(self.zot.items())
        return items
    
    def search_items(self, query:str, item_type:str='', tag:str=''):
        """
        Search for items in your library
        
        Args:
            query (str): Search query
            item_type (str): Filter by item type (e.g., 'book', 'journalArticle')
            tag (str): Filter by tag
        """
        params = {'q': query}
        if item_type != '':
            params['itemType'] = item_type
        if tag != '':
            params['tag'] = tag
            
        items = self.zot.items(**params)
        return items
    
    def create_item(self, item_data):
        """
        Create a new item in your library
        
        Args:
            item_data (dict): Item metadata using template {'itemType': 'journalArticle', 'title': '', 'creators': [{'creatorType': 'author', 'firstName': '', 'lastName': ''}], 'abstractNote': '', 'publicationTitle': '', 'volume': '', 'issue': '', 'pages': '', 'date': '', 'series': '', 'seriesTitle': '', 'seriesText': '', 'journalAbbreviation': '', 'language': '', 'DOI': '', 'ISSN': '', 'shortTitle': '', 'url': '', 'accessDate': '', 'archive': '', 'archiveLocation': '', 'libraryCatalog': '', 'callNumber': '', 'rights': '', 'extra': '', 'tags': [], 'collections': [], 'relations': {}}
        """
        # Get the item template first
        template = self.zot.item_template(item_data.get('itemType', 'journalArticle'))
        
        # Update template with provided data
        for key, value in item_data.items():
            if key in template:
                template[key] = value
        
        # Create the item
        resp = self.zot.create_items([template])
        if resp['success']:
            return True
        else:
            return False
    
    
    def delete_item(self, item_key):
        """Delete an item from your library"""
        self.zot.delete_item(self.zot.item(item_key))
        return True
    
    def get_collections(self):
        """Get all collections in your library"""
        collections = self.zot.collections()
        return collections
    
    def create_collection(self, name, parent_collection=None):
        """Create a new collection"""
        template = {}
        template['name'] = name
        
        if parent_collection:
            template['parentCollection'] = parent_collection
        
        resp = self.zot.create_collections([template])
        if resp['success']:
            return True
        return False
    
    def add_item_to_collection(self, item_key, collection_key):
        """Add an item to a collection"""
        self.zot.addto_collection(collection_key, self.zot.item(item_key))
    
    
    def export_library(self, format='bibtex'):
        """
        Export entire library in specified format
        
        Args:
            format (str): Export format ('bibtex', 'ris', 'refer', 'rdf_bibliontology')
        """
        # Get all items
        items = self.get_all_items()
        item_keys = [item['key'] for item in items]
        
        # Export
        export_data = self.zot.items(itemKey=','.join(item_keys), format=format)
        
        return export_data
    
    def export_collections(self, collection_key, format='bibtex'):
        items = self.zot.collection_items(collection_key)
        item_keys = [item['key'] for item in items]
        
        # Export
        export_data = self.zot.items(itemKey=','.join(item_keys), format=format)
        
        return export_data



# Example usage
def main():
    # Replace with your actual credentials
    load_dotenv()
    LIBRARY_ID = os.getenv("LIBRARY_ID")
    LIBRARY_TYPE = "user"  # or "group"
    API_KEY = os.getenv("ZOTERO_API_KEY")
    
    # Initialize the manager
    zot_manager = ZoteroBibliographyManager(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
    
    # Example operations
    
    # 1. Get all items
    print(dir(zot_manager.export_library()))
    print((zot_manager.export_collections('HDL9WF3K').entries))

if __name__ == "__main__":
    main()