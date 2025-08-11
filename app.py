import streamlit as st
import base64
import os
from groq import Groq
from PIL import Image
import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
@st.cache_resource
def get_groq_client():
    """Initialize and return Groq client"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Please set your GROQ_API_KEY in the .env file")
        return None
    return Groq(api_key=api_key)

# UN SDGs list
UN_SDGS = {
    "No Poverty": "End poverty in all its forms everywhere",
    "Zero Hunger": "End hunger, achieve food security and improved nutrition",
    "Good Health and Well-being": "Ensure healthy lives and promote well-being for all",
    "Quality Education": "Ensure inclusive and equitable quality education",
    "Gender Equality": "Achieve gender equality and empower all women and girls",
    "Clean Water and Sanitation": "Ensure availability and sustainable management of water",
    "Affordable and Clean Energy": "Ensure access to affordable, reliable, sustainable energy",
    "Decent Work and Economic Growth": "Promote sustained, inclusive economic growth",
    "Industry, Innovation and Infrastructure": "Build resilient infrastructure, promote innovation",
    "Reduced Inequalities": "Reduce inequality within and among countries",
    "Sustainable Cities and Communities": "Make cities and human settlements inclusive and sustainable",
    "Responsible Consumption and Production": "Ensure sustainable consumption and production patterns",
    "Climate Action": "Take urgent action to combat climate change",
    "Life Below Water": "Conserve and sustainably use the oceans, seas and marine resources",
    "Life on Land": "Protect, restore and promote sustainable use of terrestrial ecosystems",
    "Peace, Justice and Strong Institutions": "Promote peaceful and inclusive societies for sustainable development",
    "Partnerships for the Goals": "Strengthen the means of implementation and revitalize partnerships"
}

def generate_text_content(client, sdg_theme, user_prompt, content_type):
    """Generate text content using Groq LLaMA model"""
    try:
        # Create system prompt based on content type
        if content_type == "Poem":
            system_prompt = f"You are a creative poet writing about UN Sustainable Development Goals. Create an inspiring poem about {sdg_theme} based on the user's request."
        elif content_type == "Motivational Quote":
            system_prompt = f"You are a motivational speaker focused on UN Sustainable Development Goals. Create an inspiring quote about {sdg_theme} based on the user's request."
        else:  # Awareness Message
            system_prompt = f"You are an awareness campaign writer for UN Sustainable Development Goals. Create an impactful awareness message about {sdg_theme} based on the user's request."
        
        # Combine SDG context with user prompt
        full_prompt = f"SDG Theme: {sdg_theme}\nUser Request: {user_prompt}\n\nPlease create a {content_type.lower()} that addresses this request while staying true to the SDG theme."
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            model="llama-3.1-8b-instant",
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating content: {str(e)}"

def encode_image_to_base64(image):
    """Convert PIL image to base64 string"""
    try:
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode()
    except Exception as e:
        st.error(f"Error encoding image: {str(e)}")
        return None

def analyze_image_content(client, image_b64, content_type):
    """Analyze image and generate content using Groq Vision model"""
    try:
        if content_type == "Description":
            system_prompt = "You are an expert in analyzing images related to UN Sustainable Development Goals. Provide a detailed description of what you see in the image and how it relates to the SDGs."
        else:  # Message
            system_prompt = "You are an inspiring content creator focused on UN Sustainable Development Goals. Create an inspiring message based on what you see in this image and how it relates to the SDGs."
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Please analyze this image and provide a {content_type.lower()} related to UN Sustainable Development Goals."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            model="llama-3.2-11b-vision-preview",
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def main():
    # Page configuration
    st.set_page_config(
        page_title="UN SDGs Content Generator",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3em;
        margin-bottom: 0.5em;
    }
    .sub-header {
        text-align: center;
        color: #A23B72;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .sdg-section {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .content-output {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">🌍 UN SDGs Content Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Create inspiring content for Sustainable Development Goals using AI</p>', unsafe_allow_html=True)
    
    # Initialize Groq client
    client = get_groq_client()
    if not client:
        st.stop()
    
    # Sidebar for navigation
    st.sidebar.title("🎯 Choose Your Task")
    task_type = st.sidebar.radio(
        "Select task type:",
        ["📝 Text Prompt-Based Generation", "🖼️ Image Prompt-Based Generation"]
    )
    
    if task_type == "📝 Text Prompt-Based Generation":
        st.markdown('<div class="sdg-section">', unsafe_allow_html=True)
        st.header("📝 Text Prompt-Based Content Generation")
        
        # SDG theme selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_sdg = st.selectbox(
                "🎯 Choose an SDG Theme:",
                list(UN_SDGS.keys()),
                help="Select the Sustainable Development Goal theme for your content"
            )
            
            # Display SDG description
            st.info(f"**{selected_sdg}**: {UN_SDGS[selected_sdg]}")
        
        with col2:
            content_type = st.selectbox(
                "📄 Content Type:",
                ["Poem", "Motivational Quote", "Awareness Message"]
            )
        
        # User prompt input
        user_prompt = st.text_area(
            "✍️ Enter your custom prompt:",
            placeholder=f"Example: Write about how technology can help achieve {selected_sdg}...",
            height=100
        )
        
        # Generate button
        if st.button("🚀 Generate Content", type="primary"):
            if user_prompt.strip():
                with st.spinner(f"Generating your {content_type.lower()}..."):
                    generated_content = generate_text_content(client, selected_sdg, user_prompt, content_type)
                    
                    st.markdown('<div class="content-output">', unsafe_allow_html=True)
                    st.markdown(f"### 🎨 Generated {content_type}")
                    st.markdown(f"**Theme:** {selected_sdg}")
                    st.markdown("---")
                    st.markdown(generated_content)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Please enter a prompt to generate content.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:  # Image Prompt-Based Generation
        st.markdown('<div class="sdg-section">', unsafe_allow_html=True)
        st.header("🖼️ Image Prompt-Based Content Generation")
        
        # Image upload
        uploaded_file = st.file_uploader(
            "📤 Upload an image (poster or infographic) related to an SDG:",
            type=["png", "jpg", "jpeg"],
            help="Upload an image related to UN Sustainable Development Goals"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            col1, col2 = st.columns([1, 1])
            
            with col1:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                # Content type selection for image analysis
                image_content_type = st.selectbox(
                    "📄 Generate:",
                    ["Description", "Inspiring Message"]
                )
            
            with col2:
                # Generate button for image analysis
                if st.button("🔍 Analyze Image", type="primary"):
                    with st.spinner("Analyzing your image..."):
                        # Convert image to base64
                        image_b64 = encode_image_to_base64(image)
                        
                        if image_b64:
                            # Generate content based on image
                            generated_content = analyze_image_content(client, image_b64, image_content_type)
                            
                            st.markdown('<div class="content-output">', unsafe_allow_html=True)
                            st.markdown(f"### 🎨 Generated {image_content_type}")
                            st.markdown("---")
                            st.markdown(generated_content)
                            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🌍 Supporting the United Nations Sustainable Development Goals through AI-powered content creation</p>
        <p>Made with ❤️ using Streamlit and Groq LLaMA models</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
