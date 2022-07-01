#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query

app = FastAPI()

#models

class Person(BaseModel):
  first_name: str
  last_name: str
  age: int
  hair_color: Optional[str] = None
  is_married: Optional[bool] = None

@app.get('/')
def home():
  return {"message":"Hola Mundo Perro!!"}

#request and response

@app.post('/person/new')
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

@app.get('/person/detail')
def show_person(
  name: Optional[str] = Query(None, min_length=1, max_length=50),
  age: Optional[str] = Query(...)
):
  return {name: age}