# zotero-mcp-server
Zotero MCP Server<br>
Available tools
```
  • zotero_get_zotero_items: Get all items from Zotero
    Args:
        max_items: max number of items to return (default = 5)

  • zotero_search_zotero: Get all items from Zotero
  Args:
      query: terms to search
      max_items: (optional, default = 5) max number of items to return
      item_type: (optional, default = '') 'book', 'journalArticle', etc

  • zotero_create_item_zotero: Create a new item in your library
  Args:
    item_data (dict): Item metadata using template {'itemType': 'journalArticle', 'title': '', 'creators': [{'creatorType': 'author', 'firstName': '', 'lastName': ''}], 'abstractNote': '', 'publicationTitle': '', 'volume': '', 'issue': '', 'pages': '', 'date': '', 'series': '', 'seriesTitle': '', 'seriesText': '', 'journalAbbreviation': '', 'language': '', 'DOI': '', 'ISSN': '', 'shortTitle': '', 'url': '', 'accessDate': '', 'archive': '', 'archiveLocation': '', 'libraryCatalog': '', 'callNumber': '', 'rights': '', 'extra': '', 'tags': [], 'collections': [], 'relations': {}}

  • zotero_update_item_zotero: Create a new item in your library
  Args:
      item_key: key for zotero item
      item_data (dict): Item metadata using template {'itemType': 'journalArticle', 'title': '', 'creators': [{'creatorType': 'author', 'firstName': '', 'lastName': ''}], 'abstractNote': '', 'publicationTitle': '', 'volume': '', 'issue': '', 'pages': '', 'date': '', 'series': '', 'seriesTitle': '', 'seriesText': '', 'journalAbbreviation': '', 'language': '', 'DOI': '', 'ISSN': '', 'shortTitle': '', 'url': '', 'accessDate': '', 'archive': '', 'archiveLocation': '', 'libraryCatalog': '', 'callNumber': '', 'rights': '', 'extra': '', 'tags': [], 'collections': [], 'relations': {}}

  • zotero_delete_item_zotero: Delete an item in your library
  Args:
      item_key: the key for the zotero item

  • zotero_get_zotero_collections: Get all items from Zotero
  Args:
      max_items: max number of items to return (default = 5)

  • zotero_create_zotero_collection: Create a new collection
  Args:
      name: name of the collection
      parent_collection: (optional, default = '') name of parent collection if necessary

  • zotero_add_item_zotero_collection: Add item to collection
  Args:
      item_key: key of item
      collection_key: key of collection

  • zotero_export_zotero_library: Export the bibliography of every item
  Args:
      format: (optional, default ='bibtex')

  • zotero_export_zotero_collection: Export the bilbiography of a collection
  Args:
      collection_key: key of the collection to export
      format: (optional, default ='bibtex')
```
Usage example
```
💬 You: show me my zotero collections
🤔 Assistant:
🔧 Executing zotero_get_zotero_collections...
Here’s a quick snapshot of all the Zotero collections in your library (up to 20, which is the current total):

| Collection Key | Name      | Items | Sub‑Collections |
|-----------------|-----------|-------|-----------------|
| **UNRV6CM8**    | PAPERS    | 0     | 0 |
| **AZPEBBV9**    | ANALYSIS  | 0     | 0 |
| **BQFKVV3F**    | TEST      | 0     | 0 |
| **HDL9WF3K**    | RETOS     | 6     | 0 |
| **L79PUSCD**    | IPC       | 6     | 0 |

If you’d like to see the items inside any of these collections, just let me know the collection key (e.g., `HDL9WF3K`) and I can pull up the list for you.

💬 You: create a new item for the paper titled 'Hp spaces in several variables' by Charles Fefferman and Elias Stein
🤔 Assistant:
🔧 Executing zotero_create_item_zotero...
✅ The paper **“Hp spaces in several variables”** by Charles Fefferman and Elias Stein has been added to your Zotero library as a journal article. 
If you’d like to add more details (publication year, journal name, volume/issue, pages, DOI, etc.) or place it into a specific collection, just let me know and I’ll update the entry for you.

💬 You: add this item to the collection ANALYSIS
🤔 Assistant: 
🔧 Executing zotero_get_zotero_items...
🔧 Executing zotero_add_item_zotero_collection...
✅ The paper **“Hp spaces in several variables”** has been added to the **ANALYSIS** collection.  
If you need any further edits or want to add more metadata (e.g., journal, volume, pages, DOI), just let me know!
```
To install, clone the repo or download the zip file. It is recommended to use `uv` for dependency management, the requirements can be found in `requirements.txt`. It may be added to any LLM using Anthropic's SDK and the following configuration parameters
```json
{
  "command": "uv",
  "args": [
    "run", "--repository", "PATH/TO/REPO", "PATH/TO/REPO/zotero_mcp_server.py"
  ]
}
```
In order to access your zotero information, you need your user id and an API key. They can be configured in the `.env` file as
```env
LIBRARY_ID = "12334"
ZOTERO_API_KEY = "asdfasfas"
LIBRARY_TYPE = "user"
```
