from litestar import Litestar

from app.config import settings
from app.database import sqlalchemy_plugin
from app.services.accounts.controllers import accounts_router
from app.services.accounts.security import oauth2_auth
from app.services.funding.controllers import funding_router

app = Litestar(
    route_handlers=[accounts_router, funding_router],
    plugins=[sqlalchemy_plugin],
    on_app_init=[oauth2_auth.on_app_init],
    debug=settings.debug,
)
