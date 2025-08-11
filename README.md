# UN SDGs Content Generator

A Streamlit web application that generates inspiring content for UN Sustainable Development Goals using AI through the Groq API.

## Features

- **Text-based Content Generation**: Create poems, motivational quotes, and awareness messages based on SDG themes
- **Image Analysis**: Upload images related to SDGs and generate descriptions or inspiring messages
- **17 SDG Themes**: Choose from all UN Sustainable Development Goals
- **AI-Powered**: Uses Groq's LLaMA models for text generation and vision analysis

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Get your Groq API key from [https://console.groq.com/keys](https://console.groq.com/keys)

3. Add your API key to the `.env` file:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

### Text-based Generation
1. Select an SDG theme from the dropdown
2. Choose content type (Poem, Motivational Quote, or Awareness Message)
3. Enter your custom prompt
4. Click "Generate Content" to create AI-powered content

### Image-based Generation
1. Upload an image related to SDGs (PNG, JPG, JPEG)
2. Choose to generate either a description or inspiring message
3. Click "Analyze Image" to get AI-generated content based on the image

## UN Sustainable Development Goals

The application covers all 17 UN SDGs:
1. No Poverty
2. Zero Hunger
3. Good Health and Well-being
4. Quality Education
5. Gender Equality
6. Clean Water and Sanitation
7. Affordable and Clean Energy
8. Decent Work and Economic Growth
9. Industry, Innovation and Infrastructure
10. Reduced Inequalities
11. Sustainable Cities and Communities
12. Responsible Consumption and Production
13. Climate Action
14. Life Below Water
15. Life on Land
16. Peace, Justice and Strong Institutions
17. Partnerships for the Goals

## Technologies Used

- **Streamlit**: Web application framework
- **Groq API**: AI language models (LLaMA 3.1 8B and LLaMA 3.2 11B Vision)
- **PIL (Pillow)**: Image processing
- **python-dotenv**: Environment variable management

## Requirements

- Python 3.8+
- Valid Groq API key
- Internet connection for API calls

## License

This project is created for educational purposes to promote awareness about UN Sustainable Development Goals.
