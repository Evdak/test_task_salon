from fastapi import Depends, FastAPI
import uvicorn
from controllers.queue import router as QueueRouter

from controllers.masters import router as MasterRouter

from controllers.live_queue import router as LiveQueueRouter

from db.db import User, create_db_and_tables
from schemas.users import UserCreate, UserRead, UserUpdate
from controllers.users import auth_backend, current_active_user, fastapi_users


app = FastAPI()


app.include_router(
    QueueRouter,
    prefix="/queue",
    tags=["queue"]
)


app.include_router(
    LiveQueueRouter,
    prefix="/live_queue",
    tags=["liveQueue"]
)


app.include_router(
    MasterRouter,
    prefix="/master",
    tags=["master"]
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@ app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@ app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
