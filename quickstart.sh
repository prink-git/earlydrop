#!/bin/bash

# EarlyDrop Quick Start Script
# This script helps you set up and run the EarlyDrop platform

COLOR_BLUE='\033[0;34m'
COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${COLOR_BLUE}========================================${NC}"
echo -e "${COLOR_BLUE}Welcome to EarlyDrop Quick Start!${NC}"
echo -e "${COLOR_BLUE}========================================${NC}\n"

# Check if .env files exist
echo -e "${COLOR_YELLOW}Checking configuration files...${NC}"

if [ ! -f "backend/.env" ]; then
    echo -e "${COLOR_RED}✗ backend/.env not found${NC}"
    echo "  Copy backend/.env.example to backend/.env and fill in your Supabase credentials"
    exit 1
else
    echo -e "${COLOR_GREEN}✓ backend/.env found${NC}"
fi

if [ ! -f "frontend/.env.local" ]; then
    echo -e "${COLOR_YELLOW}⚠ frontend/.env.local not found${NC}"
    echo "  Creating frontend/.env.local with default values..."
    cp frontend/.env.example frontend/.env.local
    echo -e "${COLOR_GREEN}✓ frontend/.env.local created${NC}"
else
    echo -e "${COLOR_GREEN}✓ frontend/.env.local found${NC}"
fi

echo -e "\n${COLOR_YELLOW}Setup Options:${NC}"
echo "1. Install dependencies (recommended for first run)"
echo "2. Start backend only"
echo "3. Start frontend only"
echo "4. Start both (requires two terminal windows)"
echo "5. Run integration tests"
echo ""
read -p "Select an option (1-5): " choice

case $choice in
    1)
        echo -e "\n${COLOR_BLUE}Installing backend dependencies...${NC}"
        cd backend
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        pip install -r requirements.txt
        cd ..
        
        echo -e "\n${COLOR_BLUE}Installing frontend dependencies...${NC}"
        cd frontend
        npm install
        cd ..
        
        echo -e "\n${COLOR_GREEN}✓ Dependencies installed successfully!${NC}"
        ;;
    
    2)
        echo -e "\n${COLOR_BLUE}Starting backend...${NC}"
        cd backend
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        uvicorn main:app --reload
        ;;
    
    3)
        echo -e "\n${COLOR_BLUE}Starting frontend...${NC}"
        cd frontend
        npm run dev
        ;;
    
    4)
        echo -e "\n${COLOR_BLUE}To run both services, use two terminal windows:${NC}"
        echo ""
        echo -e "${COLOR_YELLOW}Terminal 1 (Backend):${NC}"
        echo "  cd backend"
        echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
        echo "  uvicorn main:app --reload"
        echo ""
        echo -e "${COLOR_YELLOW}Terminal 2 (Frontend):${NC}"
        echo "  cd frontend"
        echo "  npm run dev"
        echo ""
        echo "Backend: http://127.0.0.1:8000"
        echo "Frontend: http://localhost:3000"
        ;;
    
    5)
        echo -e "\n${COLOR_BLUE}Running integration tests...${NC}"
        echo -e "${COLOR_YELLOW}Make sure the backend is running first!${NC}"
        echo ""
        cd backend
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        python integration_test.py
        ;;
    
    *)
        echo -e "${COLOR_RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${COLOR_GREEN}Done!${NC}"
