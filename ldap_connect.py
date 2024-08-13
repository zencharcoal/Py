from ldap3 import Server, Connection, ALL

def main():
    ldap_server = 'ldap://host.com'
    username = 'cn=,dc=,dc=com'  # Adjust as necessary
    password = ''
    server = Server(ldap_server, get_info=ALL)

    # Connect to the server
    with Connection(server, user=username, password=password, auto_bind=True) as conn:
        print("Connection established and bound successfully.")

        while True:
            base_dn = input("Enter Base DN (e.g., 'dc=example,dc=com'): ")
            search_filter = input("Enter search filter (e.g., '(objectclass=*)'): ")
            attributes = input("Enter attributes to retrieve, separated by space (e.g., 'cn mail'): ").split()

            # Perform the search
            conn.search(base_dn, search_filter, attributes=attributes)
            if conn.entries:
                for entry in conn.entries:
                    print(entry)
            else:
                print("No entries found.")

            # Check if the user wants to perform another search
            continue_search = input("Perform another search? (yes/no): ")
            if continue_search.lower() != 'yes':
                break

if __name__ == "__main__":
    main()

