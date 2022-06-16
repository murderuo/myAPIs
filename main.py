from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from  data_read import ExploreData


app = FastAPI()
infilation=ExploreData()
infilation_data=infilation.get_data()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get('/')
def direct():
    return {'url':'/api/v1/infilation'}

@app.get("/api/v1/infilation")
def index():
    return infilation_data


@app.get("/api/v1/infilation/{year_id}")
def get_year_inflation(year_id: int):
    if year_id >= 2005 and year_id <= 2022:
        for d in infilation_data:
            if d["year"] == year_id:
                return d
    else:
        return {"mesaj": "geçersiz yıl bilgisi"}


@app.get("/api/v1/infilation/{year_id}/{month_id}")
def get_month_inflation(month_id: int, year_id: int):
    if year_id >= 2005 and year_id <= 2022:
        year_inflation_data=get_year_inflation(year_id)
        if month_id>=1 and month_id<=12:
            for month_data in year_inflation_data['month']:
                if month_data['month_number']==month_id:
                    return {"year":year_id, "month_data":month_data}
                    # return month_data
        else:
            return {"mesaj": "geçersiz ay bilgisi"}
    else:
        return {"mesaj": "geçersiz yıl bilgisi"}


@app.get("/api/v1/infilation/{year_id}/{month_id}/{value}")
def get_value_infilation(year_id:int,month_id:int,value:str):
    month_infilation_value=get_month_inflation(month_id,year_id )
    # print(month_infilation_value)
    if 'mesaj' in month_infilation_value.keys():
        return {"mesaj": "geçersiz istek"}
    elif month_infilation_value['year']==year_id :
        if value=='year_inflation_value':
            return {'year_inflation_value':month_infilation_value['month_data']['year_inflation_value']}
        elif value=='month_inflation_value':
            return {'month_inflation_value': month_infilation_value['month_data']['month_inflation_value']}
        else:
            return {"mesaj": "geçersiz istek"}
    else:
        return {"mesaj": "geçersiz istek"}




