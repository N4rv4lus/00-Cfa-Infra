# CA ROOT

```shell
mkdir /root/ca/
```
```shell
mkdir certs crl newcerts private
```
```shell
chmod 700 private
```
```shell
touch index.txt
```
```shell
echo 1000 > serial
```
```shell
nano openssl.cnf
```
```shell
[ ca ]
# `man ca`
default_ca = CA_default

[ CA_default ]
# Directory and file locations.
dir              = /root/ca
certs            = $dir/certs
crl_dir          = $dir/crl
new_certs_dir    = $dir/newcerts
database         = $dir/index.txt
serial           = $dir/serial
RANDFILE         = $dir/private/.rand

# The root key and root certificate.
private_key      = $dir/private/ca.key.pem
certificate      = $dir/certs/ca.cert.pem

# For certificate revocation lists.
crlnumber        = $dir/crlnumber
crl              = $dir/crl/ca.crl.pem
crl_extensions   = crl_ext
default_crl_days = 30

# SHA-1 is deprecated, so use SHA-2 instead.
default_md       = sha256

name_opt         = ca_default
cert_opt         = ca_default
default_days     = 375
preserve         = no
policy           = policy_strict

[ policy_strict ]
# The root CA should only sign intermediate certificates that match.
# See the POLICY FORMAT section of `man ca`.
countryName            = match
stateOrProvinceName    = match
organizationName       = match
organizationalUnitName = optional
commonName             = supplied
emailAddress           = optional

[ policy_loose ]
# Allow the intermediate CA to sign a more diverse range of certificates.
# See the POLICY FORMAT section of the `ca` man page.
countryName            = optional
stateOrProvinceName    = optional
localityName           = optional
organizationName       = optional
organizationalUnitName = optional
commonName             = supplied
emailAddress           = optional

[ req ]
# Options for the `req` tool (`man req`).
default_bits       = 4096
distinguished_name = req_distinguished_name
string_mask        = utf8only

# SHA-1 is deprecated, so use SHA-2 instead.
default_md         = sha256

# Extension to add when the -x509 option is used.
x509_extensions    = v3_ca

[ req_distinguished_name ]
# See <https://en.wikipedia.org/wiki/Certificate_signing_request>.
commonName                      = Common Name
countryName                     = Country Name (2 letter code)
stateOrProvinceName             = State or Province Name
localityName                    = Locality Name
0.organizationName              = Organization Name
organizationalUnitName          = Organizational Unit Name
emailAddress                    = Email Address

# Optionally, specify some defaults.
countryName_default             = FR
stateOrProvinceName_default     = France
localityName_default            =
0.organizationName_default      = Super Ltd
#organizationalUnitName_default =
#emailAddress_default           =

[ v3_ca ]
# Extensions for a typical CA (`man x509v3_config`).
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints       = critical, CA:true
keyUsage               = critical, digitalSignature, cRLSign, keyCertSign

[ v3_intermediate_ca ]
# Extensions for a typical intermediate CA (`man x509v3_config`).
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints       = critical, CA:true, pathlen:0
keyUsage               = critical, digitalSignature, cRLSign, keyCertSign

[ usr_cert ]
# Extensions for client certificates (`man x509v3_config`).
basicConstraints       = CA:FALSE
nsCertType             = client, email
nsComment              = "OpenSSL Generated Client Certificate"
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer
keyUsage               = critical, nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage       = clientAuth, emailProtection

[ server_cert ]
# Extensions for server certificates (`man x509v3_config`).
basicConstraints       = CA:FALSE
nsCertType             = server
nsComment              = "OpenSSL Generated Server Certificate"
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage               = critical, nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage       = serverAuth

[ crl_ext ]
# Extension for CRLs (`man x509v3_config`).
authorityKeyIdentifier = keyid:always

[ ocsp ]
# Extension for OCSP signing certificates (`man ocsp`).
basicConstraints       = CA:FALSE
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer
keyUsage               = critical, digitalSignature
extendedKeyUsage       = critical, OCSPSigning
```

## GEN CA ROOT KEY

```shell
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-521 -aes-256-cbc -out private/ca.key.pem
```

```shell
chmod 400 private/ca.key.pem
```

```shell
openssl req -config openssl.cnf -key private/ca.key.pem -new -x509 -days 14600 -sha512 -extensions v3_ca -out certs/ca.cert.pem
```

```shell
chmod 444 certs/ca.cert.pem
```

```shell
openssl x509 -noout -text -in certs/ca.cert.pem
```

# CA INTERMEDIAIRE

# CA Intermediate (secondaire)
```shell
mkdir /root/ca/intermediate
```
```shell
cd intermediate/
```
```shell
mkdir certs crl csr newcerts private
```
```shell
chmod 700 private
```
```shell
touch index.txt
```
```shell
echo 1000 > serial
```
```shell
echo 1000 > /root/ca/intermediate/crlnumber
```
```shell
nano openssl.cnf
```

# OpenSSL intermediate CA configuration file.
# Copy to `/root/ca/intermediate/openssl.cnf`.

```shell
[ ca ]
# `man ca`
default_ca = CA_default

[ CA_default ]
# Directory and file locations.
dir               = /root/ca/intermediate
certs             = $dir/certs
crl_dir           = $dir/crl
new_certs_dir     = $dir/newcerts
database          = $dir/index.txt
serial            = $dir/serial
RANDFILE          = $dir/private/.rand

# The root key and root certificate.
private_key       = $dir/private/intermediate.key.pem
certificate       = $dir/certs/intermediate.cert.pem

# For certificate revocation lists.
crlnumber         = $dir/crlnumber
crl               = $dir/crl/intermediate.crl.pem
crl_extensions    = crl_ext
default_crl_days  = 30

# SHA-1 is deprecated, so use SHA-2 instead.
default_md        = sha256

name_opt          = ca_default
cert_opt          = ca_default
default_days      = 375
preserve          = no
policy            = policy_loose

copy_extensions   = copy

[ policy_strict ]
# The root CA should only sign intermediate certificates that match.
# See the POLICY FORMAT section of `man ca`.
countryName             = match
stateOrProvinceName     = match
organizationName        = match
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[ policy_loose ]
# Allow the intermediate CA to sign a more diverse range of certificates.
# See the POLICY FORMAT section of the `ca` man page.
countryName             = optional
stateOrProvinceName     = optional
localityName            = optional
organizationName        = optional
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[ req ]
# Options for the `req` tool (`man req`).
default_bits        = 2048
distinguished_name  = req_distinguished_name
string_mask         = utf8only

# SHA-1 is deprecated, so use SHA-2 instead.
default_md          = sha256

# Extension to add when the -x509 option is used.
x509_extensions     = v3_ca

[ req_distinguished_name ]
# See <https://en.wikipedia.org/wiki/Certificate_signing_request>.
commonName                      = Common Name
countryName                     = Country Name (2 letter code)
stateOrProvinceName             = State or Province Name
localityName                    = Locality Name
0.organizationName              = Organization Name
organizationalUnitName          = Organizational Unit Name
emailAddress                    = Email Address

# Optionally, specify some defaults.
countryName_default             = XX
stateOrProvinceName_default     = MyState
localityName_default            =
0.organizationName_default      = MyOrg
organizationalUnitName_default  =
emailAddress_default            =

[ v3_ca ]
# Extensions for a typical CA (`man x509v3_config`).
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[ v3_intermediate_ca ]
# Extensions for a typical intermediate CA (`man x509v3_config`).
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true, pathlen:0
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[ usr_cert ]
# Extensions for client certificates (`man x509v3_config`).
basicConstraints = CA:FALSE
nsCertType = client, email
nsComment = "OpenSSL Generated Client Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
keyUsage = critical, nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth, emailProtection

[ server_cert ]
# Extensions for server certificates (`man x509v3_config`).
basicConstraints = CA:FALSE
nsCertType = server
nsComment = "OpenSSL Generated Server Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
authorityInfoAccess = OCSP;URI:http://ocsp2.example.com
#subjectAltName = @alt_names

#[ alt_names ]
#DNS.1 = example.com
#DNS.2 = www.example.com
#DNS.3 = m.example.com

[ crl_ext ]
# Extension for CRLs (`man x509v3_config`).
authorityKeyIdentifier=keyid:always

[ ocsp ]
# Extension for OCSP signing certificates (`man ocsp`).
basicConstraints = CA:FALSE
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
keyUsage = critical, digitalSignature
extendedKeyUsage = critical, OCSPSigning
```
## Gen Intermediate CA key 
```shell
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-521 -aes-256-cbc -out /root/ca/intermediate/private/intermediate.key.pem
```
```shell
openssl req -config intermediate/openssl.cnf -new -sha512 -key intermediate/private/intermediate.key.pem -out intermediate/csr/intermediate.csr.pem
```
```shell
chmod 400 intermediate/private/intermediate.key.pem
```
```shell
openssl ca -config openssl.cnf -extensions v3_intermediate_ca -days 7300 -notext -md sha512 -in intermediate/csr/intermediate.csr.pem -out intermediate/certs/intermediate.cert.pem
```
```shell
openssl x509 -noout -text -in intermediate/certs/intermediate.cert.pem
```
```shell
openssl verify -CAfile certs/ca.cert.pem intermediate/certs/intermediate.cert.pem
```
```shell
cat intermediate/certs/intermediate.cert.pem certs/ca.cert.pem >     intermediate/certs/ca-chain.cert.pem
```
```shell
chmod 444 intermediate/certs/ca-chain.cert.pem
```
## CONFIGURATION FOR CERTIFICATE AND WORKFLOW EXPLANATION 

### OPENSSL CLI - exemple web signature

Add the specific role with the specific name 

add for webconfiguration file
```cnf
[service-name]
basicConstraints = critical, CA:FALSE # sensitivity + Authorization to sign and continue signing (CSR) values
subjectKeyIdentifier = hash # identifier, select hash - SHA1 - SHA2 - SHA3 etc
authorityKeyIdentifier = keyid,issuer # specify the identifier (your corp, compagny, well certificate issuer)
keyUsage = critical, digitalSignature # sensitivity/criticity + usage, here it's for web
extendedKeyUsage = serverAuth # specify to authenticate to the url
subjectAltName = @openbao_san # specify the alternative name dedicated for the specific source, you could only validate a domain, or a server name, or directly an IP

[dns-reference]
DNS.1 = openbao.lab.local # DNS Record, it could be a wildcard
DNS.2 = openbao # DNS hostname, wihtout fqdn in case it changes
IP.1 = 192.168.100.9 # IP if needed to secure the IP connection
```
PKI Workflow : 
1. The service-server, here a web server generates its private key.
2. It derives the corresponding public key.
3. It creates a CSR containing:
  - the public key;
  - the requested identity;
  - the requested SANs;
  - a signature made with the private key.
4. Only the CSR is sent to the intermediate CA.
5. The CA verifies the CSR and applies its policy.
6. The CA creates and signs an X.509 certificate.
7. The certificate and intermediate chain are sent back to OpenBao.
8. OpenBao installs the certificate alongside its original private key.

## COMMAND OVERVIEW 

COMMANDS : 

# openssl genpkey
Generate private key
```shell
openssl genpkey \
  -algorithm EC \ # Select the public-key algorithm for an ECDSA certificate, generate an EC key, other examples include RSA, RSA-PSS, ED25519 and ED448
  -pkeyopt ec_paramgen_curve:P-384 \ # Select the named elliptic curve, P-256, P-384 and P-521 are NIST elliptic curves
  -pkeyopt ec_param_enc:named_curve \ # select the type of curve
  -out /etc/openbao/tls/openbao.superzone.com.key.pem # Encode the EC parameters by referencing the named curve instead of writing
all the mathematical parameters explicitly, named_curve is already OpenSSL's default
```
# openssl req
generate CSR - chain signature file
```shell
openssl req \
  -new \ # Generate a new CSR
  -sha384 \ # Use SHA-384 as the digest for the CSR's signature, the CSR is signed with OpenBao's private key to prove possession of that key
  -key /etc/openbao/tls/openbao.superzone.com.key.pem \ # Select the private key used to create and sign the CSR the corresponding public key is included in the CSR.
  -out /etc/openbao/tls/openbao.superzone.com.csr.pem \ # Select the destination and filename for the CSR.
  -subj "/C=FR/O=LAB/CN=openbao.superzone.com" \ # Specify the requested subject identity for the future certificate these values describe the role, the CA policy may accept, reject or omit some of these fields.
  -addext "subjectAltName=DNS:openbao.superzone.com" # Add the requested SAN extension to the CSR the issuing CA may accept, replace or ignore requested extensions according to its own configuration.
```
```shell
openssl req \
  -new \
  -sha384 \
  -key /etc/openbao/tls/openbao.superzone.com.key.pem \
  -out /etc/openbao/tls/openbao.superzone.com.csr.pem \
  -subj "/C=FR/O=LAB/CN=openbao.superzone.com" \
  -addext "subjectAltName=DNS:openbao.superzone.com"
```
  # openssl ca
sign CSR (Certificate Signing Request) with root ca or intermediate CA (depending on your env)
```shell
openssl ca \
  -config /root/ca/intermediate/openssl.cnf \ # Load the configuration of the issuing CA, it identifies the CA certificate, CA private key, database, serial number, policies and output directories
  -extensions openbao_server \ # Apply the X.509 extension profile named openbao_server this profile should define CA:FALSE, serverAuth, key usage and SAN values. It is an OpenSSL certificate profile.
  -days 365 \ # Set the validity period of the issued certificate, a csr itself does not have a vadlity period.
  -notext \ # Do not prepend a human-readable certificate description to the output file, the output file will contain the PEM-encoded certificate.
  -md sha384 \ # Use SHA-384 when the issuing CA signs the final certificate. The CSR has it's own signature.
  -in /etc/openbao/tls/openbao.superzone.com.csr.pem \ # Select the CSR that the CA must validate and certify
  -out /root/ca/intermediate/certs/openbao.superzone.com.cert.pem # Select the output filename for the issued certificate. OpenSSL separately records the issuance in the CA database configured by the database directive, usually index.txt.
```
```shell
  openssl ca \
  -config /root/ca/intermediate/openssl.cnf \ 
  -extensions openbao_server \ 
  -days 730 \
  -notext \
  -md sha384 \
  -in /etc/openbao/tls/openbao.superzone.com.csr.pem \
  -out /root/ca/intermediate/certs/openbao.superzone.com.cert.pem
```
# openssl x509
inspects the certificate but does not validate its certification chain.
```shell
openssl x509 \
  -in /root/ca/intermediate/certs/openbao.superzone.com.cert.pem \ # Select the X.509 certificate to inspect. Here, this is the OpenBao server certificate and not a CA certificate.
  -noout \ # suppress the PEM encoded certificate output, only the requested information is displayed.
  -subject \ #  display the identity certified for the new certificate
  -issuer \ # display the CA that issued the certificate
  -dates \ # Display the notBefore and notAfter validity dates
  -ext subjectAltName,basicConstraints,keyUsage,extendedKeyUsage # alt names specified in the CA cnf file (role etc)
```
```shell
openssl x509 -in /root/ca/intermediate/certs/openbao.superzone.com2.cert.pem -noout -subject -issuer -dates -ext subjectAltName,basicConstraints,keyUsage,extendedKeyUsage
```
# openssl verify
This verifies more than the certificate signature: it also checks the chain, validity dates, CA constraints, TLS-server purpose and hostname.
```shell
openssl verify \ 
  -show_chain \ # show the certification chain  built by OpenSSL
  -purpose sslserver \ # Check that the target certificate and its chain are valid for a TLS server, this validates the certificate purpose
  -verify_hostname openbao.superzone.com \ # Verify that the requested hostname is covered by the certificate SAN.
  -CAfile /root/ca/certs/ca.cert.pem \ # Provide the trusted root CA certificate, the root is the trust anchor
  -untrusted /root/ca/intermediate/certs/intermediate.cert.pem \ # Provide the intermediate CA certificate needed to build the chain here, "untrusted" means that it is not the trust anchor it does not mean that the intermediate certificate is invalid.
  /root/ca/intermediate/certs/openbao.superzone.com.cert.pem # Specify the target certificate to validate here, this is the OpenBao server certificate, not a CA certificate.
```
```shell
openssl verify -show_chain -purpose sslserver -verify_hostname openbao.superzone.com -CAfile /root/ca/certs/ca.cert.pem -untrusted /root/ca/intermediate/certs/intermediate.cert.pem /root/ca/intermediate/certs/openbao.superzone.com2.cert.pem 
```
  Il faut maintenant ajouter dans openssl.cnf de la ca root l'élément lui permettant de signer la CA intermediaire qui permettra de signer la CA d'openbao et autorisera la chaine CA root - Ca Openbao Intermediaire - CA Openbao

```cnf
[ v3_intermediateOpenBao_ca ]
#Extensions for openbao
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:TRUE, pathlen:1
keyUsage = critical, keyCertSign, cRLSign

le fichier de configuration openssl de la ca intermediaire dédiée à openbao contiendra ces informations : 
[ ca ]
# `man ca`
default_ca = CA_default

[ CA_default ]
# Directory and file locations.
dir              = /root/ca
certs            = $dir/certs
crl_dir          = $dir/crl
new_certs_dir    = $dir/newcerts
database         = $dir/index.txt
serial           = $dir/serial
RANDFILE         = $dir/private/.rand

# The root key and root certificate.
private_key      = $dir/private/ca.key.pem
certificate      = $dir/certs/ca.cert.pem

# For certificate revocation lists.
crlnumber        = $dir/crlnumber
crl              = $dir/crl/ca.crl.pem
crl_extensions   = crl_ext
default_crl_days = 30

# SHA-1 is deprecated, so use SHA-2 instead.
default_md       = sha256

name_opt         = ca_default
cert_opt         = ca_default
default_days     = 375
preserve         = no
policy           = policy_strict

[ policy_strict ]
# The root CA should only sign intermediate certificates that match.
# See the POLICY FORMAT section of `man ca`.
countryName            = match
stateOrProvinceName    = match
organizationName       = match
organizationalUnitName = optional
commonName             = supplied
emailAddress           = optional

[ policy_loose ]
# Allow the intermediate CA to sign a more diverse range of certificates.
# See the POLICY FORMAT section of the `ca` man page.
countryName            = optional
stateOrProvinceName    = optional
localityName           = optional
organizationName       = optional
organizationalUnitName = optional
commonName             = supplied
emailAddress           = optional

[ req ]
# Options for the `req` tool (`man req`).
default_bits       = 4096
distinguished_name = req_distinguished_name
string_mask        = utf8only

# SHA-1 is deprecated, so use SHA-2 instead.
default_md         = sha256

# Extension to add when the -x509 option is used.
x509_extensions    = v3_ca

[ req_distinguished_name ]
# See <https://en.wikipedia.org/wiki/Certificate_signing_request>.
commonName                      = Common Name
countryName                     = Country Name (2 letter code)
stateOrProvinceName             = State or Province Name
localityName                    = Locality Name
0.organizationName              = Organization Name
organizationalUnitName          = Organizational Unit Name
emailAddress                    = Email Address

# Optionally, specify some defaults.
countryName_default             = FR
stateOrProvinceName_default     = France
localityName_default            = Paris
0.organizationName_default      = Subarashi Corp
#organizationalUnitName_default = Oseille
#emailAddress_default           = n4v4rlus@gmail.com

[ v3_ca ]
# Extensions for a typical CA (`man x509v3_config`).
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints       = critical, CA:true, pathlen:1
keyUsage               = critical, digitalSignature, cRLSign, keyCertSign

[ v3_intermediate_ca ]
# Extensions for a typical intermediate CA (`man x509v3_config`).
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints       = critical, CA:true, pathlen:0
keyUsage               = critical, digitalSignature, cRLSign, keyCertSign

[ v3_OpenBao_ca ]
# Extensions for openbao
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:TRUE, pathlen:0
keyUsage = critical, keyCertSign, cRLSign

[ usr_cert ]
# Extensions for client certificates (`man x509v3_config`).
basicConstraints       = CA:FALSE
nsCertType             = client, email
nsComment              = "OpenSSL Generated Client Certificate"
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer
keyUsage               = critical, nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage       = clientAuth, emailProtection

[ server_cert ]
# Extensions for server certificates (`man x509v3_config`).
basicConstraints       = CA:FALSE
nsCertType             = server
nsComment              = "OpenSSL Generated Server Certificate"
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage               = critical, nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage       = serverAuth

[ crl_ext ]
# Extension for CRLs (`man x509v3_config`).
authorityKeyIdentifier = keyid:always

[ ocsp ]
# Extension for OCSP signing certificates (`man ocsp`).
basicConstraints       = CA:FALSE
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer
keyUsage               = critical, digitalSignature
extendedKeyUsage       = critical, OCSPSigning
```
## KEY GENERATION AND SIGN
```shell
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-521 -aes-256-cbc -out /root/ca/intermediateOpenBao/intermediateOpenBao.key.pem
```
```shell
openssl req -config /root/ca/intermediateOpenBao/openssl.cnf -new -sha512 -key /root/ca/intermediateOpenBao/private/intermediateOpenBao.key.pem -out /root/ca/intermediateOpenBao/csr/intermediateOpenBao.csr.pem
```
```shell
chmod 400 intermediateOpenBao/private/intermediateOpenBao.key.pem
```
```shell
openssl ca -config /root/ca/openssl.cnf -extensions v3_openbao_parent_ca -days 7300 -notext -md sha512 -in /root/ca/intermediateOpenBao/csr/intermediateOpenBao.csr.pem -out /root/ca/intermediateOpenBao/certs/intermediateOpenBao.cert.pem
```
```shell
openssl x509 -noout -text -in /root/ca/intermediateOpenBao/certs/intermediateOpenBao.cert.pem
```
```shell
openssl verify -CAfile /root/ca/certs/ca.cert.pem /root/ca/intermediateOpenBao/certs/intermediateOpenBao.cert.pem
```
# Setup CA sign for openbao url & api

stop service if it was running

```shell
sudo systemctl stop openbao
```
then save the first config file : 
```shell
sudo cp --preserve=all \
  /etc/openbao/openbao.hcl \
  /etc/openbao/openbao.hcl.before-bootstrap
```
then create directories for open bao and add user's ownership + directory rights for users : 
```shell
sudo install -d \
  -o root \
  -g openbao \
  -m 0750 \
  /etc/openbao
```
```shell
sudo install -d \
  -o root \
  -g openbao \
  -m 0750 \
  /etc/openbao/tls
```
```shell
sudo install -d \
  -o openbao \
  -g openbao \
  -m 0700 \
  /var/lib/openbao/data
```
```shell
sudo install -d \
  -o openbao \
  -g openbao \
  -m 0750 \
  /var/log/openbao
```
## Déployez le certificat openbao WEB 
Ce certirficat certifie les éléments suivants : WEB / API / CLI
```shell
cat \
  /root/ca/intermediateOpenBao/certs/intermediateOpenBao.cert.pem \
  /root/ca/certs/ca.cert.pem \
  > /root/ca/intermediateOpenBao/certs/ca-chain.cert.pem
```
```shell
chmod 444 /root/ca/intermediateOpenBao/certs/ca-chain.cert.pem
```
# configurez openbao 

Maintenant il faut concatener les deux certificats publiques pour avoir la chaine de certificat complète: 
concatener le certificat openbao en 1er puis la clé publique de la CA intermédiaire pour avoir la full chaine.

```shell
cat \
  /root/ca/intermediate/certs/openbao.superzone.com.cert.pem \
  /root/ca/intermediate/certs/intermediate.cert.pem \
  > /etc/openbao/tls/openbao.superzone.com.fullchain.pem
```
## Renouveller un certificat 
1st create a new certificate REQ, sign. (PS you can use the old public key, or renew it, it's your choice) : 
```shell
openssl req -new -sha384 -key /etc/openbao/tls/openbao.key.pem -out /etc/openbao/tls/openbao.superzone.com2.csr.pem -subj "/C=FR/O=LAB/CN=openbao.superzone.com" -addext "subjectAltName=DNS:openbao.superzone.com"
```
```shell
openssl ca -config /root/ca/intermediate/openssl.cnf -extensions openbao_server -days 2000 -notext -md sha384 -in /etc/openbao/tls/openbao.superzone.com2.csr.pem -out /root/ca/intermediate/certs/openbao.superzone.com2.cert.pem
```
```shell
openssl x509 -noout -text -in /root/ca/intermediate/certs/openbao.superzone.com2.cert.pem
```
```shell
openssl verify -CAfile /root/ca/certs/ca.cert.pem /root/ca/intermediate/certs/openbao.superzone.com2.cert.pem
```
maintenant concatenez le nouveau certificat avec la nouvelle chaine
```shell
cat \
  /root/ca/intermediate/certs/openbao.superzone.com2.cert.pem \
  /root/ca/intermediate/certs/intermediate.cert.pem \
  > /etc/openbao/tls/openbao.superzone.com2.fullchain.pem
```
2nd revoke the old one : 
```shell
openssl ca \
  -config /root/ca/intermediate/openssl.cnf \
  -revoke /root/ca/intermediate/certs/openbao.superzone.com.cert.pem \
  -crl_reason superseded
```
3rd generate the crl (certificat revocation list)
```shell
openssl ca \
  -config /root/ca/intermediate/openssl.cnf \
  -gencrl \
  -out /root/ca/intermediate/crl/intermediate.crl.pem
```
## Fonctionnement du certificat pour openBao
Le client (navigateur par exemple) pourra voir la chaine complete dans son navigateur
Certificat TLS OpenBao
    ↓ signé par
Certificat de la CA intermédiaire
    ↓ signée par
CA racine déjà approuvée par le client

## Configurez openbao

## déployer le certificat openbao

Il va maintenant falloir configurer openbao pour utiliser ces clés, il faudra aussi configurer la fullchain et la clé privée dans openbao.

ajoutez cet élément dans votre fichier de configuration openbao.hcl. Vous pouvez aussi filtrer sur le protocole tls, et aussi l'interface d'écoute qui ici sont toutes les IPv4 (address & cluster_addr) : 
```shell
listener "tcp" {
  address       = "0.0.0.0:8200"
  cluster_addr = "0.0.0.0:8201"

  tls_disable = false
  tls_cert_file = "/etc/openbao/tls/openbao.superzone.com.fullchain.pem"
  tls_key_file  = "/etc/openbao/tls/openbao.key.pem"

  tls_min_version = "tls12"
  tls_max_version = "tls13"
}
```
Il faudra aussi maintenant configurer les urls et les ports d'écoute : 
api_addr = "https://openbao.superzone.com:8200"
cluster_addr = "https://openbao.superzone.com:8201"

il faudra aussi ensuite ouvrir les flux sur votre serveur OpenBao : 
```shell
sudo firewall-cmd --permanent --add-port=8200/tcp
sudo firewall-cmd --reload
```
Pourquoi est-ce qu'on ouvre pas le port 8201 à l'extérieur?
C'est parce qu'il ne doit etre accessible que par les autres noeuds du cluster et ici nous n'en avons pas.

Il faudra maintenant déclarer openbao sur votre serveur DNS dans les zone forward et reverse.

Il faudra ensuite déployer le certificat publique de la CA root dans le magasin de certificat de vos serveurs / applications : 

copiez la clé
```shell
scp /root/ca/certs/ca.cert.pem compte@IP:/tmp/superzone-root-ca.crt
```
puis installez la dans votre magasin système EL9: 
```shell
install -m 0644 \
  /root/ca/certs/ca.cert.pem \
  /etc/pki/ca-trust/source/anchors/subarashi-root-ca.crt
```
Then you will only need to add the correct env variable for your dedicated user : 

edit .bash_profile of the user which will use openbao cli : 
```shell
nano /home/admin/.bash_profile
```
and add this line at the bootom of the file : 
```shell
export BAO_ADDR="https://openbao.superzone.com:8200"
```
then test it :
```shell 
echo $BAO_ADDR
bao status
```

# configurez openbao a utiliser openbao et le FQDN (fourni par le DNS) pour pouvoir exécuter openbao

Créeez le fichier 

Après avoir initialisé le token en mode file (pas raft donc pas de HA) : 
```shell
bao operator init \
  -key-shares=5 \
  -key-threshold=3
Unseal Key 1: 4MxpyfXslnVT+EpupXx3KicMcaGNYO+16maPpcN3ml35
Unseal Key 2: Lv1A7xjzRJ3wA6qOV5MCB1zGWY+gvnIsH0qTR/6WSfgU
Unseal Key 3: lFJkWAAbKPlSLRjxxrNc0sj93v+AZ1dopT3oukrSrn/z
Unseal Key 4: 1XVnH9Rq7CBtnCBp6oOmWeVd/rkS6XF9DNkI8JaEXIPw
Unseal Key 5: v0OoLcRaI4NokGRGhElb7/MCnW7piqkIwbD7YM9maN/+

Initial Root Token: s.gGPXQ0Dp1lhnUinUeaNfGuj2

Vault initialized with 5 key shares and a key threshold of 3. Please securely
distribute the key shares printed above. When the Vault is re-sealed,
restarted, or stopped, you must supply at least 3 of these keys to unseal it
before it can start servicing requests.

Vault does not store the generated root key. Without at least 3 keys to
reconstruct the root key, Vault will remain permanently sealed!

It is possible to generate new unseal keys, provided you have a quorum
of existing unseal keys shares. See "bao operator rotate-keys" for more
information.
```
