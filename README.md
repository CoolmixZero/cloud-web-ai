# cloud-web-ai

## Backend (Nikita)

#### Verbal Analysis and Task Analysis:

The backend of our application is built using FastAPI, chosen for its rapid performance as a Python API framework, coupled with our team's familiarity and experience with it. The key endpoints implemented include login, registration, image upload, and retrieval of user history for model responses.

I opted for **JWT** tokens to ensure secure connections between the client and server, enhancing data protection and authentication processes. Our choice of AWS DynamoDB as the database solution stems from its exceptional speed and straightforward configuration, complemented by our prior experience with it.

Deployment on AWS Lambda was preferred for its consistent deployment process and ease of use, streamlining our deployment workflow.

#### Justification of Chosen Technologies:

**FastAPI** was selected for its efficient performance as an API framework, offering robust features and easy integration with Python. Its asynchronous capabilities contribute to the responsiveness of our application, meeting the demands of real-time interactions.

**AWS DynamoDB** was chosen for its high scalability, low-latency performance, and seamless integration with other AWS services. Its flexible data model and managed infrastructure alleviate the operational burden, allowing us to focus on application development.

**AWS Lambda** emerged as the preferred deployment option due to its serverless architecture, eliminating the need for server maintenance and scaling concerns. Its pay-as-you-go model aligns with our cost-effective approach, ensuring optimal resource utilization.

#### Simple Diagram of Services and Interconnections:

Backend (FastAPI) --> AWS Lambda --> AWS DynamoDB

#### Documentation on Application Usage:

1. Setup:
- Install necessary dependencies using pip.
- Configure environment variables for AWS credentials and other settings.
- Deploy backend on AWS Lambda.
- Start-up:

Access the deployed backend URL.
Use the provided endpoints for login, registration, image upload, and history retrieval.

2. Inputs:
- User credentials for login and registration.
- Images for upload.
- JWT tokens for authentication.

3. Outputs:
- JWT tokens upon successful authentication.
- Responses confirming actions such as successful login, registration, and image upload.
- Retrieved user history of model responses.
