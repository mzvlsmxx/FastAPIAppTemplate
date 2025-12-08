if __name__ != '__main__':
    from fastapi import FastAPI
    # from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    
    from utils import NoCacheStaticFiles
    
    
    app = FastAPI()
    templates = Jinja2Templates(directory="templates")

    import endpoints

    for router in endpoints.routers:
        app.include_router(router)

    app.mount("/static", NoCacheStaticFiles(directory="static"), name="static")

