import streamlit as st
import pandas as pd
import json
import os

from langchain.llms import AzureOpenAI

# Initialize session state to maintain state across runs
if 'collection_points' not in st.session_state:
    st.session_state['collection_points'] = {}


# Function to load the Language Learning Model from Azure OpenAI
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


# Function to identify PII types using AzureOpenAI
def identify_pii(data_element, llm):
    """
    Identifies the PII type of a given data element using AzureOpenAI.
    """
    prompt = f"What type of Personally Identifiable Information (PII) does the following data element represent: '{data_element}'? Possible PIIs are name, email, social security number, address, driver license number."
    try:
        response = llm(prompt)
        pii_response = response.strip().lower()

        pii_categories = {
            "name": "Name",
            "email": "Email",
            "social security number": "Social Security Number",
            "address": "Address",
            "driver license number": "Driver License Number"
        }

        for key, value in pii_categories.items():
            if key in pii_response:
                return value
        return "Other"
    except Exception as e:
        print(f"An error occurred while identifying PII: {str(e)}")
        return "Error"


def main():
    st.title("Platform Integration")

    # Introduction about Data Map and its importance
    st.header("Data Map")
    st.write(
        "The Data Map is central to everything that happens in the platform. It involves key abstractions such as Asset, Processing Activity, Legal Entity, and Vendor.")

    # Introduction about the modules in the system
    st.write(
        "The platform comprises several modules handling Consent Management, Cookies Management, Risks Management, "
        "Data Subject Access Requests, and Data Discovery.")
    llm = load_llm()

    # UI for selecting data elements
    data_elements_options = ['Name', 'Phone Number', 'SSN', 'Email', 'Address']

    # Process consent
    process_consent(data_elements_options)

    # DSAR Form
    process_dsar(data_elements_options)

    # Process DD
    process_dd(data_elements_options)


def process_dd(data_elements_optinos):
    # Data Discovery Form
    st.header("Data Discovery")
    st.write(
        "Data Discovery connects to several data sources, extracts, and classifies data within them. Please provide "
        "the data source name and select the PIIs to simulate the scanning and classification process.")

    # Data Discovery - User inputs
    dd_data_source = st.text_input("Enter the data source name:", key="dd_data_source")

    # Data Discovery - PII selection
    dd_selected_pii = st.multiselect("Select the PIIs discovered in the data source:", data_elements_optinos,
                                     key="dd_pii")

    # Button to add Data Discovery information to DM
    if st.button("Add Data Discovery Information"):
        if dd_data_source and dd_selected_pii:
            # Simulate adding Data Discovery as an asset in DM
            assets = st.session_state.get('collection_points', {})
            if dd_data_source not in assets:
                assets[dd_data_source] = {"Data Discovery": dd_selected_pii}

            st.session_state['collection_points'] = assets

            # Display confirmation and simulate saving to DM (here, just displaying JSON as an example)
            st.success(f"Data Discovery information for '{dd_data_source}' has been added successfully.")
            st.json(assets)
        else:
            st.error("Please fill all fields to add Data Discovery information.")


def process_dsar(data_elements_options):
    st.header("Data Subject Access Request (DSAR)")
    st.write("The DSAR allows users to request access to their data. Please provide your information and select the "
             "data elements you wish to access.")

    dsar_selected_pii = st.multiselect(
        "Select the PIIs you want to access:", data_elements_options, key="dsar_pii")
    # Button to create DSAR in DM
    if st.button("Submit DSAR"):
        if dsar_selected_pii:
            # Simulate DSAR creation as a processing activity in DM
            dsar_collection_point = "DSAR Request"
            dsar_purpose = "User Data Access"
            collection_points = st.session_state['collection_points']
            if dsar_collection_point not in collection_points:
                collection_points[dsar_collection_point] = {}
            collection_points[dsar_collection_point][dsar_purpose] = dsar_selected_pii

            st.session_state['collection_points'] = collection_points

            # Display confirmation and simulate saving to DM (here, just displaying JSON as an example)
            st.success("Your DSAR has been created successfully.")
            st.json(collection_points)
        else:
            st.error("Please fill all fields to submit your DSAR.")


def process_consent(data_elements_options):
    st.header("Consent & Preferences Management")
    # UI to get purpose from the user
    purpose = st.text_input("Enter the purpose for data collection:", key="purpose")
    # UI for collection point name input
    collection_point = st.text_input("Enter a collection point name:", key="collection_point")
    selected_data_elements = st.multiselect("Select data elements:", data_elements_options, key="data_elements")
    # Button to create data elements in Data Mapping (DM) and link to processing activity
    if st.button("Create Purposes/Collection Points"):
        if collection_point and purpose and selected_data_elements:
            # Simulate creation in DM and linking with processing activity
            collection_points = st.session_state['collection_points']
            if collection_point not in collection_points:
                collection_points[collection_point] = {}
            collection_points[collection_point][purpose] = selected_data_elements

            st.session_state['collection_points'] = collection_points

            st.success("Your Purposes/Collection points has been created successfully.")

            # Simulate saving to DM (here, just displaying JSON as an example)
            st.json(collection_points)
        else:
            st.error("Please fill all fields.")


if __name__ == "__main__":
    main()
