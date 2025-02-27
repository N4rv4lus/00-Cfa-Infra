#Ask Hosts users
host = input("entrez le nom de votre serveur \n")
ip = input("entrez l'ip de votre serveur \n")
lastOctet = ip[12:]

#print the answer to the user or admin
print(f"votre nom d\'hote est {host}")
print(f"votre ip est bien {ip}")
print(f"le dernier bit est bien {lastOctet} nous allons maintenant configurer le playbook ansible")

#ajouter le nom du serveur dans les "hosts" ansible
with open("/etc/ansible/hosts", "a") as file:
        file.write(f"\n{host}")
        file.close

print(f"votre {host} a bien été ajouté aux hoste de ansible dans : /etc/ansible/hosts")

f = open("/etc/ansible/playbook/name-addOnehost.yml")
f.write(f"""
---
  - name: Add hosts to DNS
    hosts: lab-dns
    become: yes
    become_method: sudo
    tasks:
    - name: Add entry to lab-DNS forward zone superzone.com
      shell:
          "sudo sed -i -e '$a{host}.superzone.com.          IN      A       {ip}' /var/named/fwd.superzone.com && tail -1 /var/named/fwd.superzone.com"

    - name: Add entry to lab-DNS reverseZone 192.168.100
      shell:
          "sudo sed -i -e '$a{lastOctet}   IN      PTR     {host}' /var/named/rvs.superzone.com && tail -1 /var/named/rvs.superzone.com"

    - name: reboot service
      shell:
          "sudo systemctl restart named"
""")
f.close()

f = open("/etc/ansible/playbook/name-addOnehost.yml")
print(f.read())
