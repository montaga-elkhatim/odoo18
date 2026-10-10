FROM odoo:18.0

USER root

COPY odoo.conf /etc/odoo/odoo.conf
COPY reset_password.py /tmp/reset_password.py

USER odoo

CMD ["python3", "/tmp/reset_password.py"]
