# Bao setup

## unseal the vault
bao operator unseal

Then add the token which were given when you initialised openbao

## status check
Then check the status : 

bao status

### output
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    5
Threshold       3
Version         2.6.1-1.el9
Commit Date     2026-07-22
Storage Type    file
Cluster Name    vault-cluster-7619cf36
Cluster ID      9a891ae9-e8bf-0844-39b5-1165a6d257d6
HA Enabled      false

Check the secret list and check that no pki engine was enabled : 

bao secrets list -detailed


### output
Path          Plugin       Accessor              Default TTL    Max TTL    Force No Cache    Replication    Seal Wrap    External Entropy Access    Options    Description                                                UUID                                    Version    Running Version       Running SHA256    Deprecation Status
----          ------       --------              -----------    -------    --------------    -----------    ---------    -----------------------    -------    -----------                                                ----                                    -------    ---------------       --------------    ------------------
cubbyhole/    cubbyhole    cubbyhole_f5d98f57    n/a            n/a        false             local          false        false                      map[]      per-token private secret storage                           866eb92f-6d25-bcc1-6519-faa5649df8f7    n/a        v2.6.1+builtin.bao    n/a               n/a
identity/     identity     identity_ea56d2e5     system         system     false             replicated     false        false                      map[]      identity store                                             b302792a-88d4-a5a7-b9f6-6fa51cea173c    n/a        v2.6.1+builtin.bao    n/a               n/a
sys/          system       system_fe31cfb6       n/a            n/a        false             replicated     true         false                      map[]      system endpoints used for control, policy and debugging    54065be9-2c40-f6fb-3691-40260e239a12    n/a        v2.6.1+builtin.bao    n/a               n/a

## enable pki engine

PKI_MOUNT="pki_services"

bao secrets enable -path="$PKI_MOUNT" -description="CA émettrice des certificats de services superzone.com" pki

### output
Success! Enabled the pki secrets engine at: pki_services/

## Set a time limit for certificates

bao secrets tune -default-lease-ttl="720h" -max-lease-ttl="8760h" "$PKI_MOUNT"

## Create the directory for the CSR and generate the csr
Openbao will also store the CSR in /intermediate/generate/internal
La clé privée est stockée elle directement dans openbao, la csr est publique

mkdir -p "/home/admin/pki-bootstrap"
chmod 700 "/home/admin/pki-bootstrap"

CSR_FILE="/home/admin/pki-bootstrap/openbao-services-issuing-ca.csr.pem"

umask 077

bao write -field=csr \
  "$PKI_MOUNT/intermediate/generate/internal" \
  common_name="Superzone OpenBao Services Issuing CA 2026" \
  organization="Superzone" \
  ou="PKI" \
  country="FR" \
  locality="Paris" \
  key_type="ec" \
  key_bits="384" \
  key_name="openbao-services-ca-2026" \
  exclude_cn_from_sans=true \
  > "$CSR_FILE"

## verify the csr 

openssl req \
  -in "$CSR_FILE" \
  -noout -verify -subject

openssl req \
  -in "$CSR_FILE" \
  -noout -text

## Sign the CSR with your intermediate pki dedicated for openbao

openssl ca -config /root/ca/intermediateOpenBao/openssl.cnf -extensions v3_openbao_parent_ca -days 1825 -notext -md sha512 -in /home/admin/pki-bootstrap/openbao-services-issuing-ca.csr.pem -out /root/ca/intermediateOpenBao/certs/openbao-services-issuing-ca.cert.pem

openssl x509 -noout -text -in /root/ca/intermediateOpenBao/certs/openbao-services-issuing-ca.cert.pem

openssl verify -CAfile /root/ca/intermediateOpenBao/certs/ca-chain.cert.pem /root/ca/intermediateOpenBao/certs/openbao-services-issuing-ca.cert.pem

## now generate the full chain 
sudo bash -c 'cat \
  /root/ca/intermediateOpenBao/certs/openbao-services-issuing-ca.cert.pem \
  /root/ca/intermediateOpenBao/certs/ca-chain.cert.pem \
  > /etc/openbao.d/pki-bootstrap/openbao-services-issuing-ca-chain.pem'

## Now import the signed certificate in openbao
must specify temporary values for openbao because it does not accept absolute path

PKI_MOUNT="pki_services"
BUNDLE="/home/admin/pki-bootstrap/openbao-services-issuing-ca.bundle.pem"

bao write pki_services/intermediate/set-signed /home/admin/pki-bootstrap/openbao-services-issuing-ca.bundle.pem

## vérifier l'émetteur
bao read pki_services/config/issuers
bao read pki_services/issuer/default

lister les clé cryptographiques dans le moteur PKI
bao list pki_services/keys

lister les issuers présents : 
bao list pki_services/issuers

## Nommer l'issuer, sa clé, et configurer les url AIA, CRL et OCSP

bao patch \
  pki_services/issuer/909624f4-7d5d-5a6a-62bf-fc6fcfcb72e5 \
  issuer_name="openbao-services-issuing-ca"

bao write \
  pki_services/key/82c83843-ed28-9186-eb47-816d51593aa2 \
  key_name="openbao-services-issuing-key"

Check the configuration : 
bao read \
  pki_services/key/82c83843-ed28-9186-eb47-816d51593aa2

## now check the chain and the default key 

bao read pki_services/config/keys

it must be the following uuid (set previously): 82c83843-ed28-9186-eb47-816d51593aa2

then check the chain : 
bao read -format=json pki_services/issuer/default |
jq '.data.ca_chain | length'

it must output at least 2, and 3 if you have your ca signed (ca root, intermediate, and the openbao's certificate)

## URL configuration AIA, CRL, OSCP

set the cluster path for the pki service : 

bao write pki_services/config/cluster \
  path="https://openbao.superzone.com:8200/v1/pki_services"

Now set the url in the issuer : 
bao patch \
  pki_services/issuer/909624f4-7d5d-5a6a-62bf-fc6fcfcb72e5 \
  issuing_certificates="https://openbao.superzone.com:8200/v1/pki_services/issuer/909624f4-7d5d-5a6a-62bf-fc6fcfcb72e5/der" \
  crl_distribution_points="https://openbao.superzone.com:8200/v1/pki_services/issuer/909624f4-7d5d-5a6a-62bf-fc6fcfcb72e5/crl/der" \
  ocsp_servers="https://openbao.superzone.com:8200/v1/pki_services/ocsp"

### Setup CRL

bao write pki_services/config/crl \
  disable=false \
  expiry="72h" \
  auto_rebuild=true \
  auto_rebuild_grace_period="12h" \
  enable_delta=false \
  ocsp_disable=false \
  ocsp_expiry="12h"

Generate the 1st CRL
bao read pki_services/crl/rotate

now check the crl 
bao read pki_services/config/crl

### SETUP TLS Server role
Ce rôle autorise uniquement les sous-domaines de superzone.com, sans IP, wildcard ou certificat client :

bao write pki_services/roles/tls-server-superzone \
  issuer_ref="909624f4-7d5d-5a6a-62bf-fc6fcfcb72e5" \
  allowed_domains="superzone.com" \
  allow_bare_domains=false \
  allow_subdomains=true \
  allow_glob_domains=false \
  allow_wildcard_certificates=false \
  allow_any_name=false \
  enforce_hostnames=true \
  allow_localhost=false \
  allow_ip_sans=false \
  server_flag=true \
  client_flag=false \
  code_signing_flag=false \
  email_protection_flag=false \
  key_type="ec" \
  key_bits=384 \
  key_usage="DigitalSignature" \
  ttl="720h" \
  max_ttl="2160h" \
  no_store=false \
  generate_lease=false \
  require_cn=true \
  not_before_bound="duration" \
  not_after_bound="ttl-limited"

check the configuration : 
bao read pki_services/roles/tls-server-superzone

Now test and check : 
install -d -m 0700 /home/admin/pki-test
umask 077

bao write -format=json \
  pki_services/issue/tls-server-superzone \
  common_name="pki-test.superzone.com" \
  ttl="24h" \
  > /home/admin/pki-test/issue-response.json

now check Openbao configuration : 

## Bao health check 
bao pki health-check pki_services

## bao health check output

ca_validity_period
------------------
status    endpoint                                                     message
------    --------                                                     -------
ok        /pki_services/issuer/33a8fb97-0e21-0ff1-1c26-28782a521566    Issuer's validity (2046-08-07) is OK
ok        /pki_services/issuer/909624f4-7d5d-5a6a-62bf-fc6fcfcb72e5    Issuer's validity (2031-08-24) is OK
ok        /pki_services/issuer/939d574b-9500-15ad-a735-987e4ee8256f    Issuer's validity (2066-07-23) is OK


crl_validity_period
-------------------
status    endpoint                                                               message
------    --------                                                               -------
ok        /pki_services/issuer/909624f4-7d5d-5a6a-62bf-fc6fcfcb72e5/crl          CRL's validity (2026-08-25 to 2026-08-28) is OK.
ok        /pki_services/issuer/909624f4-7d5d-5a6a-62bf-fc6fcfcb72e5/crl/delta    Delta CRL's validity (2026-08-25 to 2026-08-28) is OK.


root_issued_leaves
------------------
status    endpoint               message
------    --------               -------
ok        /pki_services/certs    Root certificate(s) in this mount have not directly issued non-CA leaf certificates.


role_allows_localhost
---------------------
status    endpoint               message
------    --------               -------
ok        /pki_services/roles    Roles follow best practices regarding allowing issuance for localhost domains.


role_allows_glob_wildcards
--------------------------
status    endpoint               message
------    --------               -------
ok        /pki_services/roles    Roles follow best practices regarding restricting wildcard certificate issuance in roles.


role_no_store_false
-------------------
status           endpoint                                    message
------           --------                                    -------
informational    /pki_services/roles/tls-server-superzone    Role currently stores every issued certificate (no_store=false). With auto-rebuild CRL enabled, less performance impact occur on CRL rebuilding, but note that too many issued and/or revoked certificates can exceed OpenBao's storage limits and make operations slow. It is suggested to limit the number of certificates issued under roles with no_store=false: use shorter lifetimes to avoid revocation and/or BYOC revocation instead.


audit_visibility
----------------
status           endpoint                         message
------           --------                         -------
informational    /sys/mounts/pki_services/tune    Mount currently HMACs csr because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs certificate because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs issuer_ref because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs common_name because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs alt_names because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs other_sans because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs ip_sans because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs uri_sans because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs ttl because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs not_after because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs serial_number because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs key_type because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs private_key_format because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs managed_key_name because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs managed_key_id because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs ou because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs organization because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs country because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs locality because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs province because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs street_address because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs postal_code because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs permitted_dns_domains because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs policy_identifiers because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs ext_key_usage_oids because it is not in audit_non_hmac_request_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs certificate because it is not in audit_non_hmac_response_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs issuing_ca because it is not in audit_non_hmac_response_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs serial_number because it is not in audit_non_hmac_response_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs error because it is not in audit_non_hmac_response_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.
informational    /sys/mounts/pki_services/tune    Mount currently HMACs ca_chain because it is not in audit_non_hmac_response_keys; as this is not a sensitive security parameter, it is encouraged to disable HMACing to allow better auditing of the PKI engine.


allow_if_modified_since
-----------------------
status           endpoint                         message
------           --------                         -------
informational    /sys/mounts/pki_services/tune    Mount hasn't enabled If-Modified-Since Request or Last-Modified Response headers; consider enabling these headers to allow clients to fetch CAs and CRLs only when they've changed, reducing total bandwidth.


enable_auto_tidy
----------------
status           endpoint                          message
------           --------                          -------
informational    /pki_services/config/auto-tidy    Auto-tidy is currently disabled; consider enabling auto-tidy to execute tidy operations periodically. This helps the health and performance of a mount.


tidy_last_run
-------------
status      endpoint                     message
------      --------                     -------
critical    /pki_services/tidy-status    Tidy hasn't run since this mount was created; this can point to problems with the mount's auto-tidy configuration or an external tidy executor; this can impact PKI's and OpenBao's performance if not run regularly. It is suggested to enable auto-tidy on this mount.


too_many_certs
--------------
status    endpoint               message
------    --------               -------
ok        /pki_services/certs    This mount has an OK number of stored certificates.


enable_acme_issuance
--------------------
status           endpoint                     message
------           --------                     -------
informational    /pki_services/config/acme    Consider enabling ACME support to support a self-rotating PKI infrastructure.


allow_acme_headers
------------------
status            endpoint                     message
------            --------                     -------
not_applicable    /pki_services/config/acme    ACME is not enabled, no additional response headers required.

## Tidy configuration 
Tidy stores delivered certificates, revoked certificates, issuers, and ACME objects
interval_duration specify the tidy run to erase non necessary objects.
safety_buffer

Now configury tidy : 

bao write pki_services/config/auto-tidy \
  enabled=true \
  interval_duration="24h" \
  safety_buffer="72h" \
  tidy_cert_store=true \
  tidy_revoked_certs=true \
  tidy_expired_issuers=false \
  tidy_revoked_cert_issuer_associations=false \
  tidy_acme=true

checker la configuration : 
bao read pki_services/config/auto-tidy

output : 
Key                                         Value
---                                         -----
acme_account_safety_buffer                  2592000
enabled                                     true
interval_duration                           24h
issuer_safety_buffer                        31536000
maintain_stored_certificate_counts          false
page_size                                   1000
pause_duration                              0s
publish_stored_certificate_count_metrics    false
revoked_safety_buffer                       259200
safety_buffer                               259200
tidy_acme                                   true
tidy_cert_store                             true
tidy_expired_issuers                        false
tidy_invalid_certs                          false
tidy_move_legacy_ca_bundle                  false
tidy_revoked_cert_issuer_associations       false
tidy_revoked_certs                          true

## Authorize conditional cache for CA and CRL

Eviter au clients d'utiliser if-modified-since, ce qui évite de retélécharger une CA ou une crl inchangée

bao secrets tune \
  -passthrough-request-headers="If-Modified-Since" \
  -allowed-response-headers="Last-Modified" \
  pki_services/

check configuration : 
bao read sys/mounts/pki_services/tune

Key                            Value
---                            -----
allowed_response_headers       [Last-Modified]
default_lease_ttl              720h
description                    CA émettrice des certificats de services .superzone.com
force_no_cache                 false
max_lease_ttl                  8760h
passthrough_request_headers    [If-Modified-Since]

## set cluster PKI url 
path = api du moteru pki
aia_path = adresse publique utilisée dans les certificats CA, CRL et OSCP

bao write pki_services/config/cluster \
  path="https://openbao.superzone.com:8200/v1/pki_services" \
  aia_path="https://openbao.superzone.com:8200/v1/pki_services"

## set url with templating 
Cela permettra de remplacer automatiquement openbao avec l'id du bon issuer, fonctionnement assuré malgré la futur rotation de la CA Openbao

bao write pki_services/config/urls \
  enable_templating=true \
  issuing_certificates='{{cluster_aia_path}}/issuer/{{issuer_id}}/der' \
  crl_distribution_points='{{cluster_aia_path}}/issuer/{{issuer_id}}/crl/der' \
  ocsp_servers='{{cluster_aia_path}}/ocsp'


output : 
Key                              Value
---                              -----
crl_distribution_points          [{{cluster_aia_path}}/issuer/{{issuer_id}}/crl/der]
delta_crl_distribution_points    []
enable_templating                true
issuing_certificates             [{{cluster_aia_path}}/issuer/{{issuer_id}}/der]
ocsp_servers                     [{{cluster_aia_path}}/ocsp]

verifier la configuration : 
bao read pki_services/config/cluster

output :
Key         Value
---         -----
aia_path    https://openbao.superzone.com:8200/v1/pki_services
path        https://openbao.superzone.com:8200/v1/pki_services

checker les url : 
bao read pki_services/config/urls

output : 
Key                              Value
---                              -----
crl_distribution_points          [{{cluster_aia_path}}/issuer/{{issuer_id}}/crl/der]
delta_crl_distribution_points    []
enable_templating                true
issuing_certificates             [{{cluster_aia_path}}/issuer/{{issuer_id}}/der]
ocsp_servers                     [{{cluster_aia_path}}/ocsp]

maintenant effectuer un test : 

curl --fail --silent --show-error \
  "https://openbao.superzone.com:8200/v1/pki_services/issuer/909624f4-7d5d-5a6a-62bf-fc6fcfcb72e5/crl/der" \
  --output /tmp/pki-services.crl.der

et vérifiez la configuration : 
openssl crl \
  -inform DER \
  -in /tmp/pki-services.crl.der \
  -noout \
  -issuer \
  -lastupdate \
  -nextupdate

output : 
issuer=C=FR, O=Superzone, OU=PKI, CN=Superzone OpenBao Services Issuing CA 2026
lastUpdate=Aug 25 15:43:56 2026 GMT
nextUpdate=Aug 28 15:43:56 2026 GMT

## enable acme

commencez par checker le role : 
bao read -format=json pki_services/roles/tls-server-superzone |
jq '.data | {
  issuer_ref,
  no_store,
  ttl,
  max_ttl,
  allowed_domains,
  allow_subdomains,
  allow_localhost,
  allow_ip_sans,
  allow_wildcard_certificates,
  key_type,
  key_bits
}'

output :
{
  "issuer_ref": "909624f4-7d5d-5a6a-62bf-fc6fcfcb72e5",
  "no_store": false,
  "ttl": 2592000,
  "max_ttl": 7776000,
  "allowed_domains": [
    "superzone.com"
  ],
  "allow_subdomains": true,
  "allow_localhost": false,
  "allow_ip_sans": false,
  "allow_wildcard_certificates": false,
  "key_type": "ec",
  "key_bits": 384
}

le setting suivant doit etre à false pour configurer acme
no_store = false

maintenant configurez le role tls pour acme et la validité à 48h
bao patch pki_services/roles/tls-server-superzone \
  issuer_ref="default" \
  no_store=false \
  ttl="48h" \
  max_ttl="48h" \
  require_cn=false \
  allow_localhost=false \
  allow_ip_sans=false \
  allow_wildcard_certificates=false

output : 
Key                                   Value
---                                   -----
allow_any_name                        false
allow_bare_domains                    false
allow_glob_domains                    false
allow_globs_in_identity_templates     false
allow_ip_sans                         false
allow_localhost                       false
allow_subdomains                      true
allow_token_displayname               false
allow_wildcard_certificates           false
allowed_domains                       [superzone.com]
allowed_domains_template              false
allowed_ip_sans_cidr                  []
allowed_other_sans                    []
allowed_serial_numbers                []
allowed_uri_sans                      []
allowed_uri_sans_template             false
allowed_user_ids                      []
basic_constraints_valid_for_non_ca    false
client_flag                           false
cn_validations                        [email hostname]
code_signing_flag                     false
country                               []
email_protection_flag                 false
enforce_hostnames                     true
ext_key_usage                         []
ext_key_usage_oids                    []
generate_lease                        false
issuer_ref                            default
key_bits                              384
key_type                              ec
key_usage                             [DigitalSignature]
locality                              []
max_ttl                               48h
no_store                              false
not_after                             n/a
not_after_bound                       ttl-limited
not_before                            n/a
not_before_bound                      duration
not_before_duration                   30s
organization                          []
ou                                    []
policy_identifiers                    []
postal_code                           []
province                              []
require_cn                            false
server_flag                           true
signature_bits                        0
street_address                        []
ttl                                   48h
use_csr_common_name                   true
use_csr_sans                          true
use_pss                               false

autoriser les en têtes ACME
bao secrets tune \
  -passthrough-request-headers="If-Modified-Since" \
  -allowed-response-headers="Last-Modified" \
  -allowed-response-headers="Replay-Nonce" \
  -allowed-response-headers="Link" \
  -allowed-response-headers="Location" \
  pki_services/

maintenant activez acme de manière restrictive

bao write pki_services/config/acme \
  enabled=true \
  allowed_issuers="909624f4-7d5d-5a6a-62bf-fc6fcfcb72e5" \
  allowed_roles="tls-server-superzone" \
  default_directory_policy="forbid" \
  eab_policy="always-required" \
  allow_role_ext_key_usage=false

Il faudra ensuite générer un EAB pour un serveur ou un service :
EAB = autorisation initiale pour certbot de créer son compte ACME 

bao write -format=json -f \
  pki_services/roles/tls-server-superzone/acme/new-eab |
jq '.data | {
  id,
  key,
  acme_directory,
  created_on
}'

output : 
{
  "id": "c4a6c9ca-8a6e-d1ed-274b-c73067020a62",
  "key": "vault-eab-0-5mVhjvx_P7nJ3AqlIJrMBtH3zpRtwiT2dy2LYi5kwfk",
  "acme_directory": "roles/tls-server-superzone/acme/directory",
  "created_on": "2026-08-25T18:11:59+02:00"
}

Explication :

allowed_issuers : seule ta CA OpenBao peut signer via ACME ;
allowed_roles : seul ton rôle TLS serveur est exposé ;
default_directory_policy=forbid : interdit le répertoire générique potentiellement trop permissif ;
eab_policy=always-required : chaque nouveau compte Certbot doit être autorisé par OpenBao ;
allow_role_ext_key_usage=false : les certificats ACME reçoivent uniquement ServerAuth.

Lors de la future rotation de l’issuer, il faudra ajouter/remplacer son UUID dans allowed_issuers.

auto certificate renewal

bao secrets tune \
  -passthrough-request-headers="If-Modified-Since" \
  -allowed-response-headers="Last-Modified" \
  -allowed-response-headers="Replay-Nonce" \
  -allowed-response-headers="Link" \
  -allowed-response-headers="Location" \
  pki_services/
