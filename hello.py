from fastapi import FastAPI,HTTPException,status
import json
from pydantic import BaseModel,computed_field,Field,model_validator
from typing import Annotated,Dict

app = FastAPI()

def load_data():
    with open('student.json','r')as f:
        data = json.load(f)
        
    return data


def save_data(data):
    with open('student.json','w')as f:
        json.dump(data,f)

class Student(BaseModel):
    id:Annotated[str,Field(...,description="Unique Id of the students")]
    name:Annotated[str,Field(...,description="Name of the Student")]
    grade:Annotated[int,Field(...,description="Grade of the Student")]
    section:Annotated[str,Field(...,description="Grade of the studnets",examples=['Rosy','Pansy'])]
    contact:Annotated[Dict[str,str],Field(...,description="Contact Details of the student")]
    math_m:Annotated[float,Field(...,description="Math marks of the student")]
    science_m: Annotated[float,Field(...,description="Science marks of the student")]
    
    @model_validator(mode="after")
    def validate_emergency_contact(cls,model):
        if model.grade < 8 and 'emergency' not in model.contact:
            raise ValueError("Emergency Number required for below class 8 compulsory")
        
        return model
    
    @computed_field
    @property
    def percentage(self) -> float:
        percentage = (self.math_m + self.science_m)/200 * 100
        return percentage
    
    

@app.post('/create')
def create(student:Student):
    data = load_data()
    if student.id in data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={'msg':'Already Present'})
    
    data[student.id]=student.model_dump(exclude=['id'])
    
    save_data(data)
    
    
    

