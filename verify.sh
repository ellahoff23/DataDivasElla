#!/bin/bash
# Quick verification script for DataDivas Streamlit app setup

echo "🔍 DataDivas Streamlit App Verification"
echo "========================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python --version
echo ""

# Check if requirements.txt exists
echo "✓ Checking requirements.txt..."
if [ -f requirements.txt ]; then
    echo "  ✅ requirements.txt found"
    cat requirements.txt
else
    echo "  ❌ requirements.txt not found"
    exit 1
fi
echo ""

# Check if streamlit_app.py exists
echo "✓ Checking streamlit_app.py..."
if [ -f streamlit_app.py ]; then
    echo "  ✅ streamlit_app.py found"
else
    echo "  ❌ streamlit_app.py not found"
    exit 1
fi
echo ""

# Check datadivas package
echo "✓ Checking datadivas package..."
if [ -f datadivas/__init__.py ]; then
    echo "  ✅ datadivas/__init__.py found"
else
    echo "  ❌ datadivas package not found"
    exit 1
fi
echo ""

# Check assignment.py
echo "✓ Checking datadivas/assignment.py..."
if [ -f datadivas/assignment.py ]; then
    echo "  ✅ datadivas/assignment.py found"
else
    echo "  ❌ datadivas/assignment.py not found"
    exit 1
fi
echo ""

# Suggest next steps
echo "📝 Next Steps:"
echo "1. Install dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "2. Run locally:"
echo "   streamlit run streamlit_app.py"
echo ""
echo "3. Deploy to Streamlit Cloud:"
echo "   - Push to GitHub"
echo "   - Go to https://share.streamlit.io"
echo "   - Select your repository and streamlit_app.py"
echo ""
echo "✅ Setup verification complete!"
