#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI, UploadFile
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, File


app = FastAPI()

# Models

class HairColor(Enum): 
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel): 
    city: str
    state: str
    country: str

class PersonBase(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Miguel"
        )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Torres"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)

class Person(PersonBase): 
    password: str = Field(..., min_length=8)

    # class Config: 
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Facundo",
    #             "last_name": "García Martoni",
    #             "age": 21, 
    #             "hair_color": "blonde",
    #             "is_married": False
    #         }
    #     }

class PersonOut(PersonBase): 
    pass

class LoginOut(BaseModel): 
    username: str = Field(..., max_length=20, example="miguel2021")
    message: str = Field(default="Login Succesfully!")

@app.get(
  path="/",
  status_code=status.HTTP_200_OK,
  tags=["Home"]
)
def home(): 
    return {"Hello": "World"}

# Request and Response Body

@app.post(
  path="/person/new",
  response_model=PersonOut,
  status_code=status.HTTP_201_CREATED,
  tags=["Person"],
  summary="Create Person in the app"
)
def create_person(person: Person = Body(...)):
  """
  Create Person

  This function
  - Parameters
  - Resultado
  """ 
  return person

# Validaciones: Query Parameters

@app.get(
  path="/person/detail",
  tags=["Person"],
  deprecated=True
)
def show_person(
  name: Optional[str] = Query(
      None,
      min_length=1, 
      max_length=50,
      title="Person Name",
      description="This is the person name. It's between 1 and 50 characters",
      example="Rocío"
      ),
  age: str = Query(
      ...,
      title="Person Age",
      description="This is the person age. It's required",
      example=25
      )
): 
    return {name: age}

# Validaciones: Path Parameters

persons=[1,2,3,4,5]

@app.get(
  "/person/detail/{person_id}",
  status_code=status.HTTP_200_OK,
  tags=["Person"]
)
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=5
        )
): 
  if person_id not in persons:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="¡This person doesn't exists!"
    )
  return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put(
  path="/person/{person_id}",
  status_code=status.HTTP_201_CREATED,
  tags=["Person"]  
)
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
): 
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person

@app.post(
  path="/login",
  response_model=LoginOut,
  status_code=status.HTTP_200_OK,
  tags=["Login","Person"]
)
def login(username: str = Form(...), password: str = Form(...)):
  return LoginOut(username=username)

@app.post(
  path="/contact",
  status_code=status.HTTP_200_OK,
  tags=["Contact"]
)
def contact(
  first_name: str = Form(
    ...,
    max_length=20,
    min_length=1,
  ),
  last_name: str = Form(
    ...,
    max_length=20,
    min_length=1,
  ),
  email: str = Form(...),
  message: str = Form(
    ...,
    min_length=20
  ),
  user_agent: Optional[str] = Header(default=None),
  ads: Optional[str] = Cookie(default=None)
):
  return user_agent

@app.post(
  path="/post-image",
  tags=["File"]
)
def post_image(
  image: UploadFile = File(...)
):
  return {
    "Filename":image.filename,
    "Format":image.content_type,
    "Size(kb)":round(len(image.file.read())/1024,ndigits=2)
  }