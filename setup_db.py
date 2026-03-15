import urllib.request
import os

"""
The Chinook database is a sample music store database. Here's what it contains:

The catalog: Artist → Album → Track form the core music library, with Genre and MediaType
classifying each track (e.g., rock, jazz / MP3, AAC).

The business: Customer buys music, generating Invoice and InvoiceLine records — essentially the
store's sales transactions.

The staff: Employee holds the store's employee records, including a self-referencing hierarchy
(managers and their reports).

Playlists: Playlist and PlaylistTrack track curated collections of songs.

It's modeled after a digital music retailer (think early iTunes), and is widely used as a
learning/demo database because it covers realistic relationships like sales, inventory,
and org structure in a compact, clean dataset.
"""


def download_chinook():
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
    db_name = "chinook.db"

    if not os.path.exists(db_name):
        print("Downloading Chinook database...")
        urllib.request.urlretrieve(url, db_name)
        print("Download complete!")
    else:
        print("chinook.db already exists.")


if __name__ == "__main__":
    download_chinook()
