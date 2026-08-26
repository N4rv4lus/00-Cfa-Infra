Il faut maintenant ajouter dans openssl.cnf de la ca root l'élément lui permettant de signer la CA intermediaire qui permettra de signer la CA d'openbao et autorisera la chaine CA root - Ca Openbao Intermediaire - CA Openbao

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

## KEY GENERATION AND SIGN

openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-521 -aes-256-cbc -out /root/ca/intermediateOpenBao/intermediateOpenBao.key.pem

openssl req -config /root/ca/intermediateOpenBao/openssl.cnf -new -sha512 -key /root/ca/intermediateOpenBao/private/intermediateOpenBao.key.pem -out /root/ca/intermediateOpenBao/csr/intermediateOpenBao.csr.pem

chmod 400 intermediateOpenBao/private/intermediateOpenBao.key.pem

openssl ca -config /root/ca/openssl.cnf -extensions v3_openbao_parent_ca -days 7300 -notext -md sha512 -in /root/ca/intermediateOpenBao/csr/intermediateOpenBao.csr.pem -out /root/ca/intermediateOpenBao/certs/intermediateOpenBao.cert.pem

openssl x509 -noout -text -in /root/ca/intermediateOpenBao/certs/intermediateOpenBao.cert.pem

openssl verify -CAfile /root/ca/certs/ca.cert.pem /root/ca/intermediateOpenBao/certs/intermediateOpenBao.cert.pem

cat \
  /root/ca/intermediateOpenBao/certs/intermediateOpenBao.cert.pem \
  /root/ca/certs/ca.cert.pem \
  > /root/ca/intermediateOpenBao/certs/ca-chain.cert.pem

chmod 444 /root/ca/intermediateOpenBao/certs/ca-chain.cert.pem

