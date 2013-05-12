#!/usr/bin/env python

"""
Scrape the PGA tour's official data endpoint.
"""

import os
import lxml.html as lh
import requests as req


headers = {
    "User-Agent": "Mozilla/5.0 (ESPN) AppleWebKit/535.30 (KHTML, like Gecko)",
    "Referer": "http://www.pgatour.com"
}


def scrape_stats(year):
    """Scrape PGA JSON stats data for a given year."""
    print year
    url = "http://www.pgatour.com/data/r/stats/{0}/".format(year)
    text = req.get(url, headers=headers).text
    html = lh.fromstring(text)
    links = html.cssselect("td > a")
    for link in links:
        href = link.attrib["href"]
        if href.endswith("json"):
            endpoint = url + href
            print "\t {0}".format(endpoint)
            data = req.get(endpoint, headers=headers).text
            # Check the path is already on disk
            disk_path = "data/{0}".format(year)
            if not os.path.exists(disk_path):
                os.makedirs(disk_path)
            # Save the JSON data to disk
            file_name = "data/{0}/{1}".format(year, href)
            with open(file_name, "w") as f:
                f.write(data)


def find_tourneys():
    """Find PGA tournaments."""
    endpoints = []
    url = "http://www.pgatour.com/data/r/"
    text = req.get(url, headers=headers).text
    html = lh.fromstring(text)
    links = html.cssselect("td > a")
    for link in links:
        href = link.attrib["href"]
        if href.strip("/").isdigit():
            tournament = href.strip("/")
            endpoints.append(tournament)
    return endpoints


def scrape_tourney(tournament):
    """Scrape a given tournament."""
    print tournament
    url = "http://www.pgatour.com/data/r/{0}/".format(tournament)
    text = req.get(url, headers=headers).text
    html = lh.fromstring(text)
    links = html.cssselect("td > a")
    for link in links:
        href = link.attrib["href"]
        if href.endswith("json"):
            endpoint = url + href
            print "\t {0}".format(endpoint)
            data = req.get(endpoint, headers=headers).text
            # Make sure we have a place to save the data
            disk_path = "data/tournaments/{0}".format(tournament)
            if not os.path.exists(disk_path):
                os.makedirs(disk_path)
            # Save the data to disk
            file_name = "data/tournaments/{0}/{1}".format(tournament, href)
            with open(file_name, "w") as f:
                f.write(data)


def main():
    for tournament in find_tourneys():
        scrape_tourney(tournament)


if __name__ == '__main__':
    main()
