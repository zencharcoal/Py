import sys
import ldap3
from ldap3 import Server, Connection, ALL, Tls
import ssl

def read_file(file_path):
    """Reads lines from a file and returns them as a list."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def main(ldap_server, username_file, password_file):
    user_list = read_file(username_file)
    pass_list = read_file(password_file)

    print(f"Connecting to server: {ldap_server}")
    tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLS_CLIENT)
    server = Server(ldap_server, use_ssl=True, tls=tls_configuration, get_info=ALL)

    for username, password in zip(user_list, pass_list):
        print(f"Attempting to connect as {username}")
        try:
            with Connection(server, user=username, password=password, authentication=ldap3.SIMPLE) as conn:
                if conn.bind():
                    print(f"Connection succeeded for user: {username}")
                else:
                    print(f"Connection failed for user: {username}")
        except ldap3.core.exceptions.LDAPBindError as e:
            print(f"Bind error for user {username}: {str(e)}")
        except Exception as e:
            print(f"An error occurred for user {username}: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python ldap_test.py <LDAP server URL> <username file> <password file>")
        sys.exit(1)

    ldap_server = sys.argv[1]
    username_file = sys.argv[2]
    password_file = sys.argv[3]

    main(ldap_server, username_file, password_file)

