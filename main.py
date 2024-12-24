from fastapi import FastAPI

from routes.weather import router as wea_router

app=FastAPI(
    title="Weather-Api",
description="Weather Forcast Application.",
contact={
    "name": "M.Waqas",
    "email": "abdullahwaqas22@gmail.com"

},
license_info={
    "name": "Associate Software Engineer"
}
)

app.include_router(wea_router)