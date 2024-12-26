# AltContextPro

An AI-powered image analysis tool that generates detailed alt text, contextual information, and sentiment analysis for images using multiple AI models.

## Features

- 🖼️ Image Upload & Processing with drag-and-drop support
- 🤖 AI-Powered Alt Text Generation
- 📝 Enhanced Context Generation
- 🎭 Sentiment Analysis with emotional elements
- 🔄 Multiple AI Model Support (OpenAI, Gemini, Hugging Face)
- 🎨 Modern, Responsive UI with styled-components

## Project Structure
.
├── backend/
│ ├── app/
│ │ ├── api/
│ │ │ ├── routes.py # API endpoints
│ │ ├── services/
│ │ │ ├── vision_service.py
│ │ │ └── sentiment_service.py
│ ├── .env # Backend environment variables
│ └── run.py # Backend entry point
│
└── frontend/
├── src/
│ ├── components/
│ │ ├── UploadForm.js # Image upload component
│ │ └── Spinner.js # Loading spinner
│ ├── pages/
│ │ ├── document.js # Next.js custom document
│ │ ├── index.js # Home page
│ │ └── upload.js # Upload page
│ └── utils/
│ └── api.js # API utilities
└── .env.local # Frontend environment variables


## Environment Setup

### Backend Environment (.env)

env
OpenAI API Key (optional)
OPENAI_API_KEY=sk-your-openai-key
Google Gemini API Key (optional)
GEMINI_API_KEY=your-gemini-key
Hugging Face API Key (required)
Get from: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=hf_your_huggingface_key
FLASK_ENV=development
DEBUG=True


### Frontend Environment (.env.local)
env
NEXT_PUBLIC_API_URL=http://localhost:8000

## Quick Start

### Backend Setup
bash
Navigate to backend
cd backend
Create virtual environment and install dependencies
pipenv install
pipenv shell
Start server
python run.py


### Frontend Setup
bash
Navigate to frontend
cd frontend
Install dependencies
yarn install
or
npm install
Start development server
yarn dev
or
npm run dev

## API Endpoints

### Image Processing
- `POST /api/process-image`
  - Accepts multipart form data with image file
  - Returns alt text, context, and sentiment analysis

### Model Configuration
- `POST /api/config/model`
  - Switch between AI models (OpenAI, Gemini, Hugging Face)

### Test Endpoints
- `GET /api/test-huggingface` - Test Hugging Face connection
- `GET /api/test-openai` - Test OpenAI connection
- `GET /api/test-gemini` - Test Gemini connection

## Getting API Keys

### Required
1. **Hugging Face API Key**
   - Visit https://huggingface.co/settings/tokens
   - Create new token with 'read' access
   - Add to `backend/.env` as `HUGGINGFACE_API_KEY`

### Optional
1. **OpenAI API Key**
   - Visit https://platform.openai.com/api-keys
   - Add to `backend/.env` as `OPENAI_API_KEY`

2. **Google Gemini API Key**
   - Visit https://makersuite.google.com/app/apikey
   - Add to `backend/.env` as `GEMINI_API_KEY`

## Development

### Tech Stack
- Frontend: Next.js, styled-components, TypeScript
- Backend: Flask, Prisma, Python
- AI Services: OpenAI, Google Gemini, Hugging Face

### Running Tests
bash
Frontend
cd frontend
yarn test
Backend
cd backend
python -m pytest


### Code Style
- Frontend: Airbnb JavaScript Style Guide
- Backend: PEP 8
- Enforced using ESLint and Prettier

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License

## Troubleshooting

1. **API Key Issues**
   - Verify keys are correctly set in `.env`
   - Check API access permissions
   - Ensure no whitespace in key values

2. **Image Upload Issues**
   - Check file size (max 10MB)
   - Verify supported formats (JPG, PNG, GIF)
   - Check browser console for errors

3. **Backend Connection**
   - Verify backend is running on port 8000
   - Check CORS settings if needed
   - Ensure `.env` files are properly loaded
