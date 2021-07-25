import socket
import re
import common_ports


ports_and_services = common_ports.ports_and_services


def check_valid_hostname(target):
    valid_hostname_regex = "^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$"
    is_valid_hostname = re.match(valid_hostname_regex, target)
    return is_valid_hostname


def get_host(ip):
    try:
        host = socket.gethostbyaddr(ip)[0]
        return host
    except:
        return ip


def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    try:
        ip = socket.gethostbyname(target)
        host_info = socket.gethostbyname_ex(target)

        host = get_host(ip) if host_info[0] == ip else host_info[0]

        for port in range(port_range[0], port_range[1] + 1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)

            result = s.connect_ex((ip, port))

            if result == 0:
                open_ports.append(port)

            s.close()

        if verbose:
            title = 'Open ports for ' + host + \
                ' (' + ip + ')' if host != ip else 'Open ports for ' + ip

            description_list = [title, 'PORT     SERVICE']

            for port in open_ports:
                space = ' ' * max((9 - len(str(port))), 0)
                row = str(port) + space + \
                    ports_and_services[port] if port in ports_and_services else str(
                        port)

                description_list.append(row)

            return '\n'.join(row for row in description_list)

    except socket.gaierror:
        is_valid_hostname = check_valid_hostname(target)

        if is_valid_hostname:
            return 'Error: Invalid hostname'

        return 'Error: Invalid IP address'

    except socket.error:
        print(socket.error)

    return(open_ports)