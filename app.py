import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain_core.runnables import RunnableLambda

# Function to get response from Llama 2 model
def getLLamaresponse(input_text, no_words, blog_style):
    # Load the Llama 2 model
    llm = CTransformers(
        model="../../model/llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        config={'max_new_tokens': 256, 'temperature': 0.01}
    )

    # Create a prompt template
    template = """
    Write a blog for {blog_style} job profile for a topic "{input_text}"
    within {no_words} words.
    """

    prompt = PromptTemplate(
        input_variables=["blog_style", "input_text", "no_words"],
        template=template
    )

    # Format the prompt
    final_prompt = prompt.format(
        blog_style=blog_style,
        input_text=input_text,
        no_words=no_words
    )

    # Wrap LLM in RunnableLambda to use invoke
    runnable_llm = RunnableLambda(lambda x: llm(x))

    # Generate response
    response = runnable_llm.invoke(final_prompt)

    return response


# Streamlit UI
st.set_page_config(
    page_title="Generate Blogs",
    page_icon='🤖',
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.header("Generate Blogs 🤖")

input_text = st.text_input("Enter the Blog Topic")

# Creating two columns for extra inputs
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input("No of Words")

with col2:
    blog_style = st.selectbox(
        "Writing the blog for",
        options=("Researchers", "Data Scientist", "Common People"),
        index=0
    )

submit = st.button("Generate")

# Final response
if submit:
    if not input_text or not no_words:
        st.warning("Please fill in all fields to generate a blog.")
    else:
        response = getLLamaresponse(input_text, no_words, blog_style)
        st.subheader("📝 Generated Blog")
        st.write(response)
