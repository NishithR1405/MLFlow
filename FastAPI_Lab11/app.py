from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "mlopssecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_user = {
    "username": "admin",
    "password": "admin123"
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.get("/")
def home():
    return {"message": "Secure FastAPI Application"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or form_data.password != fake_user["password"]:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/secure-data")
def secure_data(token: str = Depends(oauth2_scheme)):
    return {"message": "Access granted to protected route"}
