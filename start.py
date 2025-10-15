#!/usr/bin/env python3
"""
智能启动脚本
根据配置自动启动所有必需的服务，并自动初始化数据
"""

import os
import sys
import subprocess
import time
import asyncio
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.app.core.smart_env_loader import load_smart_env


def print_banner():
    """打印启动横幅"""
    print("\n" + "=" * 70)
    print("  AI Context System - 智能启动器")
    print("=" * 70 + "\n")


async def init_database_data():
    """初始化数据库数据（分类等）"""
    try:
        # 添加backend目录到sys.path
        import sys
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        # 先初始化数据库连接
        from app.core import database as db_module
        await db_module.init_db()
        
        # 确保创建数据库表
        from app.models.database import DevType, DocumentType, Base
        from sqlalchemy import select
        import uuid
        
        # 创建所有表
        async with db_module.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # 使用会话工厂创建session
        async with db_module.async_session() as session:
            # 检查是否已有分类数据
            result = await session.execute(select(DevType))
            existing = result.scalars().first()
            
            if existing:
                print("   数据库数据已存在")
                return
            
            print("   初始化分类数据...")
            
            # 业务文档类型
            business_types = [
                ("design_doc", "设计文档", "系统设计、架构设计等文档", "", 1),
                ("requirement_doc", "需求文档", "产品需求、功能需求等文档", "", 2),
                ("technical_doc", "技术文档", "技术方案、技术选型等文档", "", 3),
                ("test_doc", "测试文档", "测试计划、测试用例等文档", "", 4),
                ("user_manual", "用户手册", "用户使用指南、操作手册", "", 5),
            ]
            
            # Demo代码类型
            demo_types = [
                ("api_example", "API示例", "API接口示例代码", "", 1),
                ("package_example", "工具包示例", "工具包、库的示例代码", "", 2),
                ("unittest_example", "单元测试", "单元测试示例代码", "", 3),
                ("full_project", "完整项目示例", "完整的项目示例代码", "", 4),
            ]
            
            # 规范文档类型
            checklist_types = [
                ("dev_standard", "开发规范", "开发流程、编码规范等", "", 1),
                ("code_standard", "代码规范", "代码风格、命名规范等", "", 2),
                ("test_standard", "测试规范", "测试流程、测试标准等", "", 3),
            ]
            
            # 插入数据
            for name, display_name, desc, icon, order in business_types:
                session.add(DevType(
                    id=str(uuid.uuid4()),
                    category=DocumentType.BUSINESS_DOC,
                    name=name,
                    display_name=display_name,
                    description=desc,
                    icon=icon,
                    sort_order=order
                ))
            
            for name, display_name, desc, icon, order in demo_types:
                session.add(DevType(
                    id=str(uuid.uuid4()),
                    category=DocumentType.DEMO_CODE,
                    name=name,
                    display_name=display_name,
                    description=desc,
                    icon=icon,
                    sort_order=order
                ))
            
            for name, display_name, desc, icon, order in checklist_types:
                session.add(DevType(
                    id=str(uuid.uuid4()),
                    category=DocumentType.CHECKLIST,
                    name=name,
                    display_name=display_name,
                    description=desc,
                    icon=icon,
                    sort_order=order
                ))
            
            await session.commit()
            print("   ✓ 分类数据初始化完成")
            
    except Exception as e:
        print(f"   ⚠ 分类数据初始化失败（可以后续手动初始化）: {e}")


def check_dependencies(env_vars):
    """检查并启动必需的依赖服务"""
    environment = env_vars.get('ENVIRONMENT')
    
    print("[检查依赖服务]\n")
    
    dependencies = []
    
    # Neo4j
    if env_vars.get('NEO4J_ENABLED') == 'true':
        dependencies.append({
            'name': 'Neo4j',
            'check': check_neo4j,
            'start': start_neo4j if environment == 'development' else None
        })
    
    # Redis (生产环境或明确启用时)
    if env_vars.get('REDIS_ENABLED') == 'true':
        dependencies.append({
            'name': 'Redis',
            'check': check_redis,
            'start': start_redis if environment == 'development' else None
        })
    
    # ChromaDB
    if env_vars.get('CHROMA_ENABLED') == 'true':
        dependencies.append({
            'name': 'ChromaDB',
            'check': check_chroma,
            'start': start_chroma if environment == 'development' else None
        })
    
    # 检查并启动依赖
    for dep in dependencies:
        print(f"   检查 {dep['name']}...", end=' ')
        
        if dep['check']():
            print("[运行中]")
        elif dep['start']:
            print("[未运行] 尝试启动...")
            if dep['start']():
                print(f"      > {dep['name']} 已启动")
            else:
                print(f"      > {dep['name']} 启动失败，某些功能可能不可用")
        else:
            print("[未运行] 需要手动启动")
    
    print()


def check_neo4j():
    """检查 Neo4j 是否运行"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex(('localhost', 7687))
        s.close()
        return result == 0
    except:
        return False


def start_neo4j():
    """启动 Neo4j（测试环境）"""
    return False


def check_redis():
    """检查 Redis 是否运行"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex(('localhost', 6379))
        s.close()
        return result == 0
    except:
        return False


def start_redis():
    """启动 Redis（测试环境）"""
    return False


def check_chroma():
    """检查 ChromaDB 是否运行"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex(('localhost', 8001))
        s.close()
        return result == 0
    except:
        return False


def start_chroma():
    """启动 ChromaDB（测试环境）"""
    return False


def install_dependencies(env_vars):
    """安装 Python 依赖"""
    network_env = env_vars.get('NETWORK_ENV')
    
    print("[检查 Python 依赖]\n")
    
    # 基础依赖
    requirements_file = project_root / 'backend' / 'requirements.txt'
    
    if requirements_file.exists():
        print(f"   检查基础依赖...")
        # 检查是否需要安装依赖
        try:
            import fastapi
            import uvicorn
            print(f"   > 基础依赖已安装")
        except ImportError:
            print(f"   安装基础依赖...")
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-q', '-r', str(requirements_file)],
                capture_output=True
            )
            if result.returncode == 0:
                print(f"   > 基础依赖已安装")
            else:
                print(f"   > 基础依赖安装失败，请手动安装：pip install -r backend/requirements.txt")
    
    # 外网环境需要本地 Embedding 模型依赖
    if network_env == 'internet':
        print(f"   检查 Embedding 模型依赖...")
        try:
            import sentence_transformers
            print(f"   > Embedding 依赖已安装")
        except ImportError:
            print(f"   > Embedding 依赖未安装（开发模式可选）")
    
    print()


def start_backend(env_vars):
    """启动 Backend 服务"""
    print("[启动 Backend 服务]\n")
    
    backend_dir = project_root / 'backend'
    port = env_vars.get('BACKEND_PORT', '8000')
    
    # 启动 FastAPI
    cmd = [
        sys.executable, '-m', 'uvicorn',
        'app.main:app',
        '--host', '0.0.0.0',
        '--port', port
    ]
    
    # 开发环境启用热重载
    if env_vars.get('RELOAD') == 'true':
        cmd.append('--reload')
    
    print(f"   命令：{' '.join(cmd)}")
    print(f"   访问：http://localhost:{port}")
    print(f"   文档：http://localhost:{port}/docs")
    print()
    
    try:
        subprocess.Popen(cmd, cwd=str(backend_dir))
    except Exception as e:
        print(f"   [错误] 后端启动失败：{e}")



def start_frontend(env_vars):
    """启动 Frontend 服务"""
    print("[启动 Frontend 服务]\n")
    
    frontend_dir = project_root / 'frontend'
    port = env_vars.get('FRONTEND_PORT', '3000')
    
    # 检查前端目录是否存在
    if not frontend_dir.exists():
        print("   [警告] frontend/ 目录不存在，跳过前端启动")
        return
    
    os.chdir(frontend_dir)
    
    # 跨平台 npm 命令
    npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
    
    # 检查 node_modules 是否存在
    if not (frontend_dir / 'node_modules').exists():
        print(f"   检测到首次运行，正在安装前端依赖...")
        install_result = subprocess.run([npm_cmd, 'install'], capture_output=True, text=True)
        if install_result.returncode != 0:
            print(f"   [警告] 前端依赖安装失败：{install_result.stderr}")
            return
    
    cmd = [npm_cmd, 'start']
    
    print(f"   命令：{' '.join(cmd)}")
    print(f"   访问：http://localhost:{port}")
    print()
    
    # 设置环境变量
    env = os.environ.copy()
    env['PORT'] = port
    
    try:
        subprocess.Popen(cmd, env=env, cwd=str(frontend_dir))
    except Exception as e:
        print(f"   [错误] 前端启动失败：{e}")



def start_mcp(env_vars):
    """启动 MCP Server"""
    print("[启动 MCP Server]\n")
    
    mcp_dir = project_root / 'mcp-server'
    port = env_vars.get('MCP_PORT', '3001')
    
    # 检查 MCP 目录是否存在
    if not mcp_dir.exists():
        print("   [警告] mcp-server/ 目录不存在，跳过 MCP 启动")
        return
    
    os.chdir(mcp_dir)
    
    # 跨平台 npm 命令
    npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
    
    # 检查 node_modules 是否存在
    if not (mcp_dir / 'node_modules').exists():
        print(f"   检测到首次运行，正在安装 MCP 依赖...")
        install_result = subprocess.run([npm_cmd, 'install'], capture_output=True, text=True)
        if install_result.returncode != 0:
            print(f"   [警告] MCP 依赖安装失败：{install_result.stderr}")
            return
    
    cmd = [npm_cmd, 'run', 'dev' if env_vars.get('RELOAD') == 'true' else 'start']
    
    print(f"   命令：{' '.join(cmd)}")
    print(f"   访问：http://localhost:{port}")
    print()
    
    try:
        subprocess.Popen(cmd, cwd=str(mcp_dir))
    except Exception as e:
        print(f"   [错误] MCP 启动失败：{e}")



def deploy_k8s(env_vars):
    """使用 K8s 部署（生产环境）"""
    print("[K8s 部署]\n")
    
    k8s_dir = project_root / 'k8s'
    
    if not k8s_dir.exists():
        print("   [错误] 找不到 k8s/ 目录")
        return
    
    # 应用 K8s 配置
    configs = [
        'namespace.yaml',
        'configmap.yaml',
        'secrets.yaml',
        'postgres.yaml',
        'redis.yaml',
        'neo4j.yaml',
        'chroma.yaml',
        'backend.yaml',
        'frontend.yaml',
        'mcp-server.yaml',
        'ingress.yaml'
    ]
    
    for config in configs:
        config_file = k8s_dir / config
        if config_file.exists():
            print(f"   应用配置：{config}")
            subprocess.run(['kubectl', 'apply', '-f', str(config_file)])
    
    print()
    print("   > K8s 部署完成")
    print("   查看状态：kubectl get pods -n ai-context-system")
    print()


def main():
    """主函数"""
    print_banner()
    
    # 加载环境配置
    try:
        env_vars = load_smart_env()
    except Exception as e:
        print(f"[错误] 配置加载失败：{e}")
        sys.exit(1)
    
    environment = env_vars.get('ENVIRONMENT')
    
    # 测试环境：本地启动
    if environment == 'development':
        # 检查依赖服务
        check_dependencies(env_vars)
        
        # 安装 Python 依赖
        install_dependencies(env_vars)
        
        # 初始化数据库数据
        print("[初始化数据库]\n")
        try:
            asyncio.run(init_database_data())
        except Exception as e:
            print(f"   ⚠ 数据库初始化跳过: {e}")
        print()
        
        # 启动服务
        print("[启动服务]\n")
        print("=" * 70)
        print()
        
        start_backend(env_vars)
        time.sleep(2)
        
        start_frontend(env_vars)
        time.sleep(2)
        
        start_mcp(env_vars)
        
        print()
        print("=" * 70)
        print("  所有服务已启动")
        print("=" * 70)
        print()
        print("  访问地址：")
        print(f"     Frontend: http://localhost:{env_vars.get('FRONTEND_PORT')}")
        print(f"     Backend:  http://localhost:{env_vars.get('BACKEND_PORT')}")
        print(f"     MCP:      http://localhost:{env_vars.get('MCP_PORT')}")
        print(f"     API 文档: http://localhost:{env_vars.get('BACKEND_PORT')}/docs")
        print()
        print("  按 Ctrl+C 停止所有服务")
        print()
        
        # 保持运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n  正在停止服务...")
            print()
    
    # 生产环境：K8s 部署
    elif environment == 'production':
        deploy_k8s(env_vars)
    
    else:
        print(f"[错误] 未知的环境：{environment}")
        sys.exit(1)


if __name__ == '__main__':
    main()
