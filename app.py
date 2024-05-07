"""
Author : Aman Ulla
Description: This is a Project to Generate Markdown API Documentation for FastAPI OpenAPI specs
"""


import streamlit as st
import jsonref

# Configure the Streamlit page to have a specific title, icon, and layout
st.set_page_config(
    page_title="FastAPI OpenAPI Documentation Generator",
    page_icon="📜",
    layout="wide",
)

def generate_api_docs(openapi_json: str) -> str:
    """
    Generates API documentation from an OpenAPI JSON string.

    Args:
        openapi_json (str): The OpenAPI JSON string.

    Returns:
        str: The generated markdown documentation.
    """
    markdown_content = ""
    openapi_spec = jsonref.loads(openapi_json)
    
    paths = openapi_spec.get('paths', {})
    components = openapi_spec.get('components', {})

    for path, methods in paths.items():
        for method, details in methods.items():
            markdown_content += f"\n### {details.get('summary', '')}\n"
            markdown_content += f"\n{details.get('description', '')}\n"
            markdown_content += "| Method | URL |\n|--------|-----|\n"
            markdown_content += f"| {method.upper()} | {path} |\n"
            markdown_content += "\n#### Parameters\n"
            markdown_content += "| Name | In | Description | Required |\n|------|----|-------------|----------|\n"
            
            for param in details.get('parameters', []):
                description = param['schema'].get('description', '')
                required = "Required" if param.get('required', False) else "Optional"
                markdown_content += f"| {param.get('name')} | {param.get('in')} | {description} | {required} |\n"
            
            if 'requestBody' in details:
                markdown_content += "\n##### Request Body\n"
                request_body = details['requestBody']
                content_type, schema_info = next(iter(request_body.get('content').items()))
                markdown_content += "| Field | Type | Description | Required |\n|-------|------|-------------|----------|\n"
                for prop_name, prop_details in schema_info.get('schema', {}).get('properties', {}).items():
                    required = "Required" if prop_name in schema_info.get('schema', {}).get('required', []) else "Optional"
                    markdown_content += f"| {prop_name} | {prop_details.get('type', 'N/A')} | {prop_details.get('description', '')} | {required} |\n"
            
            responses = details.get('responses', {})
            for status_code, response in responses.items():
                markdown_content += f"\n##### Response ({status_code})\n"
                markdown_content += "| Field | Type | Description |\n|-------|------|-------------|\n"
                for content_type, content_info in response.get('content', {}).items():
                    for prop_name, prop_details in content_info.get('schema', {}).get('properties', {}).items():
                        markdown_content += f"| {prop_name} | {prop_details.get('type', 'N/A')} | {prop_details.get('description', '')} |\n"
            
            markdown_content += '\n---\n'
    return markdown_content

def render_markdown_with_copy_button(markdown_text: str):
    """
    Renders markdown text in Streamlit with a copy button.

    Args:
        markdown_text (str): Markdown text to render.
    """
    st.markdown(markdown_text, unsafe_allow_html=True)

def render_footer():
    """
    Renders a custom footer in Streamlit.
    """
    footer_html = """
    <style>
    a:link, a:visited {
        color: #BFBFBF;
        background-color: transparent;
        text-decoration: none;
    }
    a:hover, a:active {
        color: #0283C3;
        background-color: transparent;
        text-decoration: underline;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #808080;
        text-align: center;
    }
    </style>
    <div class="footer">
        <p>Made with ❤️ by <a href="https://github.com/connectaman" target="_blank">Aman Ulla</a></p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def main():
    """
    Main function to run the Streamlit app.
    """
    st.markdown("<h1 style='text-align: center;'>FastAPI OpenAPI Documentation Generator</h1>", unsafe_allow_html=True)
    openapi_json = st.text_area("Paste the OpenAPI JSON here:", height=300)
    json_file = st.file_uploader("Or upload an OpenAPI JSON file:", type="json")
    
    if st.columns(4)[2].button('Generate Documentation'):
        if json_file is not None:
            openapi_json = json_file.getvalue().decode("utf-8")
        if openapi_json:
            markdown_content = generate_api_docs(openapi_json)
            st.download_button("📥Download", markdown_content, "api_documentation.md", "text/markdown")
            with st.expander("View Documentation"):
                render_markdown_with_copy_button(markdown_content)
        else:
            st.error("Please provide an OpenAPI JSON to generate documentation.")
    
    render_footer()

if __name__ == "__main__":
    main()