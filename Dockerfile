FROM odoo:18.0

USER root

RUN pip3 install --break-system-packages psycopg2-binary

USER odoo
