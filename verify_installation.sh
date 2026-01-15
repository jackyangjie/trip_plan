#!/bin/bash

echo "=== 验证前端依赖 ==="
cd frontend
npm install
echo "✓ Frontend dependencies installed"

echo "=== 验证后端依赖 ==="
cd ../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "✓ Backend dependencies installed"

echo "=== 验证Supabase ==="
cd ..
npx supabase start
echo "✓ Supabase started successfully"

echo "=== 验证后端启动 ==="
cd backend
source venv/bin/activate
python -c "import agentscope; print('✓ AgentScope installed')"
python -c "import fastapi; print('✓ FastAPI installed')"
python -c "import supabase; print('✓ Supabase Python client installed')"

echo "=== 所有依赖验证完成 ==="
