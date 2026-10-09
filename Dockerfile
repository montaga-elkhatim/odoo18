FROM odoo:18.0

USER root

COPY odoo.conf /etc/odoo/odoo.conf

USER odoo

CMD ["odoo", "-c", "/etc/odoo/odoo.conf", "-i", "base", "--stop-after-init"]
