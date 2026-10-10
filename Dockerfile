FROM odoo:18.0

USER root

COPY odoo.conf /etc/odoo/odoo.conf
COPY custom_addons/ /mnt/extra-addons/

RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo

CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
