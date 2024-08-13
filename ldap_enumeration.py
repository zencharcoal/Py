import ldap

# Configuration - Replace these with actual server details and credentials
LDAP_SERVER = 'ldap://<target-ip>:389'
BIND_DN = 'cn=manager,dc=example,dc=com'
BIND_PASSWORD = 'password'
BASE_DN = 'dc=example,dc=com'

def initialize_ldap_connection(server, bind_dn, password):
    try:
        l = ldap.initialize(server)
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(bind_dn, password)
        print("Connected and bound to server.")
        return l
    except ldap.LDAPError as e:
        print("Failed to connect or bind:", e)
        return None

def search_and_print(ldap_conn, base_dn, search_filter, attributes):
    try:
        result = ldap_conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, attributes)
        for dn, entry in result:
            print('DN:', dn)
            for attr in entry:
                print(f'{attr}: {entry[attr]}')
    except ldap.LDAPError as e:
        print("Search failed:", e)

def perform_queries(ldap_conn):
    # Query 1: All users
    print("\n--- All Users ---")
    search_and_print(ldap_conn, BASE_DN, "(objectClass=person)", ['cn', 'mail'])

    # Query 2: All groups
    print("\n--- All Groups ---")
    search_and_print(ldap_conn, BASE_DN, "(objectClass=group)", ['cn'])

    # Query 3: Users with specific attribute (e.g., users with no password expiration)
    print("\n--- Users with no password expiration ---")
    search_and_print(ldap_conn, BASE_DN, "(&(objectClass=person)(pwdLastSet=0))", ['cn'])

    # Query 4: All organizational units
    print("\n--- Organizational Units ---")
    search_and_print(ldap_conn, BASE_DN, "(objectClass=organizationalUnit)", ['ou'])

    # Query 5: Members of a specific group (e.g., "Admins")
    print("\n--- Members of 'Admins' Group ---")
    search_and_print(ldap_conn, BASE_DN, "(&(objectClass=person)(memberOf=cn=Admins,ou=groups,dc=example,dc=com))", ['cn'])

if __name__ == "__main__":
    ldap_conn = initialize_ldap_connection(LDAP_SERVER, BIND_DN, BIND_PASSWORD)
    if ldap_conn:
        perform_queries(ldap_conn)
        ldap_conn.unbind_s()  # Disconnect and unbind from server

