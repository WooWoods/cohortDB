from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import crud
import models
import schemas
from database import db
from services import file_handler
from auth import create_access_token, verify_password, get_password_hash, decode_access_token, oauth2_scheme
from datetime import timedelta

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
def startup_event():
    db.connect()
    db.create_tables([
        models.ReportedAges,
        models.BsRate,
        models.Coverage,
        models.Fastp,
        models.Markdup,
        models.PicardAlignmentSummary,
        models.PicardGcBias,
        models.PicardGcBiasSummary,
        models.PicardHs,
        models.PicardInsertSize,
        models.PicardQualityYield,
        models.Screen,
        models.User, # Add User model to tables
    ])
    # Ensure a default admin user exists and its password is up-to-date with the current hashing scheme
    admin_username = "admin"
    admin_password = "admin12345"

    # Delete existing admin user to ensure a clean state with the correct hash scheme
    try:
        admin_user_to_delete = models.User.get(models.User.username == admin_username)
        admin_user_to_delete.delete_instance()
        print(f"Existing admin user '{admin_username}' deleted.")
    except models.User.DoesNotExist:
        pass # No admin user to delete

    # Create a new admin user with the correct hashing scheme
    admin_user_data = schemas.UserCreate(username=admin_username, password=admin_password, is_admin=True)
    hashed_password = get_password_hash(admin_user_data.password)
    crud.create_user(admin_user_data, hashed_password)
    print(f"Default admin user created/recreated: username='{admin_username}', password='{admin_password}'")

@app.on_event("shutdown")
def shutdown_event():
    if not db.is_closed():
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:
    """
    Retrieves the current authenticated user from the JWT token.
    """
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = crud.get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_admin_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    """
    Retrieves the current authenticated user and checks if they are an admin.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
    return current_user

@app.post("/api/v1/auth/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Handles user login and returns a JWT access token.
    """
    user = crud.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/auth/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Retrieves the current authenticated user's information.
    """
    return current_user

@app.post("/api/v1/data/upload")
async def upload_data(file: UploadFile = File(...), current_user: models.User = Depends(get_current_admin_user)):
    try:
        file_handler.process_uploaded_file(file)
        return {"message": "File uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/data/initial")
async def get_initial_data_route(offset: int = 0, limit: int = 20):
    try:
        data = crud.get_initial_data(offset=offset, limit=limit)
        total_count = crud.get_total_data_count()
        return {"data": data, "total_count": total_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/data/download")
async def download_data(samples: str):
    sample_list = [s.strip() for s in samples.split(',')]
    try:
        excel_file = file_handler.generate_excel_file(sample_list)
        return StreamingResponse(excel_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=cohort_data.xlsx"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/data/filter")
async def filter_data(filters: schemas.FilterSchema):
    try:
        data = crud.get_filtered_data(filters)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/data/search")
async def search_data(search_term: str = Form(...)):
    try:
        samples = crud.get_samples_by_search_term(search_term)
        data = crud.get_data_by_samples(samples)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
