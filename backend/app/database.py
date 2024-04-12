from os import getenv
from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key

from .models import UserInDB

user_table = resource("dynamodb",
				aws_access_key_id=getenv("AWS_ACCES_KEY_ID"),
				aws_secret_access_key=getenv("AWS_SECRET_ACCES_KEY"),
				region_name=getenv("REGION_NAME")
).Table("users_table")

def init_test_user():
	response = user_table.put_item(
		Item={
			"user_id": "2212bb96-f13e-4e97-a5e9-bf3f329d0c48",
			"username": "johndoe",
			"email": "johndoe@example.com",
			"hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
			"disabled": False,
		}
	)
	print(f"Insert item: {response}") 

def create_new_user(new_user: UserInDB):
	response = user_table.put_item(Item=new_user)
	status_code = response['ResponseMetadata']['HTTPStatusCode']

	return status_code



def get_user_from_db(username: str) -> UserInDB | None:
    """
    Checks if a user exists in the database and returns the user data if found.

    Args:
        username: The username of the user to search for.

    Returns:
        A UserInDB object containing the user data if found, otherwise None.
    """

    response = user_table.scan(
		FilterExpression=Attr("username").eq(username)
	)
    if response.get("Count") == 0:
        return None

    items = response.get("Items")
    return UserInDB(**items[0])