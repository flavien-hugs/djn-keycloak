from ninja import NinjaAPI, Router


def router_factory(**kwargs) -> Router:
    router = Router(**kwargs)
    return router


class NinjaServiceAPI(NinjaAPI):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
