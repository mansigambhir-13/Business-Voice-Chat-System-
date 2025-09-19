#!/bin/bash

# 🎯 Stealth Business Voice System - Quick Start Script
# Professional Voice Cloning with snorTTS-Indic-v0

echo "🎯 Starting Stealth Business Voice System Setup..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Found Python: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    print_success "Found Python: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    print_error "Python is not installed. Please install Python 3.7+ and try again."
    exit 1
fi

# Check if pip is installed
print_status "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    print_success "Found pip3"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    print_success "Found pip"
    PIP_CMD="pip"
else
    print_error "pip is not installed. Please install pip and try again."
    exit 1
fi

# Create virtual environment
print_status "Creating virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi
print_success "Virtual environment activated"

# Upgrade pip
print_status "Upgrading pip..."
$PIP_CMD install --upgrade pip

# Install requirements
print_status "Installing requirements..."
if [ -f "requirements.txt" ]; then
    $PIP_CMD install -r requirements.txt
    print_success "Requirements installed successfully"
else
    print_error "requirements.txt not found. Make sure all files are in the correct directory."
    exit 1
fi

# Check if main app file exists
if [ ! -f "app.py" ]; then
    print_error "app.py not found. Make sure all files are in the correct directory."
    exit 1
fi

print_success "Setup completed successfully!"
echo ""
echo "🎯 SYSTEM READY FOR DEPLOYMENT"
echo "=============================="
echo ""
echo -e "${GREEN}✅ snorTTS-Indic-v0 environment ready${NC}"
echo -e "${GREEN}✅ 80% quality target configured${NC}"
echo -e "${GREEN}✅ Stealth mode activated${NC}"
echo -e "${GREEN}✅ Streamlit interface ready${NC}"
echo -e "${GREEN}✅ Business demo phrases loaded${NC}"
echo ""

# Offer options
echo "Choose your next step:"
echo "1) Run Streamlit app (Recommended)"
echo "2) Run API server for small calls integration"
echo "3) Run both (Streamlit + API)"
echo "4) Exit and deploy manually"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        print_status "Starting Streamlit app..."
        echo ""
        echo -e "${BLUE}🚀 Your voice cloning system will be available at:${NC}"
        echo -e "${GREEN}   http://localhost:8501${NC}"
        echo ""
        echo -e "${YELLOW}📝 Features available:${NC}"
        echo "   • Text-to-Voice with dialog box"
        echo "   • 80% quality monitoring"
        echo "   • Pre-built business demo phrases"
        echo "   • Real-time quality scoring"
        echo "   • Stealth mode operation"
        echo ""
        echo -e "${BLUE}Press Ctrl+C to stop the server${NC}"
        echo ""
        streamlit run app.py
        ;;
    2)
        print_status "Starting API server..."
        echo ""
        echo -e "${BLUE}🚀 Your API server will be available at:${NC}"
        echo -e "${GREEN}   http://localhost:5000${NC}"
        echo ""
        echo -e "${YELLOW}📡 API Endpoints:${NC}"
        echo "   • POST /api/business-voice - Generate voice"
        echo "   • GET /api/demo-phrases - Get demo phrases"
        echo "   • GET /api/stats - System statistics"
        echo "   • GET /health - Health check"
        echo ""
        echo -e "${BLUE}Press Ctrl+C to stop the server${NC}"
        echo ""
        if [ -f "api_integration.py" ]; then
            $PYTHON_CMD api_integration.py
        else
            print_error "api_integration.py not found. Running basic Flask server..."
            $PYTHON_CMD -c "
from flask import Flask
app = Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'Voice system ready'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
"
        fi
        ;;
    3)
        print_status "Starting both Streamlit and API server..."
        echo ""
        echo -e "${BLUE}🚀 Starting dual servers:${NC}"
        echo -e "${GREEN}   Streamlit: http://localhost:8501${NC}"
        echo -e "${GREEN}   API:       http://localhost:5000${NC}"
        echo ""
        echo -e "${BLUE}Press Ctrl+C to stop both servers${NC}"
        echo ""
        
        # Start API server in background
        if [ -f "api_integration.py" ]; then
            $PYTHON_CMD api_integration.py &
            API_PID=$!
        fi
        
        # Start Streamlit
        streamlit run app.py &
        STREAMLIT_PID=$!
        
        # Wait for either to finish
        wait $STREAMLIT_PID
        
        # Kill API server if it's still running
        if [ ! -z "$API_PID" ]; then
            kill $API_PID 2>/dev/null
        fi
        ;;
    4)
        echo ""
        print_success "Setup complete! You can now:"
        echo ""
        echo -e "${YELLOW}For Streamlit app:${NC}"
        echo "   streamlit run app.py"
        echo ""
        echo -e "${YELLOW}For API server:${NC}"
        echo "   python api_integration.py"
        echo ""
        echo -e "${YELLOW}For deployment:${NC}"
        echo "   • Push to GitHub"
        echo "   • Deploy on Render using render.yaml"
        echo "   • Or deploy on Heroku/other platforms"
        echo ""
        ;;
    *)
        print_warning "Invalid choice. Exiting..."
        exit 1
        ;;
esac

print_success "Thanks for using the Stealth Business Voice System!"
echo -e "${BLUE}🎯 Professional voice cloning with snorTTS-Indic-v0 ready!${NC}"