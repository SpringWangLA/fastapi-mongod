from bson.objectid import ObjectId
import motor.motor_asyncio
from server.config import settings


MONGO_DETAILS = settings.DATABASE_URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

print('Connected to DB...')

database = client.students
functional_db = client.ft

student_collection = database.get_collection("students_collection")
ft_collection = functional_db.get_collection("ft1")
#helpers

def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }

def result_helper(result) -> dict:
    return {
        **{
            "id": str(result["_id"])
        },
        **{
            key:value for (key,value) in result.items() if key != "_id"
        }
    }

# Retrieve all students present in the database
async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


# Add a new student into to the database
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


# Retrieve a student with a matching ID
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


# Update a student with a matching ID
async def update_student(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_student:
            return True
        return False


# Delete a student from the database
async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True

# Create a randomly data
async def add_test_result(test_result: dict) -> dict:

    result = await ft_collection.insert_one(test_result)
    new_result = await ft_collection.find_one({"_id": result.inserted_id})
    return result_helper(new_result)
    
# Retrieve all random data present in the database
async def retrieve_test_results():
    results = []
    async for result in ft_collection.find():
        results.append(result_helper(result))
    return results

# Delete a student from the database
async def delete_test_result(id: str):
    result = await ft_collection.find_one({"_id": ObjectId(id)})
    if result:
        await ft_collection.delete_one({"_id": ObjectId(id)})
        return True