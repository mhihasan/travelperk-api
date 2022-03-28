from typing import TypedDict

TProduct = TypedDict("TProduct", {"code": str, "name": str, "price": float})

TUser = TypedDict("TUser", {"id": str, "firstName": str, "lastName": str})
