import random

import streamlit as st
import os
from graphviz import Digraph

from comments import Comments


def set_env():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    os.environ["SQL_SERVER"] = st.secrets["SQL_SERVER"]
    os.environ["SQL_DATABASE"] = st.secrets["SQL_DATABASE"]
    os.environ["SQL_USERNAME"] = st.secrets["SQL_USERNAME"]
    os.environ["SQL_PASSWORD"] = st.secrets["SQL_PASSWORD"]
    os.environ["MYSQL_CONNECTION_STRING"] = st.secrets["MYSQL_CONNECTION_STRING"]


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

    # Process models
    process_model_creation()

    # Process vendor engagements
    process_vendor_engagements()

    process_purposes()

    # Process comments
    process_comments()


def process_purposes():
    st.header("Purposes as First Class Citizens")

    # Introduction to Purposes
    introduction_to_purposes = """
        **Introduction to Purposes**

        There are three fundamental questions that a privacy governance platform should be able to answer:

        1. What data do I have? This pertains to privacy. An enterprise typically has data stored across hundreds of systems, used in various ways. For the data governance persona, the initial step is to understand all the data the enterprise possesses.

        2. Why do I have the data? Understanding the purpose is crucial. Enterprises collect data for specific purposes, and these must be identified and documented. This is vital for ensuring that enterprises have the necessary user consents, as they may otherwise unknowingly violate regulatory compliance.

        3. What are my responsibilities with this data? Enterprises must understand their obligations regarding user data, including compliance with regulations such as data masking and deletion based on retention policies.

        The platform provides tools such as multimodal data discovery methods, including assessments, imports, data mapping, and data discovery, to answer the first question, This pertains to privacy, as an enterprise typically has data stored across hundreds of systems, used in various ways. For the data governance persona, the initial step is to understand all the data the enterprise possesses.

        The platform also offers the consent platform to capture consents from users, addressing the second question. However, it falls short in connecting this with the data we discover. This crucial aspect is addressed in the following sections.

        Finally our platform continues to address the third question by providing tools to handle data responsibly. We help enterprises understand their obligations when handling customer data, flag risks, and recommend controls, with GRC playing a significant role.
        """

    # Purpose Management Overview
    purpose_management_overview = """
        **Purpose Management Overview**

        Purpose management is a critical aspect of our privacy tech platform, providing the foundation for linking data to specific use cases or intentions. This functionality enables enterprises to manage and track the reasons for which personal data is processed, ensuring compliance with privacy regulations and enhancing data governance practices.
        """

    # Linking Purposes to Data
    linking_purposes_to_data = """
        **Linking Purposes to Data**

        This functionality allows data stewards to select objects from the catalog and link them to one or more purposes. By linking purposes to data, enterprises can ensure that data processing activities are aligned with the intended use cases and purposes specified in their privacy policies. The process of linking identified data to purposes shows a central list of purposes maintained on the consent platform, ensuring consistency and accuracy.
        """

    # Surfacing Purposes from Central List
    surfacing_purposes = """
        **Surfacing Purposes from Central List**

        Purposes are maintained centrally on the consent platform. When linking identified data to purposes, users can select from a central list of purposes, ensuring consistency and accuracy across the platform.
        """

    # Adding New Purposes
    adding_new_purposes = """
        **Adding New Purposes**

        Enterprises often need to add new purposes dynamically to reflect changes in data processing activities or to comply with new regulatory requirements. This functionality enables users to add new purposes on the fly, ensuring that the platform remains flexible and adaptable to evolving privacy needs. The purpose discovery process automatically updates the central purpose repository, unifying all purposes in the platform.
        """

    # Launching Purpose Discovery Assessments
    launching_purpose_discovery = """
        **Launching Purpose Discovery Assessments**

        Purpose discovery assessments are crucial for capturing purposes from different teams and departments within an organization. This functionality streamlines the process of gathering purpose information, ensuring that all relevant stakeholders are involved in defining and documenting data processing purposes.
        """

    # Updating Asset Discovery Templates
    updating_asset_discovery_templates = """
        **Updating Asset Discovery Templates**

        Asset discovery templates need to be updated to capture purposes associated with data elements. This functionality ensures that purposes are included in the data discovery process, providing visibility into how data is being used and for what purposes.
        """

    # Backpropagating Newly Discovered Purposes to Consent Module
    backpropagating_new_purposes = """
        **Backpropagating Newly Discovered Purposes to Consent Module**

        This functionality enables the persona to create new collection points to gather consents for newly discovered purposes. By backpropagating purposes to the consent module, enterprises can ensure that all data processing activities have appropriate consents in place.
        """

    # Updating Data Map with Purposes
    updating_data_map_with_purposes = """
        **Updating Data Map with Purposes**

        The data map is updated with purposes linked to data elements, along with granular stats on how many users have consented to these purposes and how many haven't. This provides a comprehensive view of data usage and consent status across the organization.
        """

    # Building Tooling to Surface Data Subject Level Consent Data
    building_tooling_to_surface_consent_data = """
        **Building Tooling to Surface Data Subject Level Consent Data**

        Tooling is built to surface data subject level consent data based on identified purposes. This data is then sent back to third party systems or teams to ensure that they are using only data for which they have user consent, thus ensuring compliance with privacy regulations.
        """

    # Displaying the purpose management overview and functionalities
    st.markdown(introduction_to_purposes)
    st.markdown(purpose_management_overview)
    st.markdown(linking_purposes_to_data)
    st.markdown(surfacing_purposes)
    st.markdown(adding_new_purposes)
    st.markdown(launching_purpose_discovery)
    st.markdown(updating_asset_discovery_templates)
    st.markdown(backpropagating_new_purposes)
    st.markdown(updating_data_map_with_purposes)
    st.markdown(building_tooling_to_surface_consent_data)


def process_comments():
    comments = Comments()
    comments.connect()

    st.subheader("Have a suggestion?")
    # Detailed question displayed to the user
    st.markdown("""
        We invite you to examine the data map closely and share any suggestions for enhancements or additional elements ...
    """, unsafe_allow_html=True)

    suggestion_type = st.selectbox("Select a Category:", ["Consent", "Cookies", "Data Discovery", "DSAR", "Other"],
                                   key="suggestion_type")
    user_suggestion = st.text_area("Leave your suggestion here:")

    if st.button("Submit", type="primary") and user_suggestion:
        # Add the new user comment along with its category
        comments.add_user_comment(user_suggestion, suggestion_type)
        st.success("Thank you for your suggestion!")

    # Display all comments for the selected category
    all_suggestions = comments.get_user_comments_by_category(suggestion_type)
    # Display all comments for the selected category
    for suggestion, suggestion_type, created_at in all_suggestions:
        st.markdown(
            f"""
            <div style="margin: 10px 0; padding: 10px; background-color: #f9f9f9; border-left: 5px solid #4CAF50;">
                <p style="margin: 0;"><span style="font-size: small;">Category: {suggestion_type}</span></p>
                <pre style="white-space: pre-wrap; word-wrap: break-word; margin: 0;">{suggestion}</pre>
                <sub>Posted on {created_at}</sub>
            </div>
            """,
            unsafe_allow_html=True
        )

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
            if website_domain not in st.session_state.get("assets", {}):
                # If the website domain doesn't exist, create a new entry
                st.session_state["assets"][website_domain] = []

            # Randomly pick a list of vendors from the given options
            vendors_list = ["Microsoft", "Google", "Meta", "Salesforce"]
            selected_vendors = random.sample(vendors_list, random.randint(1, len(vendors_list)))

            # Ensure "vendors" and "links" session variables are initialized
            if "vendors" not in st.session_state:
                st.session_state["vendors"] = []
            if "links" not in st.session_state:
                st.session_state["links"] = []

            # Add selected vendors to the session and create links
            for vendor in selected_vendors:
                if vendor not in st.session_state["vendors"]:
                    st.session_state["vendors"].append(vendor)
                # Create a link between the asset (website domain) and the vendor
                if (website_domain, vendor) not in st.session_state["links"]:
                    st.session_state["links"].append((website_domain, vendor))

            # Display the vendors found as part of the scanning result
            vendors_found = ", ".join(selected_vendors)
            st.success(f"Cookies scanned and added for {website_domain}. Vendors found: {vendors_found}.")
            visualize_data_map()
        else:
            st.error("Please enter a website domain.")


def process_vendor_engagements():
    st.header("Vendor Engagements")

    # Using the rewritten description for Vendor Engagements
    st.markdown("""
    **Vendor Engagements for Comprehensive Risk Management:**
    Vendor risk management is an essential element of any privacy strategy. The OneTrust platform enhances this by offering capabilities to import vendors and assess their risks. With the growing need for oversight over third, fourth, and fifth-party vendors, managing these complex relationships becomes more challenging. OneTrust simplifies this by allowing these multi-tier vendor engagements to be grouped under a single framework, enabling consistent risk management across all vendor levels.
    """)

    # UI to capture engagement name and select third-party vendors, ensuring no duplicates
    engagement_name = st.text_input("Enter Engagement Name:", key="engagement_name")
    predefined_vendors = ["Microsoft", "Google", "Meta", "Salesforce"]
    session_vendors = st.session_state.get("vendors", [])
    available_vendors = sorted(set(predefined_vendors + session_vendors))

    third_party_vendors = st.multiselect("Select Third-Party Vendors:", available_vendors, key="third_party_vendors")

    if st.button("Create Engagement", type="primary"):
        if engagement_name and third_party_vendors:
            # Represent the engagement as a processing activity
            if "processing_activities" not in st.session_state:
                st.session_state["processing_activities"] = {}
            st.session_state["processing_activities"][engagement_name] = []

            # Link the third-party vendors to the processing activity
            if "links" not in st.session_state:
                st.session_state["links"] = []
            for vendor in third_party_vendors:
                if (engagement_name, vendor) not in st.session_state["links"]:
                    st.session_state["links"].append((engagement_name, vendor))

                if vendor not in st.session_state.get("vendors", []):
                    if "vendors" not in st.session_state:
                        st.session_state["vendors"] = []
                    st.session_state["vendors"].append(vendor)

            visualize_data_map()

            st.success(
                f"Engagement '{engagement_name}' with vendors {', '.join(third_party_vendors)} has been successfully added to the Data Map.")


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

        **Data Elements:** The Consent Integration process acknowledges the dynamic nature of data collection by allowing for the creation and selection of Data Elements. These elements form the substantive content of consent. Upon selection, these Data Elements are now published to Data Mapping, where they are meticulously mapped to the corresponding Collection Point, ensuring a direct relationship between where the data is collected and the data itself.

        This structured approach to Consent Integration enhances the transparency and accountability of data processing activities by explicitly linking Collection Points to Data Elements and Purposes to Processing Activities, ensuring every piece of user data is managed with the utmost respect for user privacy and legal compliance.
    """

    st.markdown(consent_integration_text)

    # UI to get inputs from the user
    collection_point = st.text_input("Enter the collection point for data collection:", key="collection_point")
    purpose = st.text_input("Enter the purpose for data collection:", key="purpose")
    selected_data_elements = st.multiselect("Select data elements:", data_elements_options, key="data_elements")

    if st.button("Integrate Consent", type="primary"):
        if collection_point and purpose and selected_data_elements:
            # Update Processing Activities
            if "processing_activities" not in st.session_state:
                st.session_state["processing_activities"] = {}
            st.session_state["processing_activities"][purpose] = []

            # Update Assets
            if "assets" not in st.session_state:
                st.session_state["assets"] = {}
            st.session_state["assets"][collection_point] = selected_data_elements

            # Update Links
            if "links" not in st.session_state:
                st.session_state["links"] = []
            # Don't duplicate
            if (purpose, collection_point) not in st.session_state.get("links", []):
                st.session_state["links"].append((purpose, collection_point))

            st.success("Consent integration has been successfully processed.")
            visualize_data_map()
        else:
            st.error("Please fill in all fields to integrate consent.")


def process_model_creation():
    st.header("AI Governance")
    st.markdown("""
        **AI Governance:**
        The OneTrust Platform introduces a comprehensive AI Governance solution designed to empower customers in the oversight of their AI initiatives. Central to this governance is the Model object, a construct that encapsulates the essence of an AI model, ensuring transparency and accountability. Through the Model object, users have the capability to define critical attributes such as the model's name, its descriptive overview, and its intended purpose. This facilitates a meticulous recording of the AI model's parameters, including the datasets it relies upon, which may carry inherent biases. By capturing this information, the platform aids in identifying and mitigating potential biases, ensuring AI implementations are both ethical and effective. Each Model object is integrated within the platform's data map where the model object is linked to its purpose, captured as a Processing Activity, providing a clear and structured representation of how AI models interact with and impact data governance landscapes.
    """)

    # Predefined processing activities
    predefined_activities = ["Loan Approval Process", "Account Validation Process", "Credit Check Process"]
    # Adding existing activities from session state if available
    existing_activities = list(st.session_state.get("processing_activities", {}).keys())
    all_activities = predefined_activities + existing_activities
    unique_activities = list(set(all_activities))  # Ensure activities are unique

    model_name = st.text_input("Model Name:", value="Loan Approval", key="model_name")
    model_description = st.text_area("Model Description:", key="model_description")
    model_purpose_options = ["Select a processing activity...", "Add new processing activity"] + unique_activities
    model_purpose = st.selectbox("Model Purpose:", model_purpose_options, key="model_purpose")

    # Handling the case where "Add new processing activity" is selected
    if model_purpose == "Add new processing activity":
        model_purpose = st.text_input("Enter new processing activity name:", key="new_activity_name")

        # Button to create a new processing activity
        if st.button("Create New Processing Activity", key="create_new_pa"):
            # Ensure "processing_activities" is initialized in session state
            if "processing_activities" not in st.session_state:
                st.session_state["processing_activities"] = {}
            # Add the new processing activity
            if model_purpose not in st.session_state["processing_activities"]:
                st.session_state["processing_activities"][model_purpose] = []
            st.success(f"Processing activity '{model_purpose}' has been created successfully.")
    elif model_purpose != "Select a processing activity...":
        if "processing_activities" not in st.session_state:
            st.session_state["processing_activities"] = {}
        # Add the new processing activity
        st.session_state["processing_activities"][model_purpose] = []

    if model_purpose not in ["Select a processing activity...", "Add new processing activity"] and st.button(
            "Create Model", type="primary"):
        if model_name and model_description:
            # Initialize "models" if not already in session state
            if "models" not in st.session_state:
                st.session_state["models"] = {}
            # Add the new model
            st.session_state["models"][model_name] = {"description": model_description, "purpose": model_purpose}

            # Use "links" to record both asset-collection point and model-processing activity relationships
            if "links" not in st.session_state:
                st.session_state["links"] = []
            # Record the model-processing activity link
            if (model_purpose, model_name) not in st.session_state.get("links", []):
                st.session_state["links"].append((model_purpose, model_name))

            st.success(
                f"Model '{model_name}' has been created successfully and linked to the processing activity '{model_purpose}'.")
        else:
            st.error("Please fill in all fields to create a model.")

        visualize_data_map()


def visualize_data_map():
    dot = Digraph(comment='Data Map Visualization', format='svg')  # Use SVG for better text rendering

    # Adjusting the default font size and name for all nodes
    dot.attr('node', fontsize='12', fontname='Helvetica bold')  # Specifying a bold font

    # Node attribute configurations for different categories
    processing_activities_attrs = {'style': 'filled', 'color': '#1BB3F0'}
    assets_attrs = {'style': 'filled', 'color': 'orange'}
    models_attrs = {'style': 'filled', 'color': 'yellow'}
    vendors_attrs = {'style': 'filled', 'color': '#CD9F4A'}
    element_attrs = {'style': 'filled', 'color': '#CCF01B'}

    # Creating the root node
    dot.node('Data Map', '<<b>Data Map</b>>', shape='folder', style='filled', color='lightgrey')

    # Visualize Processing Activities with specific attributes
    for activity, elements in st.session_state.get("processing_activities", {}).items():
        dot.node(activity, f"<<b>{activity}</b>>", **processing_activities_attrs)
        dot.edge('Data Map', activity)
        for element in elements:
            element_node = f'{activity}_{element}'
            dot.node(element_node, f"<<b>{element}</b>>", **element_attrs)
            dot.edge(activity, element_node)

    # Visualize Assets and Data Elements with specific attributes
    for asset, elements in st.session_state.get("assets", {}).items():
        dot.node(asset, f"<<b>{asset}</b>>", **assets_attrs)
        dot.edge('Data Map', asset)
        for element in elements:
            element_node = f'{asset}_{element}'
            dot.node(element_node, f"<<b>{element}</b>>", **element_attrs)
            dot.edge(asset, element_node)

    # If "models" are maintained separately, visualize them
    for model, details in st.session_state.get("models", {}).items():
        dot.node(model, f"<<b>{model}</b>>", **models_attrs)

    # If "vendors" are maintained separately, visualize them
    for vendor in st.session_state.get("vendors", []):
        dot.node(vendor, f"<<b>{vendor}</b>>", **vendors_attrs)

    # Utilize "links" session variable for connecting nodes directly
    for source, target in st.session_state.get("links", []):
        dot.edge(source, target)

    # Define colors for different categories (for legend)
    colors = {
        'Processing Activities': '#1BB3F0',
        'Assets': 'orange',
        'Models': 'yellow',
        'Vendors': '#CD9F4A',
        'Data Elements': '#CCF01B',
    }

    # Constructing the legend HTML with left-aligned text
    legend_html = '''<<table border="0" cellborder="0" cellspacing="2" cellpadding="2" style="margin-left:auto; margin-right:0;">'''
    legend_html += '''<tr><td colspan="2" align="left"><b>Legend</b></td></tr>'''  # Ensure the 'Legend' title aligns left

    for label, color in colors.items():
        legend_html += f'''<tr>
                             <td width="20" height="20" bgcolor="{color}">&nbsp;</td>
                             <td align="left">{label}</td>  # Align text to the left
                           </tr>'''
    legend_html += '</table>>'

    # Add the legend node to the graph with 'plaintext' shape for no surrounding shape
    dot.node('legend', legend_html, shape='plaintext')

    # Display the graph
    st.graphviz_chart(dot.source)


if __name__ == "__main__":
    main()
