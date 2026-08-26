# syntax=docker/dockerfile:1

FROM grafana/grafana

# Copy modified grafana.ini in grafa directory
COPY grafana.ini /etc/grafana

COPY datasources.yml /etc/grafana/provisioning/datasources
