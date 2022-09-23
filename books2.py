from fastapi import FastAPI,HTTPException,Request, status, Form, Header
from pydantic import BaseModel,Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse



class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return

app=FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book", max_length=100, min_length=1)
    rating: int = Field(gt=-1, lt=101) #0~100

    class Config:
        schema_extra={
            "example":{
                "id":"cc3239b7-3506-430a-9c72-624bcf9d2d21",
                "title":"Computer",
                "author":"me",
                "description":"this is mine",
                "rating":57
            }
        }

class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=100,
                                       min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "id": "cc3239b7-3506-430a-9c72-624bcf9d2d21",
                "title": "Computer",
                "author": "me",
                "description": "this is mine"
            }
        }



BOOKS=[]

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request:Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message":f"read more book {exception.books_to_return}"}
    )

#add / after login make it query parameter
#book_id is referencung location of the book not UUID
#username and password is optional because we still get data if it is empty.
@app.post("/books/assignment/login/")
async def book_login_assinment(book_id:int, username: Optional[str] = Header(None), password: Optional[str] = Header(None)):
    if username == "FastAPIUser" and password == "test1234":
        return BOOKS[book_id]
    return 'Invalid User'

@app.post("/books/login")
async def book_login(username: str = Form(), password: str = Form()):
    return {"username":username, "password":password}

@app.get("/header")
async def read_header(random_header: Optional[str]=Header(None)):
    return {"Random-Header":random_header}

@app.get("/")
async def read_all_books(books_to_return: Optional[int]=None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)
    if len(BOOKS)<1:
        create_books_no_api()
    if books_to_return and len(BOOKS)>=books_to_return>0:
        i=1
        new_books=[]
        while i <=books_to_return:
            new_books.append(BOOKS[i - 1])
            i+=1
        return new_books
    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id:UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id:UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book:Book):
    BOOKS.append(book)
    return book

@app.put("/{book_id}")
async def update_book(book_id:UUID, book:Book):
    counter=0

    for x in BOOKS:
        counter +=1
        if x.id ==book_id:
            BOOKS[counter-1]=book
            return BOOKS[counter -1]
    raise raise_item_cannot_be_found_exception()

@app.delete("/{book_id}")
async def delete_book(book_id:UUID):
    counter=0
    for x in BOOKS:
        counter +=1
        if x.id ==book_id:
            del BOOKS[counter-1]
            return BOOKS
    raise raise_item_cannot_be_found_exception()



def create_books_no_api():
    book_1=Book(id="dd883b98-70a3-4281-9f74-6fbca2de1d71",
                title="title_one",
                author="author_1",
                description="description1",
                rating=100)

    book_2=Book(id="3718352a-fe47-4889-a6c2-deaa7fb0b786",
                title="title_2",
                author="author_2",
                description="description2",
                rating=70)

    book_3=Book(id="883a959d-2c1c-4bf7-86dd-04c577cd0fab",
                title="title_3",
                author="author_3",
                description="description3",
                rating=80)

    book_4=Book(id="e61c3ae3-2c78-4151-9dd1-8e1c8ce98142",
                title="title_4",
                author="author_4",
                description="description4",
                rating=10)

    book_5=Book(id="07ed8037-dd4f-4f77-a10e-3f883268f0f2",
                title="title_5",
                author="author_5",
                description="description5",
                rating=0)

    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
    BOOKS.append(book_5)



def raise_item_cannot_be_found_exception():
    return  HTTPException(status_code=404, detail="Book not found",
                        headers={"X-Header-Error":
                                 "Noting to be seen at UUID"})


