from urllib.request import Request
from fastapi import FastAPI, HTTPException, status
import models.user_model
from repository.database import engine, get_db
import models.user_model as models, utils.auth as auth
from views import auth_views, category_views, job_views

# Run the database migrations
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()


@app.middleware("http")
async def verify_token(request: Request, call_next):
    if request.url.path == "/token" or request.url.path == "/register":
        response = await call_next(request)
        return response
    token = request.headers.get("Authorization")
    if token:
        token = token.split("Bearer ")[1]
        username = auth.verify_token(token)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        request.state.user = username
    response = await call_next(request)
    return response


app.include_router(auth_views.router, tags=["auth"])
app.include_router(job_views.router, tags=["jobs"], prefix="/jobs")
app.include_router(category_views.router, tags=["categories"], prefix="/categories")

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
