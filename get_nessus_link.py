#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# Source: https://gist.github.com/parly/a62d3f69abab8a16e878134d610d8cdc

# To install the prerequisites, use the command below:
#   pacman -S python python-beautifulsoup4 python-requests

import json
import hashlib
import os
from bs4 import BeautifulSoup
import requests


def main():
    data = get_json()
    url = None
    for download in data['props']['pageProps']['page']['downloads']:
        filename = download['file']
        if filename.endswith('-fc34.x86_64.rpm'):
            url = f'https://www.tenable.com/downloads/api/v1/public/pages/nessus-agents/downloads/{download["id"]}/download?i_agree_to_tenable_license_agreement=true'
            print(f'Downloading: {filename}')
            r = requests.get(url, allow_redirects=True)

            with open(filename, 'wb') as bfile:
                _f = bfile.write(r.content)
            
            with open(filename, 'rb') as bfile:
                blake_hash_agent = hashlib.blake2b()
                for chunk in iter(lambda: bfile.read(4096), b""):
                    blake_hash_agent.update(chunk)

            with open('LICENSE', 'rb') as bfile:
                blake_hash_license = hashlib.blake2b()
                for chunk in iter(lambda: bfile.read(4096), b""):
                    blake_hash_license.update(chunk)
            
            os.remove(filename)
            
            break

    if url is not None:
        print(f'\nFile: {filename}')
        print(f'URL: {url}')
        print(f"\nb2sums=('{blake_hash_agent.hexdigest()}'\n\t'{blake_hash_license.hexdigest()}')\n")



    else:
        print('Cannot find a download link!')


def get_json():
    res = requests.get('https://www.tenable.com/downloads/nessus-agents')
    soup = BeautifulSoup(res.text, 'html.parser')
    tag = soup.find(id='__NEXT_DATA__')
    return json.loads(tag.string)



if __name__ == '__main__':
    main()
