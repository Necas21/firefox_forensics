import sqlite3
import re
import os
import argparse
import sys


# Get history of downloaded files
# Downloads database location: ~/.mozilla/firefox/m2hdptz3.default-release/places.sqlite
def get_downloads(download_db):
	conn = sqlite3.connect(download_db)
	c = conn.cursor()
	c.execute("SELECT content, dateTime(dateAdded/1000000, 'unixepoch'), url FROM moz_annos INNER JOIN moz_places ON moz_annos.place_id = moz_places.id;")
	print("[*] --- Files Downloaded ---")

	for row in c:
		file_name = row[0]
		date = row[1]
		url = row[2]
		print(f"[+] On [{date}] Downloaded File {file_name} from {url}")

	conn.close()


# Get users browser cookies
# Cookies database location: ~/.mozilla/firefox/m2hdptz3.default-release/cookies.sqlite
def get_cookies(cookies_db):
	conn = sqlite3.connect(cookies_db)
	c = conn.cursor()
	c.execute("SELECT name, value, host FROM moz_cookies;")
	print("[*] --- Cookies ---")

	for row in c:
		name = row[0]
		value = row[1]
		host = row[2]
		print(f"[+] Host: {host} | Cookie: {name} | Value: {value}")

	conn.close()


# Get browser history
# History database location: ~/.mozilla/firefox/m2hdptz3.default-release/places.sqlite
def get_history(history_db):
	conn = sqlite3.connect(history_db)
	c = conn.cursor()
	c.execute("SELECT url, dateTime(visit_date/1000000, 'unixepoch') FROM moz_places INNER JOIN moz_historyvisits ON moz_places.id = moz_historyvisits.place_id;")
	print("[*] --- History ---")

	for row in c:
		url = row[0]
		visit_date = row[1]
		print(f"[+] On [{visit_date}] visited: {url}")

	conn.close()


# Get the Google searches from the users history
# History database location: ~/.mozilla/firefox/m2hdptz3.default-release/places.sqlite
def get_google_search(history_db):
	conn = sqlite3.connect(history_db)
	c = conn.cursor()
	c.execute("SELECT url, dateTime(visit_date/1000000, 'unixepoch') FROM moz_places INNER JOIN moz_historyvisits ON moz_places.id = moz_historyvisits.place_id;")
	print("[*] --- Google Searches ---")

	for row in c:
		url = row[0]
		visit_date = row[1]

		if "google" in url.lower():
			r = re.findall(r"&q=.*", url)
			if r:
				search = r[0].replace("&q=", "").replace("+", " ").split("&")[0]
				print(f"[+] On [{visit_date}] Googled for: {search}")

	conn.close()	


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="path", help="Specify the path to the Firefox SQLite databases.")

    if len(sys.argv) != 3:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()
    path = args.path
    places_db = os.path.join(path, "places.sqlite")
    cookies_db = os.path.join(path, "cookies.sqlite")
    get_downloads(places_db)
    get_cookies(cookies_db)
    get_history(places_db)
    get_google_search(places_db)



if __name__ == "__main__":
	main()