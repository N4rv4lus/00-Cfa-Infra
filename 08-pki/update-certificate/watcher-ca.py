import hashlib, os, subprocess

# monitor certificate
## check current certificate hash and compare the old file hash
print(f"\n ### CHECKIN CERTIFICATE - Update ###\n")

with open("/var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem", "rb") as old, \
     open("/watcher/nginx-wildcard-bundle.pem", "rb") as new, \
     open("/watcher/new-wildcard.pem", "rb") as test:
    current_ca_hash = hashlib.file_digest(old, "sha256").hexdigest()
    new_ca_hash = hashlib.file_digest(new, "sha256").hexdigest()
    test_hash = hashlib.file_digest(test, "sha256").hexdigest()

## read comparison
if current_ca_hash == new_ca_hash:
    print(f"Les fichiers ont la même signature : \n /var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem = {current_ca_hash} \n /watcher/nginx-wildcard-bundle.pem     = {new_ca_hash}")

## if difference copy and extract
elif current_ca_hash != new_ca_hash:
    print(f"Les fichiers n'ont pas la même signature, le certificat a été mis à jour : \n /var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem = {current_ca_hash} \n /watcher/nginx-wildcard-bundle.pem     = {new_ca_hash}")
    ## créer un répertoire de travail
    os.makedirs("/watcher/tmp", mode=0o700, exist_ok=True)
    print("le répertoire a bien été créé \n")

    ## copier le fichier bundle-certificat
    subprocess.run(["cp", "/var/lib/openbao-agent/rendered/nginx-wildcard-bundle.pem", "/watcher/tmp/nginx-wildcard-bundle.pem"])
    print("le ficheir a bien été copié")

    ## extraire les clés et créer les fichier correspondant
    bundle = "/watcher/tmp/nginx-wildcard-bundle.pem"

    ## clé privée
    print(f"\n ### EXTRACT - Private Key ###\n")
    privkey = "/watcher/tmp/privkey.pem"

    with open(privkey, "wb") as output:
        subprocess.run(
            [
                "sed",
                "-n",
                "/-----BEGIN EC PRIVATE KEY-----/,/-----END EC PRIVATE KEY-----/p",
                bundle,
            ],
            stdout=output,
            check=True,
        )
    print("La Clé privée a bien été extraite.")

    ## fullchain
    print(f"\n ### EXTRACT - Fullchain ###\n")
    fullchain = "/watcher/tmp/fullchain.pem"

    with open(fullchain, "wb") as output:
        subprocess.run(
            [
                "sed",
                "-n",
                "/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/p",
                bundle,
            ],
            stdout=output,
            check=True,
        )
    print("La Fullchain a bien été extraite.")
## tester les ficheirs

    ## FULLCHAIN - vérifier le format et vérifier l'expiration et le subject alt-name (DNS)
    print(f"\n ### VERIFICATION - Certificat - Expiration & SubjectALTname ###\n")
    subprocess.run(
    [
        "openssl",
        "x509",
        "-in", str(fullchain),
        "-noout",
        "-subject",
        "-issuer",
        "-dates",
        "-ext", "subjectAltName",
        "-purpose",
    ],
    check=True,
    )

    ## FULLCHAIN - vérifier la clé privée
    print(f"\n ### VERIFICATION - Clé Privée ###\n")
    subprocess.run(
    [
        "openssl",
        "pkey",
        "-in", str(privkey),
        "-check",
        "-noout",
    ],
    check=True,
    )

    ## vérifier la wildcard correspond bien a la clé privée
    print(f"\n ### VERIFICATION - Wildcard X Clé Privée ###\n")
    cert_publique = subprocess.run(
    [
        "openssl",
        "x509",
        "-in", str(fullchain),
        "-pubkey",
        "-noout",
    ],
    capture_output=True,
    check=True,
    ).stdout

    cle_publique = subprocess.run(
    [
        "openssl",
        "pkey",
        "-in", str(privkey),
        "-pubout",
    ],
    capture_output=True,
    check=True,
    ).stdout

    if cert_publique != cle_publique:
        raise ValueError(
            "La clé privée ne correspond pas au certificat"
    )

    elif cert_publique == cle_publique:
        print(f"Les clés ont bien la même signature : \n certificat publique : {cert_publique} \n clé publique :        {cle_publique}")

else:
    print("error")

print(f"\n ### TEST CERTIFICATE - NGINX Reverse container\n")

fullchain = "/watcher/tmp/fullchain.pem"
privkey = "/watcher/tmp/privkey.pem"
nginx_tls = "/store-docker-file/nginx-reverse/tls/"
nginx_current_fullchain = "/store-docker-file/nginx-reverse/tls/fullchain.pem"
nginx_current_privkey = "/store-docker-file/nginx-reverse/tls/privkey.pem"
nginx_current_fullchain_bkp = "/store-docker-file/nginx-reverse/tls/fullchain.pem.bkp"
nginx_current_privkey_bkp = "/store-docker-file/nginx-reverse/tls/privkey.pem.bkp"

print(f"\n ### Creating backup - fullchain & private key\n")

subprocess.run(
    [
        "cp",
        "/store-docker-file/nginx-reverse/tls/fullchain.pem",
        "/store-docker-file/nginx-reverse/tls/fullchain.pem.bkp",
    ],
    check=True,
)

subprocess.run(
    [
        "cp",
        "/store-docker-file/nginx-reverse/tls/privkey.pem",
        "/store-docker-file/nginx-reverse/tls/privkey.pem.bkp",
    ],
    check=True,
)

subprocess.run(
    [
        "cp",
        str(fullchain), str(privkey),
        "/store-docker-file/nginx-reverse/tls/",
    ],
    check=True,
)

print(f"\n ### NGINX - check before reload \n")

subprocess.run(
    [
        "docker",
        "exec",
        "nginx-reverse",
        "nginx",
        "-t",
    ],
    check=True,
)

subprocess.run(
    [
        "docker",
        "exec",
        "nginx-reverse",
        "nginx",
        "-s",
        "reload",
    ],
    check=True,
)

## AJOUTER Inotify certificat openbao agent + Droits de fichier + tests / boucle + code retour + suppression du dossier tmp
print(f"\n ### CLEANING - Suppression des repertoires temporaire \n")

subprocess.run(
    [
        "rm",
        "-rf",
        "/watcher/tmp/",
    ],
    check=True,
)