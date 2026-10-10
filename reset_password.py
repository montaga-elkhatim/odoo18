import odoo
from odoo import api, SUPERUSER_ID

DB_NAME = "school_g6sb"
LOGIN = "admin"
NEW_PASSWORD = "montaga"

registry = odoo.registry(DB_NAME)

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})

    user = env["res.users"].search(
        [("login", "=", LOGIN)],
        limit=1
    )

    if user:
        user.write({"password": NEW_PASSWORD})
        cr.commit()
        print("Password reset successfully for:", LOGIN)
    else:
        print("User not found:", LOGIN)