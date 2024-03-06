import streamlit as st
import pandas as pd
import json

from langchain.llms import AzureOpenAI
import os

from langchain.prompts import PromptTemplate

MAX_RETRIES = 3  # Maximum number of retries
RETRY_DELAY = 1  # Delay between retries (in seconds)


def load_llm():
    os.environ["OPENAI_API_TYPE"] = st.secrets["OPENAI_API_TYPE"]
    os.environ["OPENAI_API_BASE"] = st.secrets["OPENAI_API_BASE"]
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["DEPLOYMENT_NAME"] = st.secrets["DEPLOYMENT_NAME"]
    os.environ["OPENAI_API_VERSION"] = st.secrets["OPENAI_API_VERSION"]
    os.environ["MODEL_NAME"] = st.secrets["MODEL_NAME"]
    return AzureOpenAI(temperature=0.9,
                       deployment_name=os.environ["DEPLOYMENT_NAME"],
                       model_name=os.environ["MODEL_NAME"])


# Function to identify PII types
def identify_pii(data_element, llm):
    """
    Identifies the PII type of a given data element using AzureOpenAI.

    Parameters:
    - data_element (str): The data element text to analyze.
    - llm (AzureOpenAI): An instance of AzureOpenAI class for making LLM calls.

    Returns:
    - str: The identified PII type.
    """
    # Define the prompt for identifying PII type
    prompt = f"What type of Personally Identifiable Information (PII) does the following data element represent: '{data_element}'? Possible PIIs are name, email, social security number, address, driver license number."

    try:
        # Make the LLM call
        response = llm(prompt)
        pii_response = response.strip().lower()  # Assuming the response is a simple text

        # Define mappings from LLM response to PII categories
        pii_categories = {
            "name": "Name",
            "email": "Email",
            "social security number": "Social Security Number",
            "address": "Address",
            "driver license number": "Driver License Number"
        }

        # Map the LLM's response to a PII category
        for key, value in pii_categories.items():
            if key in pii_response:
                return value
        return "Other"  # Default case if no PII type is identified
    except Exception as e:
        print(f"An error occurred while identifying PII: {str(e)}")
        return "Error"  # You might want to handle this more gracefully in your application


def main():
    st.title("Data Collection and Processing")
    llm = load_llm()

    collection_points = {}
    collection_point = st.text_input("Define a collection point name:", value="Marketing")

    if collection_point:
        # Initialize purposes and data elements for the collection point if not exist
        collection_points[collection_point] = {}

        # Step 2: Define purposes for the collection point
        purpose = st.text_input(f"Define a purpose for {collection_point}:", value="Sell products")

        if purpose:
            # Step 3: Define data elements for each purpose
            # Replace the single text area with three text input fields for data elements
            data_element_1 = st.text_input(f"Enter PII question that you want in the form:",
                                           key=f"{collection_point}_{purpose}_data_element_1",
                                           value="Where do you live?")
            data_element_2 = st.text_input(f"Enter PII question that you want in the form:",
                                           key=f"{collection_point}_{purpose}_data_element_2",
                                           value="What do you go by?")
            data_element_3 = st.text_input(f"Enter PII question that you want in the form:",
                                           key=f"{collection_point}_{purpose}_data_element_3",
                                           value="What is your email?")

            # Collect data elements into a list only if they are not empty
            data_elements = [de for de in [data_element_1, data_element_2, data_element_3] if de]
            collection_points[collection_point][purpose] = data_elements

            if st.button("Save", key=f"save_{collection_point}_{purpose}"):
                # Map collection points to assets and purposes to processing activities
                assets = []
                for cp, purposes in collection_points.items():
                    asset = {"asset_name": cp, "processing_activities": []}
                    for purpose, data_elements in purposes.items():
                        processing_activity = {"name": purpose, "data_elements": []}
                        for data_element in data_elements:
                            pii_type = identify_pii(data_element.strip(), llm)
                            processing_activity["data_elements"].append(
                                {"question": data_element.strip(), "data element": pii_type})
                        asset["processing_activities"].append(processing_activity)
                    assets.append(asset)

                # Visual representation (simple JSON output for example purposes)
                st.json(assets)


if __name__ == "__main__":
    main()
