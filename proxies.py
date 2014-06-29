
"""
A function for reading a list of free proxy servers 
from a file, where each line is of the format:

host:port

and producing a dict for use by pycurl (unlike
user agents, the actual list of free prxoy servers
is too variable and unreliable to check into 
source code).

"""

import os.path

def get_proxies (proxy_list, folder='/tmp'):
    """Read the proxy list file and produce a
    list of proxy dicts for each valid line"""

    proxies = []

    try:
        f = open(os.path.join(folder, proxy_list), 'r')
        data = f.read()
        f.close()
        for line in data.splitlines():
            parts = line.split(':')
            try:
                proxies.append({'host': parts[0],
                                'port': int(parts[1])})
            except (IndexError, ValueError):
                pass
    except IOError:
        pass

    return proxies
