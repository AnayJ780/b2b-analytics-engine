from fastapi import FastAPI, UploadFile, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd
from io import StringIO
from database import get_db, engine, Base
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
import auth
import schemas 
import models

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind = engine)
app = FastAPI(title = 'B2B E-Commerce Analytics')
@app.get("/")
def read_root():
    return {"status": "Success", "message": "B2B Analytics API is running live!"}
def process_csv_data(csv_content:str, merchant_id:int, db:Session):
    try:
        df = pd.read_csv(StringIO(csv_content))
        for index, row in df.iterrows():
            new_record = models.SalesRecord(
                product_name=row['product_name'],
                quantity_sold=row['quantity'],
                revenue=row['revenue'],
                merchant_id=merchant_id 
            )
            db.add(new_record)
        db.commit()
    except Exception as e:
        print(f"Failed to process CSV for merchant {merchant_id}: {e}")

from pydantic import BaseModel

# 1. Define the shape of the data we expect from a new user
class MerchantCreate(BaseModel):
    company_name: str
    password: str

# 2. Create the Signup Route
@app.post("/api/v1/signup")
def create_merchant(merchant: MerchantCreate, db: Session = Depends(get_db)):
    # Check if this company name is already taken
    existing_merchant = db.query(models.Merchant).filter(
        models.Merchant.company_name == merchant.company_name
    ).first()
    
    if existing_merchant:
        raise HTTPException(status_code=400, detail="Company already registered")
    
    # Hash the password securely using your auth file
    hashed_password = auth.get_password_hash(merchant.password)
    
    # Save the new merchant to PostgreSQL
    new_merchant = models.Merchant(
        company_name=merchant.company_name, 
        api_key=hashed_password
    )
    db.add(new_merchant)
    db.commit()
    
    return {"message": f"Successfully created merchant: {merchant.company_name}. You can now log in."}

@app.post('/api/v1/login', response_model = dict)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()):
    merchant = db.query(models.Merchant).filter(
        models.Merchant.company_name == form_data.username).first()

    if not merchant or not auth.verify_password(form_data.password, merchant.api_key):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},)

    access_token = auth.create_access_token(
        data = {'sub': str(merchant.id)}
    )
    return {'access_token' : access_token , 'token_type': 'bearer'}


@app.post("/api/v1/upload-sales/")
async def upload_sales_csv(
    file: UploadFile, 
    background_tasks: BackgroundTasks, # FastAPI injects the background task manager
    db: Session = Depends(get_db),
    current_merchant_id: int = Depends(auth.get_current_merchant_id)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    # Read the file into memory while the user waits
    content = await file.read()
    csv_text = content.decode("utf-8")
    
    
    # Hand the heavy lifting off to the background worker
    background_tasks.add_task(process_csv_data, csv_text, current_merchant_id, db)
    
    # Immediately return a 200 OK status to the client, preventing browser timeouts
    return {
        "status": "success",
        "message": "File accepted. Data is being processed in the background."
    }

@app.get('/api/v1/analytics/overview')
def get_analytics_overview(
    db:Session = Depends(get_db),
    current_merchant_id :int = Depends(auth.get_current_merchant_id)
):
    total_revenue = (db.query(func.sum(models.SalesRecord.revenue))
    .filter(models.SalesRecord.merchant_id == current_merchant_id)
    .scaler () or 0.0)

    total_units = (
        db.query(func.sum(models.SalesRecord.quantity_sold))
        .filter(models.SalesRecord.merchant_id == current_merchant_id)
        .scalar() or 0.0
    )

    best_product_record = (
        db.query(
            models.SalesRecord.product_name,
            func.sum(models.SalesRecord.quantity_sold).label('total_qty')
        )
        .filter(models.SalesRecord.merchant_id == current_merchant_id)
        .group_by(models.SalesRecord.product_name)
        .order_by(func.sum(models.SalesRecord.quantity_sold).desc())
        .first()
    )

    best_product = best_product_record.product_name if best_product_record else "No Data"

    return {
        'merchant_id': current_merchant_id,
        'total_revenue': total_revenue,
        'total_units_sold': total_units,
        'best_selling_products': best_product
    }



