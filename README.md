# cloud-web-ai

## Diagram 

![image](https://github.com/CoolmixZero/cloud-web-ai/assets/107999456/f2dd48d7-5052-485e-b2f9-08d70a579660)

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
  - Access the deployed backend URL.
  - Use the provided endpoints for login, registration, image upload, and history retrieval.

2. Inputs:

- User credentials for login and registration.
- Images for upload.
- JWT tokens for authentication.

3. Outputs:

- JWT tokens upon successful authentication.
- Responses confirming actions such as successful login, registration, and image upload.
- Retrieved user history of model responses.

## NN(Roiko)

#### Overview

This web application utilizes a neural network to detect cancerous cells from medical imagery. It's part of a collaborative school project designed to help in the early diagnosis of cancer.

#### Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8 or above
- Pip package manager
- Jupyter Notebook or JupyterLab
- Azure ML SDK (for data handling with Azure)

#### Installation

To install the required Python packages:

```commandline
pip install -r requirements.txt
```

### Dataset and Initial Processing

#### Dataset Source

Our neural network leverages the CBIS-DDSM (Curated Breast Imaging Subset of DDSM) breast cancer image dataset for training. Available on Kaggle, this dataset provides a diverse collection of mammographic images crucial for our model's accuracy: [CBIS-DDSM Breast Cancer Image Dataset](https://www.kaggle.com/datasets/awsaf49/cbis-ddsm-breast-cancer-image-dataset).

#### Data Acquisition and Preprocessing

The `cnncancer.ipynb` notebook encapsulates the entire data preparation pipeline, beginning with data transfer and culminating in preprocessing:

1. **Transfer Data from Azure**: Utilizing Azure's ML workspace, the following script is executed to retrieve the dataset:

   ```python
   from azureml.core import Workspace, Dataset

   subscription_id = '<your-subscription-id>'
   resource_group = '<your-resource-group>'
   workspace_name = '<your-workspace-name>'

   workspace = Workspace(subscription_id, resource_group, workspace_name)

   dataset = Dataset.get_by_name(workspace, name='data2')
   dataset.download(target_path='.', overwrite=False)
   ```

2. **Unzip the Dataset**: Once downloaded, the dataset is unzipped and prepped for processing:
   ```python
   import zipfile
   local_zip = 'processed_images.zip'
   with zipfile.ZipFile(local_zip, 'r') as zip_ref:
       zip_ref.extractall('')
   ```

#### Image Preprocessing Function

The following function plays a pivotal role in our data preprocessing stage:

```python
import os
import cv2
import numpy as np

def image_processor(image_path, target_size, save_dir, image_name=None):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if image_name is None:
        image_name = os.path.basename(image_path)
    absolute_image_path = os.path.abspath(image_path)
    image = cv2.imread(absolute_image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (target_size[1], target_size[0]))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    l_channel, a_channel, b_channel = cv2.split(image)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l_channel = clahe.apply(l_channel)
    image = cv2.merge((l_channel, a_channel, b_channel))
    image = cv2.cvtColor(image, cv2.COLOR_LAB2RGB)
    image = 255 - image
    image = image.astype(np.float32) / 255.0
    save_path = os.path.join(save_dir, image_name)
    cv2.imwrite(save_path, (image * 255).astype(np.uint8))
    return save_path
```

```python
def process_and_save_images(dataframe, save_dir, target_size):
    processed_image_paths = []
    for index, row in dataframe.iterrows():
        image_path = row['image_file_path']
        image_name = f"processed_{index}.jpg"
        processed_path = image_processor(image_path, target_size[:2], save_dir, image_name)
        processed_image_paths.append(processed_path)
    dataframe['processed_image_path'] = processed_image_paths
```

This functions take an image file path and processes it according to our neural network's requirements.
It handles image resizing, color space conversion, contrast enhancement using CLAHE, and normalization.
Processed images are saved to a specified directory, ready for model ingestion.

#### Running the Initial Cells

Follow the order of execution in the `cnncancer.ipynb` notebook to properly configure the data for model training. Verify Azure login and permission settings before commencing.

### Neural Network Model

#### Architecture

The core of our application is a meticulously structured convolutional neural network (CNN). It's composed of several convolutional layers to extract features, pooling layers to reduce dimensionality, and densely connected layers for classification. Specifics of the architecture—including layer configurations and hyperparameters—are detailed in the notebook.

#### Training and Evaluation

Using the preprocessed CBIS-DDSM dataset, the CNN undergoes training to distinguish between benign and malignant medical images. It's rigorously evaluated to ascertain its accuracy, which reflect the model's diagnostic reliability.

## Front-End (Mark Chernomorchenko)

In his part a nice looking UI was developed using Vue.js 3rd version + Vite as a compiler. The packages which were used are: `tailwind`, `sass`, `pinia`, `primeicons`, `vue-router`, `vue-axios`, `primevue`.

The routes the project contains:

- `/` -> Home page
- `/login` -> Login page
- `/register` -> Register page
- `/profile` -> Profile page

The workflow of using the UI is next:

- A user is not able to upload an image of the scan until they log in or register in the system.
- To do this, user must proceed to `/login` or `/register` route, depends whether the user has an account or not.
- To open one of the routes, user can see two buttons in the header of the application, clicking on one of them will take the user on a certain page with a form.
- After entering data, the validation system checks it and if something is wrong, the system then returns a warning message under an input which the system thinks is wrong.
- If all inputs are correct, user then can click on the `submit` button and wait until the system log them in or create a new account for them.
- Then UI will take the user on the home page, where the user can see upload field as well as submit button.
- As soon as user upload an image, they can immediately see the image which was just uploaded.
- By clicking on the `Submit` button below, user then should receive a result which will say whether the AI see cancer or not on the provided scan.
- The UI background will also follow the answer from AI and color the background red or green.
