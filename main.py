if __name__ == "__main__":
    import os
    import uvicorn

    from dotenv import find_dotenv, load_dotenv

    
    load_dotenv(find_dotenv())

    uvicorn.run(
        app="create:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", 7777)),
        workers=int(os.getenv("APP_WORKERS", 1)),
        log_level=os.getenv("APP_LOG_LEVEL", "info"),
        reload=True
    )