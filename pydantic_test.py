from pydantic import BaseModel,StrictInt,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

# class Patients(BaseModel):
#     name: str = Field(max_length=50)
#     email: EmailStr
#     linkedin: AnyUrl
#     age: StrictInt = Field(gt=0,lt=120)
#     weight : float=Field(gt=0)
#     married: bool
#     allergies: Optional[List[str]] = Field(max_length=3)
#     contact_details:Dict[str,str]
    
# data = {"name":"bikram","age":12, "weight":75.2,'married':True,'allergies':['pollen','dust'],'contact_details':{'email':'normal@gmail.com','phone':'9847074993'}}

# p1 = Patients(**data)

# def pyfun(patient : Patients):
#     print(patient.age)
#     print(patient.name)
#     print(patient.allergies) 
   

# pyfun(p1)
# -------------------------------------------------------------------------------------------------------------------

# class Patient(BaseModel):
#     name: Annotated[str, Field(max_length=50,title='Name of Patient',description='Give the name of patient',examples=['Bikram','Megna'])]
#     email:EmailStr
#     linkedin_url:AnyUrl
#     age:int=Field(gt=0,lt=120)
#     weight: Annotated[float,Field(gt=0,strict=True)]
#     married:Annotated[bool,Field(default=None,description='Is the patient married')]
#     allergies: Annotated[Optional[List[str]],Field(default=None,max_length=5)]
    
# def update_patient_data(patient:Patient):
#     print(patient.married)

# patient_info = {
#     'name':'Bikram',
#     'email':'bikram@gmail.com',
#     'linkedin_url':'http://linkedin.com/132',
#     'age':21,
#     'weight':55.5,
#     'married':True,   
# }

# p1 = Patient(**patient_info)
# update_patient_data(p1)

# --------------------------------field validator----------------------------------------------------------------------------------------------------------------
from pydantic import field_validator


# class Patient(BaseModel):
#     name: str
#     email:EmailStr
#     age:int
#     weight: float
#     married:bool
#     allergies: List[str]
#     contact_details: Dict[str,str]
    
#     @field_validator('email')
#     @classmethod
#     def email_validator(cls,value):
#         valid_domains = ['hdfc.com','icici.com']
#         domain_name = value.split('@')[-1]
#         if domain_name not in valid_domains:
#             raise ValueError("Not a valid domain")
        
#         return value
    
#     @field_validator('name')
#     @classmethod
#     def name_validator(cls,value):
#         value = value.upper()
        
#         return value
    
#     @field_validator('age',mode='after')  
#     before mode value is passed before type conversion if we pass string in age then it will pass as a string and throw error so mode should be after by default
#     @classmethod
#     def age_validator(cls,value):
#         if 0>value>100:
#             raise ValueError("Invalid Age")
#         return value
            
    
# def update_patient_data(patient:Patient):
#     print(patient.married)
#     print(patient.email)
#     print(patient.name)
#     print(patient.age)

# patient_info = {
#     'name':'Bikram',
#     'email':'bikram@hdfc.com',
#     'linkedin_url':'http://linkedin.com/132',
#     'age':21,
#     'weight':55.5,
#     'married':True,
#     'allergies':['pollen grains','egg'],
#     'contact_details':{'phone':'9847074993'}
# }

# p1 = Patient(**patient_info)
# update_patient_data(p1)

# -------------Model validator-----------------------------------------------------

# from pydantic import model_validator

# class Patient(BaseModel):
#     name: str
#     email:EmailStr
#     age:int
#     weight: float
#     married:bool
#     allergies: List[str]
#     contact_details: Dict[str,str]
    
#     @model_validator(mode='after')
#     def validate_emergency_contact(cls,model):
#         if model.age >60 and 'emergency' not in model.contact_details:
#             raise ValueError("Patients older than 60 must have emergency contact")
#         return model
    
    
# def update_patient_data(patient:Patient):
#     print(patient.married)
#     print(patient.email)
#     print(patient.name)
#     print(patient.age)

# patient_info = {
#     'name':'Bikram',
#     'email':'bikram@hdfc.com',
#     'linkedin_url':'http://linkedin.com/132',
#     'age':61,
#     'weight':55.5,
#     'married':True,
#     'allergies':['pollen grains','egg'],
#     'contact_details':{'phone':'9847074993','emergency':'9847074993'}
# }

# p1 = Patient(**patient_info)
# update_patient_data(p1) 


# ------------Computed Fields ----------------------------------------------
# from pydantic import computed_field

# class Patient(BaseModel):
#     name: str
#     email:EmailStr
#     age:int
#     weight: float
#     height: float
#     married:bool
#     allergies: List[str]
#     contact_details: Dict[str,str]
    
#     @computed_field
#     @property
#     def bmi(self)->float:
#         bmi = round(self.weight/(self.height**2),2)
#         return bmi
    
# def update_patient_data(patient:Patient):
#     print(patient.married)
#     print(patient.email)
#     print(patient.name)
#     print(patient.age)
#     print(patient.bmi)

# patient_info = {
#     'name':'Bikram',
#     'email':'bikram@hdfc.com',
#     'linkedin_url':'http://linkedin.com/132',
#     'age':61,
#     'weight':55.5,
#     'height':105,
#     'married':True,
#     'allergies':['pollen grains','egg'],
#     'contact_details':{'phone':'9847074993','emergency':'9847074993'}
# }

# p1 = Patient(**patient_info)
# update_patient_data(p1) 


# --------------------Nested Models ---------------------------------

# from pydantic import BaseModel

# class Address(BaseModel):
#     city:str
#     state:str
#     pin:str

# class Patient(BaseModel):
#     name:str
#     gender:str
#     age:int
#     address:Address
    
# adddress_dict = {
#     'city':'Kathmandu',
#     'state':'Bagmati',
#     'pin':'122412'
# }

# address1 = Address(**adddress_dict)

# patients_dic = {
#     'name':'Bikram',
#     'gender':'Male',
#     'age':21,
#     'address':address1
# }

# patients1 = Patient(**patients_dic)

# print(patients1.address)


# -------------Serialization----------------------------------

from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin:str

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address:Address
    
adddress_dict = {
    'city':'Kathmandu',
    'state':'Bagmati',
    'pin':'122412'
}

address1 = Address(**adddress_dict)

patients_dic = {
    'name':'Bikram',
    'gender':'Male',
    'age':21,
    'address':address1
}

patients1 = Patient(**patients_dic)

temp = patients1.model_dump(include=['name'])  # dump export into python dict  and dump_json export into json
print(temp)
print(type(temp))
