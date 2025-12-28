#!/usr/bin/env python
"""
AI Interview Assistant v2.0 - System Verification Script
Verifies all components are configured correctly
"""

import os
import sys
import subprocess
from pathlib import Path

def print_status(status, message):
    """Print colored status message"""
    if status == "✓":
        print(f"  ✓ {message}")
    elif status == "✗":
        print(f"  ✗ {message}")
    elif status == "⚠":
        print(f"  ⚠ {message}")
    else:
        print(f"  ℹ {message}")

def check_python():
    """Check Python installation"""
    print("\n📦 Python Environment:")
    try:
        version = subprocess.check_output([sys.executable, '--version']).decode().strip()
        print_status("✓", f"Python {version}")
        return True
    except:
        print_status("✗", "Python not found")
        return False

def check_gemini():
    """Check Gemini library"""
    print("\n🤖 Gemini AI:")
    try:
        import google.genai
        print_status("✓", "google-genai installed")
        return True
    except ImportError:
        print_status("✗", "google-genai not installed")
        print_status("ℹ", "Run: pip install google-genai")
        return False

def check_dependencies():
    """Check required Python packages"""
    print("\n📚 Dependencies:")
    packages = ['fastapi', 'motor', 'pymongo', 'pydantic', 'dotenv']
    all_ok = True
    
    for package in packages:
        try:
            __import__(package)
            print_status("✓", f"{package} installed")
        except ImportError:
            print_status("✗", f"{package} not installed")
            all_ok = False
    
    return all_ok

def check_env_files():
    """Check environment configuration files"""
    print("\n🔑 Environment Files:")
    
    # Check backend .env
    backend_env = Path("backend/.env")
    if backend_env.exists():
        with open(backend_env) as f:
            content = f.read()
            if "GEMINI_API_KEY" in content:
                print_status("✓", "backend/.env configured with Gemini API key")
            else:
                print_status("✗", "backend/.env missing GEMINI_API_KEY")
    else:
        print_status("✗", "backend/.env not found")
    
    # Check frontend .env.local
    frontend_env = Path(".env.local")
    if frontend_env.exists():
        print_status("✓", ".env.local exists")
    else:
        print_status("⚠", ".env.local not found (using defaults)")

def check_backend_files():
    """Check backend files"""
    print("\n🔧 Backend Files:")
    
    files = [
        ("backend/main_v2.py", "v2.0 with Gemini AI"),
        ("backend/main.py", "v1.0 fallback"),
        ("backend/requirements.txt", "Dependencies"),
    ]
    
    for file_path, description in files:
        if Path(file_path).exists():
            print_status("✓", f"{file_path} ({description})")
        else:
            print_status("✗", f"{file_path} missing")

def check_frontend_files():
    """Check frontend files"""
    print("\n⚛️  Frontend Files:")
    
    files = [
        ("app/interview/page.tsx", "Interview page"),
        ("app/results/page.tsx", "Results page"),
        ("lib/api.ts", "API client"),
    ]
    
    for file_path, description in files:
        if Path(file_path).exists():
            print_status("✓", f"{file_path} ({description})")
        else:
            print_status("✗", f"{file_path} missing")

def check_mongodb():
    """Check MongoDB connection"""
    print("\n🗄️  MongoDB:")
    try:
        result = subprocess.run(
            ["mongosh", "--eval", "db.adminCommand('ping')"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print_status("✓", "MongoDB is running (localhost:27017)")
            return True
        else:
            print_status("✗", "MongoDB is not running")
            print_status("ℹ", "Start MongoDB before running the application")
            return False
    except FileNotFoundError:
        print_status("⚠", "mongosh not found in PATH")
        print_status("ℹ", "Install MongoDB or add it to PATH")
        return False
    except subprocess.TimeoutExpired:
        print_status("✗", "MongoDB connection timeout")
        return False
    except Exception as e:
        print_status("✗", f"MongoDB check failed: {str(e)}")
        return False

def check_ports():
    """Check if required ports are available"""
    print("\n🔌 Ports:")
    import socket
    
    ports = {
        8000: "Backend API",
        3000: "Frontend",
        27017: "MongoDB",
    }
    
    for port, service in ports.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('localhost', port))
                if result == 0:
                    print_status("⚠", f"Port {port} in use ({service})")
                else:
                    print_status("✓", f"Port {port} available ({service})")
        except:
            print_status("✓", f"Port {port} available ({service})")

def check_documentation():
    """Check documentation files"""
    print("\n📚 Documentation:")
    
    docs = [
        "START_HERE_AI_v2.md",
        "QUICKSTART_AI_v2.md",
        "IMPLEMENTATION_COMPLETE.md",
        "COMMANDS.md",
    ]
    
    for doc in docs:
        if Path(doc).exists():
            print_status("✓", doc)
        else:
            print_status("✗", doc)

def print_summary():
    """Print summary and next steps"""
    print("\n" + "="*60)
    print("✨ AI Interview Assistant v2.0 - Verification Summary")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Ensure MongoDB is running: mongosh")
    print("2. Start Backend: cd backend && uvicorn main_v2:app --reload")
    print("3. Start Frontend: pnpm dev")
    print("4. Visit: http://localhost:3000")
    print("\n📖 Read: START_HERE_AI_v2.md for complete setup guide")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("\n🚀 AI Interview Assistant v2.0 - System Check\n")
    
    # Run all checks
    check_python()
    check_gemini()
    check_dependencies()
    check_env_files()
    check_backend_files()
    check_frontend_files()
    check_mongodb()
    check_ports()
    check_documentation()
    
    # Print summary
    print_summary()
    
    print("✅ Verification complete!")
    print("\nFor issues, check COMMANDS.md or START_HERE_AI_v2.md")
