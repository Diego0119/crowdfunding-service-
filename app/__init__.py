from litestar import Litestar
from litestar.config.cors import CORSConfig
from app.config import settings
from app.database import sqlalchemy_plugin
from app.services.accounts.controllers import accounts_router
from app.services.accounts.security import oauth2_auth
from app.services.funding.controllers import funding_router

# esto permite hacer peticion desde el front, pero no esta funcionando
cors_config = CORSConfig(
    allow_origins=["http://localhost:5500"], 
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True,  
)

app = Litestar(
    route_handlers=[accounts_router, funding_router],
    plugins=[sqlalchemy_plugin],
    on_app_init=[oauth2_auth.on_app_init],
    debug=settings.debug,
    cors_config=cors_config,  
)

for route in app.routes:
    print(f"Route: {route.path}, Method: {route.methods}")
