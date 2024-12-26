from flask import Blueprint, request, jsonify
from app.services.langchain_service import LangChainService
from app.services.openai_service import OpenAIService
from app.services.vision_service import VisionService
from app.services.sentiment_service import SentimentService
from app.core.model_config import ModelType
from app.core.exceptions import VisionError
from werkzeug.utils import secure_filename
import os

import base64
from openai import OpenAI
from app.core.config import Config

bp = Blueprint('api', __name__, url_prefix='/api')

langchain_service = LangChainService()
openai_service = OpenAIService()
vision_service = VisionService(model_type=ModelType.HUGGINGFACE)
sentiment_service = SentimentService()

@bp.route('/test', methods=['GET'])
def test():
   return jsonify({"message": "API is working"})

@bp.route('/generate-context', methods=['POST'])
def generate_context():
   data = request.get_json()
   alt_text = data.get('alt_text')
   
   if not alt_text:
       return jsonify({"error": "Alt text is required"}), 400
       
   context = langchain_service.generate_context(alt_text)
   enhanced_context = openai_service.enhance_context(context)
   
   return jsonify({
       "original_context": context,
       "enhanced_context": enhanced_context
   })

@bp.route('/process-image', methods=['POST'])
def process_image():
    try:
        # Debug logging
        print("Files received:", request.files)
        print("Headers:", request.headers)
        
        if 'image' not in request.files:
            return jsonify({
                "error": "No image file provided",
                "files_received": list(request.files.keys())
            }), 400
            
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if not file or not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        # Read the image file
        image_bytes = file.read()
        
        try:
            # Process the image
            alt_text = vision_service.generate_alt_text(image_bytes)
            context = langchain_service.generate_context(alt_text)
            enhanced_context = openai_service.enhance_context(context)
            sentiment = sentiment_service.analyze_sentiment(enhanced_context)
            
            # Debug log
            print("Sentiment Analysis Result:", sentiment)
            
            # Handle sentiment analysis based on its type
            sentiment_data = {}
            if isinstance(sentiment, dict):
                sentiment_data = {
                    "polarity": float(sentiment.get('polarity', 0)),
                    "subjectivity": float(sentiment.get('subjectivity', 0)),
                    "compound": float(sentiment.get('compound', 0)),
                    "sentiment": sentiment.get('sentiment', 'neutral')
                }
            elif isinstance(sentiment, str):
                # Parse the string if it's JSON-like, or use it as emotional elements
                try:
                    import json
                    sentiment_data = json.loads(sentiment)
                except:
                    sentiment_data = {
                        "emotional_elements": sentiment.strip('[]').replace('"', '').split(', '),
                        "sentiment": "mixed"
                    }
            
            response_data = {
                "alt_text": alt_text,
                "original_context": context,
                "enhanced_context": enhanced_context,
                "sentiment_analysis": sentiment_data
            }
            
            return jsonify(response_data)
        except VisionError as e:
            print(f"Vision Error: {str(e)}")
            return jsonify({"error": str(e)}), 422
        
    except Exception as e:
        print("Error processing image:", str(e))  # Debug logging
        return jsonify({"error": str(e)}), 500

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/config/model', methods=['POST'])
def configure_model():
    data = request.get_json()
    model_type = data.get('model_type')
    
    try:
        vision_service.switch_model(model_type)
        return jsonify({
            "message": f"Successfully switched to model: {model_type}",
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 400

@bp.route('/test-openai', methods=['GET'])
def test_openai():
    try:
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        models = client.models.list()
        return jsonify({
            "status": "success",
            "message": "OpenAI connection successful",
            "available_models": [model.id for model in models]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@bp.route('/test-gemini', methods=['GET'])
def test_gemini():
    try:
        import google.generativeai as genai
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Test connection")
        return jsonify({
            "status": "success",
            "message": "Gemini connection successful",
            "response": response.text
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@bp.route('/test-huggingface', methods=['GET'])
def test_huggingface():
    try:
        import requests
        response = requests.get(
            "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large",
            headers={"Authorization": f"Bearer {Config.HUGGINGFACE_API_KEY}"}
        )
        return jsonify({
            "status": "success",
            "message": "Hugging Face connection successful",
            "model_info": response.json()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@bp.route('/test-huggingface-token', methods=['GET'])
def test_huggingface_token():
    try:
        model = HuggingFaceVisionModel()
        if model.test_connection():
            return jsonify({
                "status": "success",
                "message": "Hugging Face token is valid"
            })
        return jsonify({
            "status": "error",
            "message": "Failed to validate Hugging Face token"
        }), 401
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500