
FROM odoo:18.0

USER root

RUN pip3 install psycopg2-binary

USER odoo
