import streamlit as st
from google import genai
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
from dotenv import load_dotenv

# Environment Variables Load කිරීම (.env file එක කියවීමට)
load_dotenv()

# Streamlit Page Config Setup
st.set_page_config(
    page_title="A/L Master AI",
    page_icon="🎓",
    layout="wide"
)

# Custom UI Styling (CSS Background, Cards, Typography)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Custom Card Header */
    .main-header {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .main-title {
        color: #38bdf8;
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .sub-credit {
        color: #94a3b8;
        font-size: 16px;
        margin-top: 8px;
    }
    
    .credit-badge {
        color: #38bdf8;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Main Header Display
st.markdown("""
    <div class="main-header">
        <div class="main-title">🎓 A/L Master AI - Science & Maths Smart Solver</div>
        <div class="sub-credit">
            <b>Created by:</b> <span class="credit-badge">[ඔබගේ නම මෙතැනට]</span> &nbsp;|&nbsp; 
            <b>Powered by:</b> <span class="credit-badge">Gemini AI</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# API Key Fetching (.env file එකෙන් හෝ Streamlit Cloud Secrets වලින්)
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

if api_key:
    # Initialize New Google GenAI Client
    client = genai.Client(api_key=api_key)

    # Subject Selection Dropdown
    selected_subject = st.selectbox(
        "🎯 විෂය තෝරන්න (Select Subject):",
        ["Physics (භෞතික විද්‍යාව)", "Chemistry (රසායන විද්‍යාව)", "Combined Mathematics (සංයුක්ත ගණිතය)"]
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Input Method Selection
    input_type = st.radio(
        "📥 ප්‍රශ්නය ඇතුළත් කරන ක්‍රමය තෝරන්න:", 
        ["ලඛිතව (Text Input)", "ඡායාරූපයක් මගින් (Image Input)"],
        horizontal=True
    )
    
    user_prompt = ""
    image_input = None

    # Handling Inputs
    if input_type == "ලඛිතව (Text Input)":
        user_prompt = st.text_area(
            "ප්‍රශ්නය මෙතැන Type කරන්න (English හෝ Sinhala):",
            placeholder="උදාහරණය: m ස්කන්ධයක් සහිත වස්තුවක් v ප්‍රවේගයෙන් ගමන් කරයි..."
        )
    else:
        uploaded_file = st.file_uploader("ප්‍රශ්නයේ ඡායාරූපය Upload කරන්න (JPG/PNG):", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image_input = Image.open(uploaded_file)
            st.image(image_input, caption="Uploaded Problem Image", width=350)
            user_prompt = st.text_input("ප්‍රශ්නයට අමතරව යමක් එකතු කිරීමට ඇත්නම් මෙතැන Type කරන්න (Optional):")

    st.markdown("<br>", unsafe_allow_html=True)

    # Action Button
    if st.button("🚀 ප්‍රශ්නය විසඳන්න (Solve Problem)", use_container_width=True):
        if not user_prompt and not image_input:
            st.warning("⚠️ කරුණාකර ප්‍රශ්නයක් ඇතුළත් කරන්න හෝ ඡායාරූපයක් Upload කරන්න.")
        else:
            with st.spinner(f"🔍 {selected_subject} විෂය නිර්දේශයට අනුව පියවරෙන් පියවර විසඳුම සකස් කරමින් පවතී..."):
                
                # System instructions sent to Gemini AI
                system_instruction = f"""
                You are an expert tutor in the Sri Lankan G.C.E. Advanced Level syllabus specifically for the subject: {selected_subject}.
                Solve the given problem (provided in Sinhala or English text, or as an image containing Sinhala/English text) strictly adhering to the official Sri Lankan A/L curriculum guidelines and standards.
                Provide the entire output in clear, accurate Sinhala (සිංහල).

                Structure the response using these exact markdown headers:

                1. **විසඳුම සහ සුළු කිරීම් (Step-by-Step Solution & Calculation)**:
                   - Show every mathematical and logical step clearly.
                   - Provide reasoning for each formula or step in Sinhala.

                2. **අදාළ සිද්ධාන්ත (Theory & Concepts)**:
                   - Explain the underlying physics principles, chemical concepts/mechanisms, or mathematical theorems used in this problem.

                3. **ප්‍රස්ථාර සහ රූප සටහන් விස්තරය (Diagram / Graph Description)**:
                   - Describe clearly how to construct the relevant diagram, force diagram, circuit, molecular layout, or coordinate graph for this problem.

                4. **Visual Concept & Animation Guide**:
                   - Provide a detailed explanation of how a video animation or visual model would represent this physical/chemical/mathematical scenario step-by-step.

                5. **වැඩිදුර අධ්‍යයනයට (References & Resources)**:
                   - Mention exact syllabus units, Resource Book sections, or search terms to study this topic further.
                """

                # Assemble contents payload
                contents = [system_instruction]
                if user_prompt:
                    contents.append(user_prompt)
                if image_input:
                    contents.append(image_input)

                try:
                    # Generate response from Gemini API
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=contents
                    )

                    st.markdown("---")
                    st.markdown("### 📝 විසඳුම (Solution)")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"දෝෂයක් සිදු විය: {str(e)}")

            # Visualisation Graph Section
            st.markdown("---")
            st.write("### 📊 Sample Visualisation Graph")
            fig, ax = plt.subplots(figsize=(8, 4))
            x = np.linspace(-10, 10, 400)
            y = x**2
            ax.plot(x, y, color='#38bdf8', linewidth=2)
            ax.set_title("Function Graph Preview", color='white')
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.set_facecolor('#0f172a')
            fig.patch.set_facecolor('#0f172a')
            ax.tick_params(colors='white')
            st.pyplot(fig)

else:
    st.error("🔑 API Key එක හමු නොවීය! `.env` file එකෙහි `GEMINI_API_KEY` ඇතුළත් කර ඇත්දැයි බලන්න.")

# Footer Section
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 14px;">
        A/L Master AI • <b>Created by [JANIDU KAVEESHA]</b> • Powered by <b>Gemini AI</b>
    </div>
""", unsafe_allow_html=True)