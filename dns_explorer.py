import dns.resolver

def get_dns_records(url):
    result = {
        'url': url,
        'ip_address': None,
        'hostname': None,
        'records': {}
    }

    try:
        # Resolution of IP address
        answers = dns.resolver.resolve(url, 'A')
        ip_addresses = [rdata.address for rdata in answers]
        result['ip_address'] = ip_addresses[0] if ip_addresses else None

        # Primary hostname resolution (PTR)
        try:
            answers = dns.resolver.resolve(url, 'PTR')
            result['hostname'] = answers[0].target if answers else None
        except dns.resolver.NoAnswer:
            pass  # Aucun enregistrement PTR trouvé

        # Resolving other record types (MX, CNAME, TXT, SPF)
        record_types = ['MX', 'CNAME', 'TXT', 'SPF']
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(url, record_type)
                result['records'][record_type] = [str(rdata) for rdata in answers]
            except dns.resolver.NoAnswer:
                result['records'][record_type] = []

    except dns.resolver.NXDOMAIN:
        pass  # Unable to resolve IP address for specified URL

    return result