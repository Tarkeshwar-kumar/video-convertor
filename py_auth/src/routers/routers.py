from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from starlette import status
from database import Session
from modles import User
from helpers import generate_uuid, UserRequest
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


router = APIRouter()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class EmailRequestForm:
    def __init__(self, email: str = Form(...), password: str = Form(...)):
        self.email = email
        self.password = password

def verify_password(password, entered_password):
    return password == entered_password
   
db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'email': email, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

SECRET_KEY = "4a25a6b3ff9818b68ec176a476e45a09b38a9e551eb544d3264870d1ac25858d"
ALGORITHM = 'HS256'



user_dependency = Annotated[dict, Depends(get_current_user)]

def authenticate_user(email: str, password:str, db: db_dependency):
    user = db.query(User).filter(User.email==email).first()
    if user is None:
        HTTPException(
            status_code=401,
            detail="User not found"
        )
    return user

def create_token(email: str, user_id: str, role: str, expiration: timedelta):
    claims = {
        'sub': email, 
        'id': user_id, 
        'role': role,
        "exp": datetime.now(timezone.utc)+ expiration
    }
    return jwt.encode(claims=claims, algorithm=ALGORITHM, key=SECRET_KEY)

    

@router.get("/users", status_code=status.HTTP_200_OK)
async def getUsers(db: db_dependency):
    try:
        res = db.query(User).all()
    except Exception as ex:
        return HTTPException(status_code=500, detail="Internal server error")
    return {
        f"message": "Fetching all users",
        "res": res
    }

@router.get("/user", status_code=status.HTTP_200_OK)
async def getUser(user: user_dependency):
    if user is None:
        HTTPException(
            status_code=401,
            detail="User is not authorised"
        )
    return user

@router.post("/user/signup", status_code=status.HTTP_201_CREATED)
async def createUser(db: db_dependency, user_request: UserRequest):
    user = User(
        id=generate_uuid(),  
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        email=user_request.email,
        password=user_request.password,
        user_type=user_request.user_type,
        age=user_request.age,
        token=None,
        refresh_token=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(user)
    db.commit()

 
@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser():
    pass

@router.post("/user/login", status_code=status.HTTP_201_CREATED)
async def login(form_data: Annotated[EmailRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.email, form_data.password, db)
    if verify_password(user.password, form_data.password):
        token = create_token(form_data.email, user.id, user.user_type, timedelta(minutes=120))
        
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
    
    return {
        "token": token
    }