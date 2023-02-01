from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_test_result,
    retrieve_test_results,
    delete_test_result
)

from server.models.student import (
    ErrorResponseModel,
    ResponseModel,
)

router = APIRouter()

@router.post("/", response_description="Random data added into the database")
async def add_test_result_data(test_result: dict[str, str]):
    # data = jsonable_encoder(test_result)
    new_data = await add_test_result(test_result)
    return ResponseModel(new_data, "Data added successfully.")

@router.get("/", response_description="Data retrieved")
async def get_test_results():
    results = await retrieve_test_results()
    if results:
        return ResponseModel(results, "Results data retrieved successfully")
    return ResponseModel(results, "Empty list returned")

@router.delete("/{id}", response_description="Random data deleted from the database")
async def delete_test_data(id: str):
    deleted_result = await delete_test_result(id)
    if deleted_result:
        return ResponseModel(
            "Data with ID: {} removed".format(id),
            "Data deleted successfully",
        )
    return ErrorResponseModel(
        "An error occured",
        502,
        "Data with ID {} doesn't exist".format(id),
    )