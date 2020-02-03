from flask_admin import AdminIndexView

from .util import ExtraCss

class AdministratorIndexView(AdminIndexView, ExtraCss):
    pass
