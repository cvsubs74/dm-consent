import streamlit as st
import os
from graphviz import Digraph
from langchain.llms import AzureOpenAI
from comments import Comments


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


def set_env():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    os.environ["SQL_SERVER"] = st.secrets["SQL_SERVER"]
    os.environ["SQL_DATABASE"] = st.secrets["SQL_DATABASE"]
    os.environ["SQL_USERNAME"] = st.secrets["SQL_USERNAME"]
    os.environ["SQL_PASSWORD"] = st.secrets["SQL_PASSWORD"]
    os.environ["MYSQL_CONNECTION_STRING"] = st.secrets["MYSQL_CONNECTION_STRING"]


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
    st.set_page_config(layout="wide")
    st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-size: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Platform Integration")
    set_env()

    # Introduction about Data Map and its importance
    data_map_intro = """
        **Data Mapping Overview**

        At the core of our platform lies the Data Map, a pivotal component orchestrating the myriad interactions and processes. This framework is built upon fundamental concepts including Assets, Processing Activities, Legal Entities, and Vendors, each serving a distinct role in the comprehensive management and safeguarding of data.
        """

    integration_narrative = """
        **Enhancing Platform Integration through Comprehensive Data Mapping**

        As we strive for a seamless and comprehensive integration across our platform, the integration of key components such as Consent, Cookies, Data Subject Access Requests (DSAR), and Data Discovery with Data Mapping is essential. This strategic alignment is crucial for elevating our platform's functionality, compliance, and user trust.

        **Consent Integration**: Ensures that user preferences are accurately reflected across all data processing activities, enabling more granular control and transparency over personal data usage.

        **Cookies Management**: By integrating Cookies Management with Data Mapping, users are given precise control over their data, enhancing privacy protections in line with their consent preferences.

        **DSAR Fulfillment**: Streamlines the processing of Data Subject Access Requests, ensuring comprehensive, accurate, and timely responses, thereby reinforcing our commitment to user rights and regulatory compliance.

        **Data Discovery**: Plays a critical role in identifying and classifying data across various sources, ensuring that every piece of data is accurately mapped and managed within our platform.

        Achieving a fully integrated Data Mapping system fortifies our compliance posture and enhances user trust, making our platform not just compliant with current regulations but also ready for the future of data privacy.
    """

    st.markdown(data_map_intro + integration_narrative)

    # UI for selecting data elements
    data_elements_options = ['Name', 'Phone Number', 'SSN', 'Email', 'Address']

    if "processing_activities" not in st.session_state:
        st.session_state["processing_activities"] = {}
    if "assets" not in st.session_state:
        st.session_state["assets"] = {}

    # Process consent
    process_consent(data_elements_options)

    # DSAR Form
    process_dsar()

    # Process DD
    process_dd(data_elements_options)

    # Process Cookies
    process_cookies()

    process_comments()


def process_comments():
    # Initialize and connect to the database using the Comments class
    comments = Comments()
    comments.connect()

    st.subheader("Have a suggestion?")
    # Detailed question displayed to the user
    st.markdown("""
        We invite you to examine the data map closely and share any suggestions for enhancements or additional elements that should be included. This may encompass new objects or attributes you believe are crucial. Furthermore, if you have specific ideas on the structuring or representation of data within the Data Map, we'd appreciate your detailed insights. Often, developing a comprehensive abstraction within the Data Map necessitates considering how various data aggregates might be represented as attributes. Should you propose a new integration, kindly outline its specifics along with the potential use cases it aims to support. Remember, a key objective of establishing a centralized data map is to facilitate robust regulatory intelligence.
        """, unsafe_allow_html=True)

    # User selects a category for their comment
    comment_category = st.selectbox(
        "Select a Category:",
        ["Consent", "Cookies", "Data Discovery", "DSAR", "Other"],
        key="comment_category"
    )

    user_comment = st.text_area("Leave your suggestion here:")

    if st.button("Submit", type="primary"):
        if user_comment:  # Make sure the user has entered a comment
            comments.add_user_comment(user_comment,
                                      comment_category)  # Assuming add_user_comment now also accepts category
            st.success("Thank you for your suggestions!")
        else:
            st.error("Please enter a suggestion.")

    # Filter criteria for recent comments
    st.subheader("Suggestions")
    selected_category = st.selectbox(
        "Select a category to filter comments:",
        ["All", "Consent", "Cookies", "Data Discovery", "DSAR", "Other"],
        key="filter_category"
    )
    all_comments = comments.get_user_comments_by_category(selected_category)

    for comment, category, created_at in all_comments:
        st.markdown(
            f"""
            <div style="margin: 10px 0; padding: 10px; border-left: 5px solid #4CAF50; background-color: #f0f0f0;">
                <h4>{category} Comment</h4>
                <p>{comment}</p>
                <sub>Posted on {created_at}</sub>
            </div>
            """, unsafe_allow_html=True)

    comments.close()


def process_cookies():
    st.header("Cookies Data Mapping Integration")
    st.markdown("""
        **Cookies Data Mapping Integration:** This integration enhances user privacy and data governance by mapping cookies to assets within the Data Map. It allows for precise control over cookie data, aligning with user consent and regulatory requirements. By scanning website domains for cookies and categorizing them accurately in the Data Map, we ensure transparency and compliance in how cookie data is handled.
        """)
    website_domain = st.text_input("Enter the website domain to scan for cookies:", key="website_domain")

    if st.button("Scan Cookies", type="primary"):
        if website_domain:
            # Check if the website domain already exists as an asset in Data Mapping
            if website_domain not in st.session_state["assets"]:
                # If the website domain doesn't exist, create a new entry
                st.session_state["assets"][website_domain] = []

            st.success(f"Cookies scanned and added for {website_domain}.")
            visualize_data_map()
        else:
            st.error("Please enter a website domain.")


def process_dd(data_elements_options):
    st.header("Data Discovery Data Mapping Integration")

    data_discovery_integration_narrative = """
        **Optimizing Data Management through Data Discovery Integration**

        Data Discovery serves as the cornerstone of our platform's approach to proactive data management and compliance. By connecting to a multitude of data sources, Data Discovery delves deep into the digital expanse, extracting and classifying the wealth of data contained within. This process is not just about uncovering data; it's about understanding its nature, relevance, and implications for privacy and compliance.

        **Initiating Data Discovery:**

        The journey begins with the identification of data sources. Users are prompted to provide the name of the data source, setting the stage for a comprehensive scanning and classification process. This step is pivotal, as it not only earmarks the source for exploration but also tailors the discovery process to the unique characteristics of each data repository.

        **Scanning and Classification:**

        Following the identification of the data source, the next phase involves the meticulous scanning of the source, with a keen eye on the Personally Identifiable Information (PII) it harbors. Users select the PIIs of interest, guiding the classification engine in its quest to map the data landscape accurately. This simulation of scanning and classification embodies our platform's commitment to precision and thoroughness in data discovery.

        **Integration into Data Mapping:**

        The culmination of Data Discovery is marked by the seamless integration of findings into the Data Map. Each data source, once defined and scanned, is elevated to the status of an Asset within the Data Map. Concurrently, the discovered PIIs are meticulously cataloged as Data Elements under this newly minted Asset. This integration is a testament to our holistic view of data management, where every piece of information is accounted for, its origins traced, and its implications understood.

        **A Unified Approach to Data Governance:**

        By integrating Data Discovery with Data Mapping, we achieve a unified approach to data governance. This strategy not only enhances our ability to manage data with unparalleled precision but also strengthens our compliance posture. Each Asset and its associated Data Elements become integral components of our Data Map, enriching it with insights and intelligence gleaned from the farthest reaches of our digital ecosystem.

        The integration of Data Discovery with Data Mapping is not merely a procedural enhancement; it's a strategic pivot towards more insightful, compliant, and effective data governance. It underscores our commitment to harnessing the full potential of our data assets while safeguarding the privacy and security of the information entrusted to us.
        """

    st.markdown(data_discovery_integration_narrative)

    # Data Discovery - User inputs
    dd_data_source = st.text_input("Enter the data source name:", key="dd_data_source")

    # Data Discovery - PII selection
    dd_selected_pii = st.multiselect("Select the PIIs discovered in the data source:", data_elements_options,
                                     key="dd_pii")

    # Button to add Data Discovery information to DM
    if st.button("Discover", type="primary"):
        if dd_data_source and dd_selected_pii:
            # Ensure "assets" is initialized in session state
            if "assets" not in st.session_state:
                st.session_state["assets"] = {}

            # Check if the data source already exists as an asset in Data Mapping
            if dd_data_source in st.session_state["assets"]:
                # Append new PII types to the existing list, avoiding duplicates
                current_pii_types = st.session_state["assets"][dd_data_source]
                updated_pii_types = list(set(current_pii_types + dd_selected_pii))
                st.session_state["assets"][dd_data_source] = updated_pii_types
            else:
                # If the data source doesn't exist, create a new entry
                st.session_state["assets"][dd_data_source] = dd_selected_pii

            st.success(f"Data Discovery information for '{dd_data_source}' has been added successfully.")
            visualize_data_map()
        else:
            st.error("Please fill all fields to add Data Discovery information.")


def process_dsar():
    st.header("DSAR Data Mapping Integration")
    st.markdown("""
        **Streamlining DSAR Integration into Data Mapping**
        The essence of Data Subject Access Requests (DSAR) transcends the mere act of solicitation for personal data; it marks a critical intersection of user empowerment and systemic transparency. Integrating DSAR with Data Mapping amplifies this synergy, embodying our commitment to operational excellence and regulatory adherence.
        ...
        By navigating this path, we set a new benchmark for data stewardship, one that harmonizes the intricacies of Data Mapping with the fundamental rights of our users. The journey of integrating DSAR with Data Mapping is a vivid reflection of our dedication to privacy, precision, and proactive engagement.
    """)

    # User-defined DSAR Request Type
    dsar_request_type = st.text_input("Enter DSAR Request Type:", key="dsar_request_type")
    data_elements_options = ["Email", "SSN", "Phone Number", "Address"]

    selected_data_elements = st.multiselect("Select Data Elements:", data_elements_options,
                                            key="selected_data_elements")

    if st.button("Submit DSAR", type="primary"):
        if dsar_request_type and selected_data_elements:
            create_processing_activity(dsar_request_type, selected_data_elements)
            visualize_data_map()
        else:
            st.error("Please enter a DSAR request type and select at least one data element.")


def create_processing_activity(dsar_request_type, selected_data_elements):
    if "processing_activities" not in st.session_state:
        st.session_state["processing_activities"] = {}

    # Directly use the DSAR request type as the key for the processing activity
    st.session_state["processing_activities"][dsar_request_type] = selected_data_elements

    st.success(f"DSAR request '{dsar_request_type}' has been created successfully.")


def process_consent(data_elements_options):
    st.header("Consent Data Mapping Integration")
    consent_integration_text = """
        In the realm of data privacy and compliance, the **Consent Integration** process plays a pivotal role, primarily focusing on the seamless interplay between **Purposes**, **Data Elements**, and **Collection Points**. This process is foundational for ensuring that user consents are meticulously captured, managed, and integrated within the Data Mapping infrastructure, thereby adhering to regulatory requirements and safeguarding user privacy.

        **Collection Points:** The avenues through which user consents are obtained—ranging from web forms to mobile applications—are abstracted as Collection Points. These points are not just channels of interaction but are critical in capturing the context of user consents, delineating the specific conditions under which user data may be collected and processed.

        **Purposes:** At the heart of the Consent Integration process lies the Purpose. It serves as a transparent declaration to users, outlining the intent behind data collection. This clarity is crucial for obtaining informed consents, thereby instilling trust and ensuring compliance with data protection regulations. Within the Data Mapping framework, each Purpose is intricately linked to a Processing Activity, endowed with a property known as the Legal Basis. It is this Legal Basis that imbues the Processing Activity with regulatory legitimacy, directly stemming from the user's consent.

        **Data Elements:** The Consent Integration process acknowledges the dynamic nature of data collection by allowing for the creation and selection of Data Elements. Whether originating from user inputs or derived from a predefined set of seeded data elements, these elements form the substantive content of consent. Upon selection, these Data Elements are published to Data Mapping, where they are meticulously mapped to the corresponding Processing Activity. This mapping is not arbitrary but is guided by the Purpose, ensuring that each data element's collection and processing are justified under the umbrella of the given consent.

        This structured approach to Consent Integration not only facilitates the strategic alignment of data collection practices with regulatory mandates but also enhances the transparency and accountability of data processing activities. By explicitly linking Collection Points to Purposes and Data Elements to Processing Activities, the process ensures that every piece of user data is collected, processed, and managed with the utmost respect for user privacy and legal compliance.
        """

    st.markdown(consent_integration_text)

    # UI to get purpose from the user
    collection_point = st.text_input("Enter the collection point for data collection:", key="collection_point")
    purpose = st.text_input("Enter the purpose for data collection:", key="purpose")
    selected_data_elements = st.multiselect("Select data elements:", data_elements_options, key="data_elements")

    # Ensuring the "Processing Activities" key exists in session state for structured storage
    if "processing_activities" not in st.session_state:
        st.session_state["processing_activities"] = {}

    # Button to create data elements in Data Mapping (DM) and link to processing activity
    if st.button("Create Purpose", type="primary"):
        if purpose and selected_data_elements:
            # Check if the purpose already exists
            if purpose in st.session_state["processing_activities"]:
                # Append new data elements to the existing list, avoiding duplicates
                current_elements = st.session_state["processing_activities"][purpose]
                updated_elements = list(set(current_elements + selected_data_elements))
                st.session_state["processing_activities"][purpose] = updated_elements
            else:
                # If the purpose doesn't exist, create a new entry
                st.session_state["processing_activities"][purpose] = selected_data_elements

            # Display the updated "Processing Activities" to the user
            visualize_data_map()
        else:
            st.error("Please specify a purpose and select at least one data element.")


# Inside your main() function, after processing activities and data discovery assets
def visualize_data_map():
    dot = Digraph(comment='Data Map Visualization')

    # Main nodes
    dot.node('A', 'Data Map')
    dot.node('B', 'Processing Activities')
    dot.node('C', 'Assets')

    # Connect main nodes to Data Map
    dot.edge('A', 'B')
    dot.edge('A', 'C')

    # Assuming session_state['processing_activities'] and session_state['assets'] have been populated
    # Iterate over processing activities

    for activity, elements in st.session_state["processing_activities"].items():
        activity_node = f'PA_{activity.replace(" ", "_")}'
        dot.node(activity_node, activity)
        dot.edge('B', activity_node)
        for element in elements:
            element_node = f'{activity_node}_{element.replace(" ", "_")}'
            dot.node(element_node, element)
            dot.edge(activity_node, element_node)

    # Iterate over data discovery assets
    for asset, elements in st.session_state["assets"].items():
        asset_node = f'DD_{asset.replace(" ", "_")}'
        dot.node(asset_node, asset)
        dot.edge('C', asset_node)
        for element in elements:
            element_node = f'{asset_node}_{element.replace(" ", "_")}'
            dot.node(element_node, element)
            dot.edge(asset_node, element_node)

    # Display the graph
    st.graphviz_chart(dot.source)


if __name__ == "__main__":
    main()
