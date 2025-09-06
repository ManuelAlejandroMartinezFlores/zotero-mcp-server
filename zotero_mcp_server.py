import os
from dotenv import load_dotenv
import logging
from typing import Any, Sequence

from zotero_manager import ZoteroBibliographyManager

load_dotenv()
LIBRARY_ID = os.getenv("LIBRARY_ID")
LIBRARY_TYPE = os.getenv("LIBRARY_TYPE")
API_KEY = os.getenv("ZOTERO_API_KEY")
    

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zotero-mcp-server")

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("zotero-mcp-server")

def format_item(item:dict) -> str:
    return f"""
Item key: {item.get('key', 'Unknown')}
Item type: {item.get('itemType', 'Unknown')}
Date: {item.get('date', 'Unknown')}
Title: {item.get('title', 'Unknown')}
Creators: {' and '.join([creator.get('firstName', '') + ' ' + creator.get('lastName', '') for creator in item.get('creators', [])])}
ISBN: {item.get('ISBN', 'Unknown')}
"""

@mcp.tool()
async def get_zotero_items(max_items:int=5) -> str:
    """Get all items from Zotero

    Args:
        max_items: max number of items to return (default = 5)
    """
    try:
        zot_manager = ZoteroBibliographyManager(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
        results = zot_manager.get_all_items()
        max_items = min(max_items, len(results))
        return ('\n' + '-'*80 + '\n').join([format_item(item.get('data', {})) for item in results[:max_items]])
    except Exception as e:
        return f"Error: {e}"
    
@mcp.tool()
async def search_zotero(query:str, max_items:int=5, item_type:str='') -> str:
    """Get all items from Zotero

    Args:
        query: terms to search
        max_items: (optional, default = 5) max number of items to return
        item_type: (optional, default = '') 'book', 'journalArticle', etc
    """
    try:
        zot_manager = ZoteroBibliographyManager(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
        results = zot_manager.search_items(query, item_type)
        max_items = min(max_items, len(results))
        return ('\n' + '-'*80 + '\n').join([format_item(item.get('data', {})) for item in results[:max_items]])
    except Exception as e:
        return f"Error: {e}"
    
@mcp.tool()
async def create_item_zotero(item_data:dict) -> str:
    """
    Create a new item in your library
    
    Args:
        item_data (dict): Item metadata using template {'itemType': 'journalArticle', 'title': '', 'creators': [{'creatorType': 'author', 'firstName': '', 'lastName': ''}], 'abstractNote': '', 'publicationTitle': '', 'volume': '', 'issue': '', 'pages': '', 'date': '', 'series': '', 'seriesTitle': '', 'seriesText': '', 'journalAbbreviation': '', 'language': '', 'DOI': '', 'ISSN': '', 'shortTitle': '', 'url': '', 'accessDate': '', 'archive': '', 'archiveLocation': '', 'libraryCatalog': '', 'callNumber': '', 'rights': '', 'extra': '', 'tags': [], 'collections': [], 'relations': {}}
    """
    try:
        zot_manager = ZoteroBibliographyManager(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
        result = zot_manager.create_item(item_data)
        if result:
            return 'Success'
        return 'Could not complete the action'
    except Exception as e:
        return f"Error: {e}"
    
@mcp.tool()
async def update_item_zotero(item_key:str, item_data:dict[str, str]) -> str:
    """
    Create a new item in your library
    
    Args:
        item_key: key for zotero item
        item_data (dict): Item metadata using template {'itemType': 'journalArticle', 'title': '', 'creators': [{'creatorType': 'author', 'firstName': '', 'lastName': ''}], 'abstractNote': '', 'publicationTitle': '', 'volume': '', 'issue': '', 'pages': '', 'date': '', 'series': '', 'seriesTitle': '', 'seriesText': '', 'journalAbbreviation': '', 'language': '', 'DOI': '', 'ISSN': '', 'shortTitle': '', 'url': '', 'accessDate': '', 'archive': '', 'archiveLocation': '', 'libraryCatalog': '', 'callNumber': '', 'rights': '', 'extra': '', 'tags': [], 'collections': [], 'relations': {}}
    """
    try:
        zot_manager = ZoteroBibliographyManager(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
        result = zot_manager.update_item(item_key, item_data)
        if result:
            return 'Success'
        return 'Could not complete the action'
    except Exception as e:
        return f"Error: {e}"
    

@mcp.tool()
async def delete_item_zotero(item_key:str) -> str:
    """
    Delete an item in your library
    
    Args:
        item_key: the key for the zotero item
    """
    try:
        zot_manager = ZoteroBibliographyManager(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
        result = zot_manager.delete_item(item_key)
        if result:
            return f'Success deleting item {item_key}'
        return 'Could not complete the action'
    except Exception as e:
        return f"Error: {e}"
    
def format_collection(collection):
    return f"""
Key: {collection.get('data', {}).get('key', 'Unknown')}
Name: {collection.get('data', {}).get('name', 'Unknown')}
Num. items: {collection.get('meta', {}).get('numItems', 'Unknown')}
Num. Collections: {collection.get('meta', {}).get('numCollections', 'Unknown')}
"""

@mcp.tool()
async def get_zotero_collections(max_items:int=5) -> str:
    """Get all items from Zotero

    Args:
        max_items: max number of items to return (default = 5)
    """
    try:
        zot_manager = ZoteroBibliographyManager(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
        results = zot_manager.get_collections()
        max_items = min(max_items, len(results))
        return ('\n' + '-'*80 + '\n').join([format_collection(item) for item in results[:max_items]])
    except Exception as e:
        return f"Error: {e}"
    

@mcp.tool()
async def create_zotero_collection(name:str, parent_collection:str='') -> str:
    """
    Create a new collection
    
    Args:
        name: name of the collection
        parent_collection: (optional, default = '') name of parent collection if necessary
    """
    try:
        zot_manager = ZoteroBibliographyManager(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
        if len(parent_collection) > 0:
            result = zot_manager.create_collection(name, parent_collection)
        else:
            result = zot_manager.create_collection(name)
        if result:
            return 'Success'
        return 'Could not complete the action'
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()   
async def add_item_zotero_collection(item_key:str, collection_key:str) -> str:
    """
    Add item to collection
    
    Args:
        item_key: key of item
        collection_key: key of collection
    """
    try:
        zot_manager = ZoteroBibliographyManager(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
        zot_manager.add_item_to_collection(item_key, collection_key)
        return 'Success'
    except Exception as e:
        return f"Error: {e}"
    
@mcp.tool()
async def export_zotero_library(format:str='bibtex') -> str:
    """
    Export the bibliography of every item
    
    Args:
        format: (optional, default ='bibtex')
    """
    try:
        zot_manager = ZoteroBibliographyManager(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
        
        return '\n'.join(zot_manager.export_library(format).entries)
    except Exception as e:
        return f"Error: {e}"
    

@mcp.tool()
async def export_zotero_collection(collection_key:str, format:str='bibtex') -> str:
    """
    Export the bilbiography of a collection
    
    Args:
        collection_key: key of the collection to export
        format: (optional, default ='bibtex')
    """
    try:
        zot_manager = ZoteroBibliographyManager(LIBRARY_ID, LIBRARY_TYPE, API_KEY)
        
        return '\n'.join(zot_manager.export_collections(collection_key, format).entries)
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
    

