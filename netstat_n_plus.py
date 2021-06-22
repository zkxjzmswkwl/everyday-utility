'''
Takes each foreign address from the output of netstat -n,
outputs city, region, country, and organization name for that address.
tl;dr quickly check if spooky connection exists.
'''
import requests
from time import sleep
from subprocess import check_output, CalledProcessError, STDOUT

def main():
    results = []
    already_hit = []

    output = check_output(["netstat", "-n"], stderr=STDOUT, universal_newlines=True)
    t = output.split('TCP')
    for a in t:
        a = a.split()
        ip = a[1].split(':')[0]
        
        if ip.startswith('192.168') or ip.startswith('127.0'):
            continue

        results.append(ip) 
        
    count = 0    
    for ip in results:
        if ip in already_hit:
            continue

        already_hit.append(ip)

        r = requests.get(f'http://ipinfo.io/{ip}/json')

        city = r.json().get('city')
        region = r.json().get('region')
        country = r.json().get('country')
        company = r.json().get('org')

        netstat_ano = check_output(["netstat", "-ano"], stderr=STDOUT, universal_newlines=True)
        proc_id = None
        
        if ip in netstat_ano:
            tmp = netstat_ano.split(ip)[1]
            if 'TIME_WAIT' in tmp:
                proc_id = tmp.split('TIME_WAIT')[1].split('T')[0].strip()
            if 'ESTABLISHED' in tmp:
                proc_id = tmp.split('ESTABLISHED')[1].split('T')[0].strip()
            if 'CLOSE_WAIT' in tmp:
                proc_id = tmp.split('CLOSE_WAIT')[1].split('T')[0].strip()
            if 'LISTENING' in tmp:
                proc_id = tmp.split('LISTENING')[1].split('T')[0].strip()

        nslookup = check_output(["nslookup", ip], stderr=STDOUT, universal_newlines=True)
        if 'Name' in nslookup:
            ip = ip + f"\n        * ({nslookup.split('Name:')[1].split('Address')[0].strip()})"
        

        print(f"""
        * {ip}:\n
            * ProcID         = {proc_id}\n
            * City           = {city}\n
            * Region         = {region}\n    
            * Country        = {country}\n  
            * Company        = {company}""")
        
        count = count + 1
        sleep(0.1)
        
    print(f'Total unique foreign addresses: {len(already_hit)}')
    print(f'Total individual connections:   {count}')

if __name__ == '__main__':
    main()
