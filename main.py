#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#models

class Person(BaseModel):
  first_name: str
  last_name: str
  age: int
  hair_color: Optional[str] = None
  is_married: Optional[bool] = None

@app.get("/")
def home():
  return {"message":"Hola Mundo Perro!!"}

#request and response

@app.post("/person/new")
def create_person(person: Person = Body(...)):
  return person

#validations: query parameters
#validate strings
# max_length
# min_length
# regex
#validate int
# ge -> great or equal than >=
# le -> less or equal than <=
# gt -> greater than >
# lt -> less than <
#documentation in query params
#title
#description

@app.get("/person/detail")
def show_person(
  name: Optional[str] = Query(
    None,
    min_length=1,
    max_length=50,
    title="Person Name",
    description="This is the person name. It's between 1 and 50 characters"
  ),
  age: Optional[str] = Query(
    ...,
    title="Person Age",
    description="This is the person age. It's required"
  )
):
  return {name: age}

#validations path_parameters

@app.get("/person/detail/{person_id}")
def show_person(
  person_id: int = Path(
    ...,
    gt=0,
    title="Person Id",
    description="This is the person id. It's required"
  )
):
  return {person_id: "It exists!"}