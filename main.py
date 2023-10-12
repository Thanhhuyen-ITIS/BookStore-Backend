from fastapi import  FastAPI
from starlette.middleware.cors import CORSMiddleware

import models
from config.database import engine
from routers import user_route, authentication, book_route, cart_route, order_route, category_route, review_route, \
    comment_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Địa chỉ nguồn gốc của trình duyệt
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Cho phép tất cả các header
)

models.Base.metadata.create_all(engine)

app.include_router(user_route.router)
app.include_router(authentication.router)
app.include_router(book_route.router)
app.include_router(cart_route.router)
app.include_router(order_route.router)
app.include_router((category_route.router))
app.include_router((review_route.router))
app.include_router((comment_route.router))