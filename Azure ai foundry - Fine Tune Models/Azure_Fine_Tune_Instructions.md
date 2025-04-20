

## Steps to take to fine tune a LLM or service in Azure Foundry 

### Create fine tuning dataset

Choose a dataset to customize your model. Ensure your training data is in a .jsonl file, formatted for chat completions, with 'messages' as the row header. The file must be less than 512 MB in size. At least 10 examples are required.

example of jsonl is located here. https://github.com/openai/openai-cookbook/blob/main/examples/data/toy_chat_fine_tuning.jsonl


### Create a folder and upload to Azure storage

Create a folder and add the jsonl to the folder. Alter the name of the training data to add a version number (v1, v2, etc). 
1


### Select Model and go through wizard

Add validataion data is needed. This should also be of jsonl format. 
2-5


### Model Training

Model training takes time so be patient. 
6

