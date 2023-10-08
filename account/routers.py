from commun.ninja import NinjaServiceAPI
from account.users import router as users_router


users_api = NinjaServiceAPI(
    title="DJN API:: Users API",
    docs_url="/users/docs",
    openapi_url="/users/openapi.json",
)
users_api.add_router("users/", users_router)
