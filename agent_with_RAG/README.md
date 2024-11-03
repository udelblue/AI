#Install
install pip install -r requirements

#Run
streamlit run main.py

---

You will also need to create:

- A search application [here](https://cloud.google.com/generative-ai-app-builder/docs/create-engine-es)
- A data store [here](https://cloud.google.com/generative-ai-app-builder/docs/create-data-store-es)

A suitable dataset to test this template with is the Alphabet Earnings Reports, which you can
find [here](https://abc.xyz/investor/). The data is also available
at `gs://cloud-samples-data/gen-app-builder/search/alphabet-investor-pdfs`.

Set the following environment variables:

* `GOOGLE_CLOUD_PROJECT_ID` - Your Google Cloud project ID.
* `DATA_STORE_ID` - The ID of the data store in Vertex AI Search, which is a 36-character alphanumeric value found on
  the data store details page.
* `MODEL_TYPE` - The model type for Vertex AI Search.