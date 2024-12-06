## Instructions to run the code

1. Clone the repository
2. Set up the virtual environment
3. Install the requirements
4. Login to azure using the command `az login`
5. To extract asset attributes for up to five Collections, run the command `python3 get_assets_for_n_collections.py <purview-account-name>` where `<purview-account-name>` is the name of the purview account.
6. To extract asset attributes for a specific Collection, run the command `python3 get_assets_for_one_collections.py <purview-account-name> <collection-name>` where `<purview-account-name>` is the name of the purview account and `<collection-name>` is the CollectionId of the collection.
