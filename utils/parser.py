import xml.etree.ElementTree as ET

def parse_nmap_xml(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        result = []
        for host in root.findall('host'):
            addr = host.find('address').get('addr')
            ports = []
            for p in host.findall('.//port'):
                ports.append({
                    'port': p.get('portid'),
                    'state': p.find('state').get('state'),
                    'service': (p.find('service').get('name')
                                if p.find('service') is not None else "")
                })
            result.append({'addr': addr, 'ports': ports})
        return result
    except:
        return []
