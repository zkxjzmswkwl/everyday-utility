'''
Takes each foreign address from the output of netstat -n,
outputs city, region, country, and organization name for that address.
tl;dr quickly check if spooky connection exists.
'''
import requests
from subprocess import check_output, CalledProcessError, STDOUT

def main():
    results = []

    output = check_output(["netstat", "-n"], stderr=STDOUT, universal_newlines=True)
    t = output.split('TCP')
    for a in t:
        a = a.split()
        ip = a[1].split(':')[0]
        if ip.startswith('192.168') or ip.startswith('127.0'):
            continue

        results.append(ip)
    
    for ip in results:
        r = requests.get(f'http://ipinfo.io/{ip}/json')
        print(f"""
        * IP ({ip}):\n
            * City           = {r.json().get('city')}\n
            * Region         = {r.json().get('region')}\n    
            * Country        = {r.json().get('country')}\n  
            * Company        = {r.json().get('org')}""")


if __name__ == '__main__':
    main()
