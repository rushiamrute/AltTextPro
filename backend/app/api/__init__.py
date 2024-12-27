CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend-url.vercel.app"],
        "methods": ["GET", "POST", "OPTIONS"]
    }
})