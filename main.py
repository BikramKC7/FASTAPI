from fastapi import FastAPI,Path,status,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal

app = FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="ID of the patient",examples=['POO'])]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description="City where patient live")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the Patient")]
    gender:Annotated[Literal['male','female','others'],Field(...,description="Gender of the Patients")]
    height:Annotated[float,Field(...,gt=0,description="Height of the patient in mtr")]
    weight:Annotated[float,Field(...,description="Weight of the patient in mtr")]
    
    @computed_field
    @property
    def bmi(self) ->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return 'Under Weight'
        elif self.bmi <25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
    

def load_data():
    with open('patients.json','r')as f:
        data = json.load(f)
        
    return data

def save_data(data):
    with open('patients.json','w')as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {"message":"Patients Management System API"}

@app.get("/about")
def about():
    return({"msg":"A fully functional API to manage your patient records"})

@app.get("/view")
def view():
    data = load_data()
    
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description='ID of the patient in the DB',example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Patient not found')
    
@app.get('sort/')
def sort_patients(sort_by:str=Query(...,description='Sort on the basis of height,weight or bmi'),order: str = Query('asc',description='Sort in asc or desc order')):
    valid_fields = ['height','weight','bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid order select between ascendign and descending')
    
    data = load_data() 
    
    sort_order = True if order == 'desc' else False
    
    sorted_data = sorted(data.values(),key=lambda x : x.get(sort_by,0),reverse=sort_order)
    
    return sorted_data
        
        
@app.post('/create')
def create(patient: Patient):
    #load existing all data
    data = load_data()
    
    #check if the coming id is already exists in database if yes error
    if patient.id in data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Patients already exist")
    
    # else new patient add to the database
     # Note patient up thers is python object and data down below is python dict
    data[patient.id]=patient.model_dump(exclude=['id'])
    
    # save into json file
    save_data(data)
    
    return JSONResponse(status_code=status.HTTP_201_CREATED,content={'msg':'patients created successfully'})

 
    
    