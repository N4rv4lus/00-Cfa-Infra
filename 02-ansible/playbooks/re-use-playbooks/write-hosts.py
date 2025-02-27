# ask user hostname he wants to add to ansible hosts file
host = input("entrez le nom de votre serveur \n")
with open("/etc/ansible/hosts", "a") as file:
        file.write(f"\n{host}")
        file.close()

# next add host public key and private key, will be added in the next few days