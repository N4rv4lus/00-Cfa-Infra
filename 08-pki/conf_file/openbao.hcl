# Full configuration options can be found at https://openbao.org/docs/configuration

ui = true

#mlock = true
#disable_mlock = true

storage "file" {
  path = "/var/lib/openbao"
}

#storage "consul" {
#  address = "127.0.0.1:8500"
#  path    = "openbao"
#}

api_addr = "https://openbao.superzone.com:8200"
cluster_addr = "https://openbao.superzone.com:8201"

# HTTP listener
#listener "tcp" {
#  address = "0.0.0.0:8200"
#  tls_disable = 1
#}

# HTTPS listener
listener "tcp" {
  address       = "0.0.0.0:8200"
  cluster_addr = "0.0.0.0:8201"

  tls_disable = false
  tls_cert_file = "/etc/openbao/tls/openbao.superzone.com2.fullchain.pem"
  tls_key_file  = "/etc/openbao/tls/openbao.key.pem"

  tls_min_version = "tls12"
  tls_max_version = "tls13"
}

# Example AWS KMS auto unseal
#seal "awskms" {
#  region = "us-east-1"
#  kms_key_id = "REPLACE-ME"
#}

# Example HSM auto unseal
#seal "pkcs11" {
#  lib            = "/usr/openbao/lib/libCryptoki2_64.so"
#  slot           = "0"
#  pin            = "AAAA-BBBB-CCCC-DDDD"
#  key_label      = "openbao-hsm-key"
#  hmac_key_label = "openbao-hsm-hmac-key"
#}