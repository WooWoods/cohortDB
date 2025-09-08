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

    # Ensure a default admin user exists
    admin_user = crud.get_user_by_username(admin_username)
    if not admin_user:
        admin_user_data = schemas.UserCreate(username=admin_username, email="admin@example.com", password=admin_password)
        hashed_password = get_password_hash(admin_user_data.password)
        admin_user = crud.create_user(admin_user_data, hashed_password)
        admin_user.is_admin = True
        admin_user.status = 'approved'
        admin_user.save()
        print(f"Default admin user created: username='{admin_username}', password='{admin_password}'")
    else:
        # ensure the admin password is correct
        if not verify_password(admin_password, admin_user.hashed_password):
            hashed_password = get_password_hash(admin_password)
            admin_user.hashed_password = hashed_password
            admin_user.save()
            print(f"Default admin user password updated.")

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

@app.post("/api/v1/auth/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    return crud.create_user(user=user, hashed_password=hashed_password)

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
    if user.status != 'approved':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not approved",
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

@app.get("/api/v1/admin/users", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, current_user: models.User = Depends(get_current_admin_user)):
    users = crud.get_users(skip=skip, limit=limit)
    return users

@app.post("/api/v1/admin/users/{user_id}/approve", response_model=schemas.User)
async def approve_user(user_id: int, current_user: models.User = Depends(get_current_admin_user)):
    return crud.update_user_status(user_id=user_id, status="approved")

@app.post("/api/v1/admin/users/{user_id}/reject", response_model=schemas.User)
async def reject_user(user_id: int, current_user: models.User = Depends(get_current_admin_user)):
    return crud.update_user_status(user_id=user_id, status="rejected")

@app.post("/api/v1/data/upload")
async def upload_data(file: UploadFile = File(...), current_user: models.User = Depends(get_current_admin_user)):
    try:
        file_handler.process_uploaded_file(file)
        return {"message": "File uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/data/initial")
async def get_initial_data_route(offset: int = 0, limit: int = 20, current_user: models.User = Depends(get_current_user)):
    try:
        data = crud.get_initial_data(offset=offset, limit=limit)
        total_count = crud.get_total_data_count()
        return {"data": data, "total_count": total_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/data/download")
async def download_data(samples: str, current_user: models.User = Depends(get_current_user)):
    sample_list = [s.strip() for s in samples.split(',')]
    try:
        excel_file = file_handler.generate_excel_file(sample_list)
        return StreamingResponse(excel_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=cohort_data.xlsx"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/data/filter")
async def filter_data(filters: schemas.FilterSchema, current_user: models.User = Depends(get_current_user)):
    print(filters)
    try:
        data = crud.get_filtered_data(filters)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/data/search")
async def search_data(search_term: str = Form(...), current_user: models.User = Depends(get_current_user)):
    try:
        samples = crud.get_samples_by_search_term(search_term)
        data = crud.get_data_by_samples(samples)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
