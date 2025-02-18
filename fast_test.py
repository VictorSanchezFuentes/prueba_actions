from typing import Optional
from typing import List
from fastapi import Body, FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pathlib import Path
from fastapi.openapi.utils import get_openapi
import os


app = FastAPI(
    title="My API with documentation",
    description="This is a dummy API project, created to test FastApi and its documentation.",
    version="0.1.0",
    contact={
        "name": "Víctor Sánchez/Alejandro García",
        "url": "https://blog.com/@test",
        "email": "proyect@thisisnotmyemail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://something.org/licenses/doesnt/exist",
    },
    redoc_options={
        "hide-hostname": True,
        "expand-responses": "200,201",
        "theme": {
            "colors": {
                "primary": {
                    "main": "#00008b"
                }
            }
        }
    },
    
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai"
    }
    )



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://www.capgemini.com/es-es/wp-content/uploads/sites/16/2022/12/Invent_Logo_2COL_CMYK-1.jpg"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi



class Item(BaseModel):
    text: str | None= Field(
        default=None, title="The name of the item", max_length=300
    )
    is_done: bool = False
    price: float = Field(
        gt=0, description="The price of the item. It must be greater than zero"
    )

items = [{
    "text": "string",
    "is_done": True,
    "price": 1.7
    }] 



@app.get("/", tags=["get"])
def root():
    return {"Hello": "World"}


@app.post("/items", description=Path("./post_items_itemid.md").read_text(), summary="Post food item", tags=["post"])
def create_item(item : Item = Query(None, description="Item to search")):
    """
    Adds the item based on a query of text and is_done to the existing lists of items
    and returns the existing list after the addition

    - **item**: A piece of food with information about its name and its done status
    """
    items.append(item)
    return items

@app.get("/items", response_model=list[Item], tags=["get"])
def list_item(limit: Optional[int] = 10):
    return items[0:limit]


@app.get("/items/{item_id}", response_model=Item, tags=["get"], responses={404: {"description": f"Item not found"}})
def get_single_item(item_id : int) -> Item:
    
    if item_id < len(items):
        return items[item_id]
    return JSONResponse(status_code=404, content={"message": f"Item {item_id} not found"}) 
    """else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    """


@app.get("/get_mode")
def get_mode():
    return os.environ.get("MODE")


"""
<to run the app, open a terminal and run the command: <uvicorn fast_test:app --reload
"""


