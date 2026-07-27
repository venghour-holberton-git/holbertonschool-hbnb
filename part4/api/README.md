# Authorization and Database Implementation

## Requirements

- Python 3.x
- Flask
- Flask-RESTX
- Flask-SQLAlchemy

This part of the project requires SQLite3. So, please ensure that it is installed in your system. The necessary code is listed below in the order of operations.

Operation of part 3

To get started and using the implementation, please follow the steps listed below:

- Cloning the repo
  
	```
		git clone https://github.com/Ethan-of-Aussie/holbertonschool-hbnb.git
 	```
  
- Navigating to target directory
  
    ```
		cd holbertonschool-hbnb/part3/
    ```

- Creating virtual environment

	```
		python3 -m venv venv
 	```
 
- Activating virtual environment (if Windows)

  	```
  		venv\Scripts\activate
   	```

- Activating virtual environment (if mac or linux)
  
	```
 		source venv/bin/activate
	```

    If you get the following error

    ```
    	bash: venv/bin/activate: No such file or directory
    ```

    Try doing the following

    ```
    	sudo apt update
    ```

    followed by

    ```
    	sudo apt install python3.10-venv
    ```

    Recreate the virutal environment and activate it following the above process after which the next step listed can be followed.

- Installing required packages
  
    ```
    	pip install -r requirements.txt
    ```

- Installing SQLite 3

    For Powershell

    ```
    	winget install SQLite.SQLite
    ```

    For bash

    ```
    	sudo apt install sqlite3
    ```

- Database creation

    ```
    	flask shell
    ```

	followed by within the interpreter that opens

    ```
    	 from app import db
    	 db.create_all()
    ```

- Database population (use when inside part 3 directory)

    For Windows

    ```
    	Get-Content populate_script.sql | sqlite3 instance/development.db
    ```

    For Linux/Mac

    ```
    	sqlite3 instance/development.db < populate_script.sql
    ```

- Running the server
  
	```
    	python3 run.py
  	```
  
Listed below is the Entity Relationship Diagram of our Hbnb clone

```mermaid
erDiagram
    USER ||--o{ PLACE : registers
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : reviewed
    PLACE ||--o{ PLACE_AMENITIY: has
    AMENITY ||--o{ PLACE_AMENITIY: has

    USER {
        string id PK
        string first_name
        string last_name
        string email
        string password
        bool is_admin
    }
    PLACE {
        string id PK
        string title
        string description
        float latitude
        float longitude
        string owner_id FK
    }
    REVIEW {
        string id
        string text
        float rating
        string user_id FK
        string place_id FK
    }
    AMENITY {
        string id PK
        string name
    }
    PLACE_AMENITIY {
        string place_id FK
        string amenity_id FK
    }
```
  
The relationships between each classes of our clone is as follows:

- User has one-to-many relationship with Place.
- User has one-to-many relationship with Review.
- Place has one-to-many relationship with review.
- Place has one-to-many relationship with Place_Amenity.
- Amenity has one-to-many relationship with Place_Amenity.
- Place_Amenity represents a join relationship between Place and Amenity (many-to-many).

Listed below are some example trial codes (curl) that can be used after running the server to check the functionality of the api calls.
  
  - User:

    * Creation:

    ```
    curl -X POST http://localhost:5000/api/v1/users/ \
      -H "Content-Type: application/json" \
      -d '{
		        "first_name": "John", 
		        "last_name": "Doe", 
            "password" : "pass123",
		        "email": "john.doe@example.com"
		      }'
	  ```

    Expected return
    
    ```
    {
      "id": generated id,
      "message": "User created successfully"
    }
    ```

    * Retrieval:

    For all users

    ```
      curl -X GET http://localhost:5000/api/v1/users/
	  ```
  
    For specific user based on id
	
    Please replace <user_id> with the id generated during user creation.

   	```
      curl -X GET http://localhost:5000/api/v1/users/<user_id>
	  ```

    For login (can be done after user creation)

    ```
      curl -X POST http://localhost:5000/api/v1/auth/login \
        -H "Content-type: application/json" \
        -d '{
            "email": "john.doe@example.com",
            "password": "pass123"
        }'
    ```

    After the login request has been made, user will be returned with an access token which can be used for accessing authenticated endpoints.

    Expected return:
    
	```
    {
      "access_token": "eyJhbGci..."
    }
	```

    * Update:

    Please replace <user_id> with the id generated during user creation.
    
    Please replace access_token with the token received after the authorization.

    ```
      curl -X PUT http://localhost:5000/api/v1/users/<user_id> \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer access_token" \
      -d '{
    	      "first_name": "Sam", 
		        "last_name": "Smith", 
		      }'
	  ```

    Expected return:

    ```
      {
        "success": "User updated"
      }
    ```

    In our clone, a regular user cannot change either email or password. When attempting to do so, the following message is expected.

    ```
          curl -X PUT http://localhost:5000/api/v1/users/<user_id> \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer access_token" \
      -d '{
    	      "first_name": "Sam", 
		        "last_name": "Smith", 
            "email": "sam.smith@example.com
		      }'
    ```

    Expected return

    ```
      {
        "error": "Cannot edit password or email"
      }
    ```

    Only admins are allowed to make these changes. Listed below are the api calls for an admin.

    * Admin login
	```
      curl -X POST http://localhost:5000/api/v1/auth/login \
      -H "Content-type: application/json" \
      -d '{
          "email": "admin@hbnb.io",
          "password": "admin1234"
          }'
	```
  
    Expected return

    ```
    {
      "access_token": "eyJhbGci..."
    }
    ```

    * Admin User Creation

	```
      curl -X POST http://localhost:5000/api/v1/admins/users/ \
      -H "Content-type: application/json" \
      -H "Authorization: Bearer access_token" \
      -d '{
            "first_name": "radnom",
            "last_name": "rando",
            "password": "random",
            "email": "ran@random.com"
          }'
 	```
  
    Expected return
    
    ```
    {
      "id": generated id,
      "message": "User created successfully"
    }
	```
    
    * Admin user update

    Unlike regular user, admins can change both the email and password of a user.

    Please replace <user_id> with the id generated during user creation.
    
    Please replace access_token with the token received after the authorization.

     ```
          curl -X PUT http://localhost:5000/api/v1/admins/users/<user_id> \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer access_token" \
      -d '{
    	        "first_name": "HELLO",
              "last_name": "THERE",
              "password": "OGERS",
              "email": "ARE@LIKEONIONS.com"
		      }'
    ```     
    
    Expected return

    ```
    {
    "message": "User updated successfully"
    }
    ```
