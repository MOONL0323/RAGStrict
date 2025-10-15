# AI Context System

AI驱动的代码和文档智能管理系统，支持多种文件格式解析、语义搜索和知识图谱构建。

## 目录

- [快速开始](#快速开始)
- [功能特性](#功能特性)
- [技术架构](#技术架构)
- [环境要求](#环境要求)
- [项目结构](#项目结构)
- [配置说明](#配置说明)
- [使用指南](#使用指南)
- [API接口文档](#api接口文档)
- [离线部署](#离线部署)
- [开发指南](#开发指南)
- [故障排除](#故障排除)
- [许可证](#许可证)

---

## 快速开始

### 一键启动

```bash
python start.py
```

就这么简单！脚本会自动完成：
- 检查并安装所有依赖
- 初始化数据库和分类数据
- 启动后端、前端和MCP服务

### 访问地址

启动成功后，访问以下地址：

- 前端页面: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs
- MCP服务: http://localhost:3001

---

## 功能特性

### 文档管理
- 支持多种格式：PDF、Word、Markdown、TXT等
- 智能解析和提取文档内容
- 文档分类和标签管理
- 团队和项目维度的文档组织

### 代码解析
- 支持主流编程语言：Python、Go、Java、JavaScript、TypeScript等
- 代码结构分析和提取
- 示例代码管理和检索

### 智能搜索
- 基于向量数据库的语义搜索
- 支持混合搜索（语义+关键词）
- 多维度筛选（团队、项目、分类等）
- 相关性排序和结果高亮

### 知识图谱
- 自动构建实体关系网络
- 可视化知识图谱
- 支持图谱查询和遍历
- 实体关系分析

### MCP集成
- 实现Model Context Protocol协议
- 支持与AI助手（Claude、ChatGPT等）交互
- 智能代码和文档检索
- 上下文感知的信息提供

---

## 技术架构

### 后端技术栈
- FastAPI: 高性能异步Web框架
- SQLAlchemy: ORM框架，支持多种数据库
- PostgreSQL/SQLite: 关系型数据库
- Neo4j: 图数据库（可选，用于知识图谱）
- ChromaDB: 向量数据库（可选，用于语义搜索）
- Redis: 缓存服务（可选，用于性能优化）

### 前端技术栈
- React 18: 现代化UI框架
- TypeScript: 类型安全的JavaScript
- Ant Design: 企业级UI组件库
- D3.js/ECharts: 数据可视化库
- React Router: 前端路由管理

### MCP Server
- TypeScript: MCP协议服务器实现
- Node.js: 运行时环境
- MCP SDK: Model Context Protocol SDK

---

## 环境要求

### 必需环境
- Python: 3.8 或更高版本
- Node.js: 16.0 或更高版本
- npm: 8.0 或更高版本

### 可选服务
- PostgreSQL: 13+ (生产环境推荐)
- Neo4j: 4.4+ (知识图谱功能)
- Redis: 6.0+ (缓存和性能优化)
- ChromaDB: 最新版本 (语义搜索)

### 操作系统
- Windows 10/11
- Linux (Ubuntu 20.04+, CentOS 7+)
- macOS 10.15+

---

## 项目结构

```
ai-context-system/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API路由定义
│   │   │   ├── auth_simple.py      # 认证接口
│   │   │   ├── documents_core.py   # 文档管理
│   │   │   ├── classifications.py  # 分类管理
│   │   │   ├── search.py           # 搜索接口
│   │   │   ├── graph.py            # 知识图谱
│   │   │   ├── entities.py         # 实体提取
│   │   │   ├── stats.py            # 统计信息
│   │   │   └── mcp_core.py         # MCP接口
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模式
│   │   └── services/       # 业务逻辑
│   ├── requirements.txt    # Python依赖
│   └── run_dev.py         # 开发服务器启动
├── frontend/              # 前端应用
│   ├── src/
│   │   ├── components/    # React组件
│   │   ├── routes/        # 页面路由
│   │   ├── services/      # API服务
│   │   ├── hooks/         # 自定义Hooks
│   │   └── interfaces/    # TypeScript接口
│   ├── package.json       # Node.js依赖
│   └── tsconfig.json      # TypeScript配置
├── mcp-server/           # MCP协议服务器
│   ├── src/
│   │   ├── index.ts       # 入口文件
│   │   ├── server.ts      # MCP服务器
│   │   ├── tools/         # MCP工具定义
│   │   └── services/      # 业务服务
│   ├── package.json
│   └── tsconfig.json
├── config/               # 配置文件目录
├── database/             # 数据库脚本
├── scripts/              # 工具脚本
├── tests/                # 测试文件
├── docker-compose.yml    # Docker编排
├── start.py              # 一键启动脚本
└── README.md            # 本文档
```

---

## 配置说明

### 基础配置

编辑项目根目录的 .env 文件：

```bash
# 环境选择：development 或 production
ENVIRONMENT=development

# 网络环境：intranet（内网）或 internet（外网）
NETWORK_ENV=intranet

# 服务端口配置
BACKEND_PORT=8000
FRONTEND_PORT=3000
MCP_PORT=3001

# 数据库配置（开发环境默认使用SQLite）
DATABASE_URL=sqlite:///./app.db
```

### 高级配置

详细配置项请查看 config/ 目录下的环境配置文件：

- config.development.env: 开发环境配置
- config.production.env: 生产环境配置
- config.intranet.env: 内网环境特殊配置
- config.internet.env: 外网环境特殊配置

---

## 使用指南

### 文档上传

1. 访问前端页面 http://localhost:3000
2. 点击"文档管理"菜单
3. 点击"上传文档"按钮
4. 填写文档信息并选择文件
5. 系统自动解析并建立索引

### 语义搜索

1. 在搜索框输入查询内容
2. 选择搜索范围（可选）
3. 查看搜索结果
4. 点击结果查看文档详情

### 知识图谱

1. 访问"知识图谱"页面
2. 查看实体关系网络可视化
3. 搜索特定实体
4. 探索实体间的关系路径

---

## API接口文档

### 基础URL

```
http://localhost:8000/api/v1
```

### 主要接口

#### 认证接口
- POST /auth/login - 用户登录
- POST /auth/register - 用户注册
- GET /auth/me - 获取当前用户

#### 文档管理接口
- POST /documents/upload - 上传文档
- GET /documents - 获取文档列表
- GET /documents/{id} - 获取文档详情
- PUT /documents/{id} - 更新文档
- DELETE /documents/{id} - 删除文档

#### 分类管理接口
- GET /classifications - 获取分类列表
- POST /classifications - 创建分类
- GET /classifications/{id} - 获取分类详情
- PUT /classifications/{id} - 更新分类
- DELETE /classifications/{id} - 删除分类

#### 搜索接口
- POST /search/semantic - 语义搜索
- POST /search/hybrid - 混合搜索

#### 知识图谱接口
- GET /graph/stats - 获取图谱统计
- GET /graph/nodes - 查询节点
- GET /graph/relationships - 查询关系

#### 统计信息接口
- GET /stats/system - 系统统计
- GET /stats/user - 用户统计

### 详细API文档

启动服务后访问 http://localhost:8000/docs 查看完整的交互式API文档（Swagger UI）。

---

## 离线部署

### 适用场景

- 内网环境无法访问互联网
- 需要在隔离网络中部署
- 对安全性有特殊要求

### 准备工作（在有网环境）

#### 1. 下载Python依赖

```bash
mkdir -p offline_packages/python
pip download -r backend/requirements.txt -d ./offline_packages/python
tar -czf python_packages.tar.gz offline_packages/python
```

#### 2. 下载Node.js依赖

```bash
# 前端依赖
cd frontend && npm install && cd ..
tar -czf frontend_node_modules.tar.gz frontend/node_modules

# MCP Server依赖
cd mcp-server && npm install && cd ..
tar -czf mcp_node_modules.tar.gz mcp-server/node_modules
```

### 内网部署步骤

#### 1. 解压依赖包

```bash
tar -xzf python_packages.tar.gz
cd frontend && tar -xzf ../frontend_node_modules.tar.gz && cd ..
cd mcp-server && tar -xzf ../mcp_node_modules.tar.gz && cd ..
```

#### 2. 安装Python依赖

```bash
pip install --no-index --find-links=./offline_packages/python -r backend/requirements.txt
```

#### 3. 配置内网环境

编辑 .env 文件：

```bash
ENVIRONMENT=production
NETWORK_ENV=intranet
EMBEDDING_API_URL=http://internal-embedding-service:8080
DATABASE_URL=postgresql://user:password@internal-db:5432/aicontext
```

#### 4. 启动服务

```bash
python start.py
```

### Docker离线部署（推荐）

```bash
# 在有网环境构建镜像
docker-compose build
docker save -o ai_context_images.tar $(docker images --format "{{.Repository}}:{{.Tag}}" | grep ai-context)

# 在内网环境加载并运行
docker load -i ai_context_images.tar
docker-compose up -d
```

### 注意事项

1. Embedding服务: 内网环境需要提前部署Embedding API服务或使用本地模型
2. 数据库服务: 确保PostgreSQL、Redis、Neo4j等已在内网部署
3. 版本匹配: 确保Python和Node.js版本与开发环境一致
4. 系统架构: 注意CPU架构匹配（x86_64 vs ARM64）

---

## 开发指南

### 后端开发

```bash
cd backend
python run_dev.py
```

开发服务器特性：
- 自动重载（修改代码后自动重启）
- 详细的调试日志
- SQLite数据库（无需额外配置）

#### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试文件
python -m pytest tests/test_api.py

# 显示详细输出
python -m pytest tests/ -v

# 生成测试覆盖率报告
python -m pytest tests/ --cov=app --cov-report=html
```

### 前端开发

```bash
cd frontend
npm start
```

开发服务器特性：
- 热模块替换（HMR）
- 自动打开浏览器
- 代理API请求到后端

#### 代码规范

```bash
# 运行ESLint检查
npm run lint

# 自动修复代码格式
npm run lint:fix

# 类型检查
npm run type-check
```

### MCP Server开发

```bash
cd mcp-server
npm run dev
```

### MCP Server 配置（用于 AI 助手集成）

MCP Server 实现了 Model Context Protocol 协议，可以让 AI 助手（如 Claude Desktop）直接访问团队知识库。

#### 1. 构建 MCP Server

```bash
cd mcp-server
npm install
npm run build
```

#### 2. 配置 Claude Desktop

**Windows 配置文件位置**:
```
%APPDATA%\Claude\claude_desktop_config.json
```

实际路径通常是:
```
C:\Users\你的用户名\AppData\Roaming\Claude\claude_desktop_config.json
```

**macOS/Linux 配置文件位置**:
```
~/.config/Claude/claude_desktop_config.json
```

**配置内容**:

在配置文件中添加以下内容（如果文件不存在，创建一个新文件）：

```json
{
  "mcpServers": {
    "team-context-server": {
      "command": "node",
      "args": [
        "D:\\project\\RAGStrict\\mcp-server\\dist\\index.js"
      ],
      "env": {
        "RAG_ENGINE_URL": "http://127.0.0.1:8000",
        "LOG_LEVEL": "info",
        "CACHE_TTL": "300"
      }
    }
  }
}
```

**注意**: 
- Windows 用户需要将路径 `D:\\project\\RAGStrict` 替换为你的实际项目路径
- macOS/Linux 用户路径示例: `/home/username/RAGStrict/mcp-server/dist/index.js`
- 路径中的反斜杠 `\` 在 JSON 中需要写成双反斜杠 `\\`

#### 3. 启动服务并测试

1. 启动后端服务:
```bash
python start.py
```

2. 重启 Claude Desktop

3. 在 Claude 中测试 MCP 功能:
   - "搜索 Python FastAPI 的代码示例"
   - "获取团队的编码规范"
   - "查询知识图谱中的 User 实体"

#### 4. MCP Server 提供的工具

Claude 可以使用以下工具访问你的知识库:

- `search_code_examples`: 搜索代码示例和 Demo
- `get_design_document`: 获取设计文档
- `get_coding_standards`: 获取编码规范
- `query_knowledge_graph`: 查询知识图谱

#### 5. 日志和故障排查

MCP Server 日志位置:
- Windows: `D:\project\RAGStrict\mcp-server\logs\`
- macOS/Linux: `/path/to/RAGStrict/mcp-server/logs/`

Claude Desktop 日志位置:
- Windows: `%APPDATA%\Claude\logs\`
- macOS: `~/Library/Logs/Claude/`

常见问题:
- MCP Server 未启动: 检查 Node.js 版本 >= 18.0
- 连接后端失败: 确保后端服务在 8000 端口运行
- 权限错误: Windows 用户尝试以管理员身份运行 Claude Desktop

#### 6. 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `RAG_ENGINE_URL` | RAG引擎地址 | `http://127.0.0.1:8000` |
| `BACKEND_API_URL` | 后端API地址 | `http://127.0.0.1:8000/api/v1` |
| `LOG_LEVEL` | 日志级别 (debug/info/warn/error) | `info` |
| `CACHE_TTL` | 缓存过期时间(秒) | `300` |

---

## 故障排除

### 端口被占用

修改 .env 文件中的端口配置：

```bash
BACKEND_PORT=8001
FRONTEND_PORT=3001
MCP_PORT=3002
```

或者关闭占用端口的进程：

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F

# Linux/macOS
lsof -i :8000
kill -9 <进程ID>
```

### 依赖安装失败

检查Python版本：

```bash
python --version  # 应该 >= 3.8
```

检查Node.js版本：

```bash
node --version  # 应该 >= 16.0
```

清除缓存重试：

```bash
# Python
pip cache purge
pip install -r backend/requirements.txt

# Node.js
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 数据库连接失败

开发环境使用SQLite（默认，无需配置）。如果使用PostgreSQL，检查：
- 数据库服务是否启动
- 连接字符串是否正确
- 用户权限是否足够

### 前端无法连接后端

1. 确认后端服务已启动
2. 检查后端端口是否正确（默认8000）
3. 检查前端API配置文件 frontend/src/config/apiConfig.ts
4. 查看浏览器控制台的错误信息

### 文档上传失败

1. 检查文件大小（默认限制100MB）
2. 检查文件格式是否支持
3. 确认 backend/uploads/ 目录有写入权限
4. 查看后端日志获取详细错误信息

### 语义搜索不工作

1. 确认已上传文档并完成索引
2. 检查Embedding服务配置
3. 确认ChromaDB或向量数据库服务正常
4. 查看后端日志中的Embedding相关错误

---

## 性能优化

### 生产环境建议

1. 使用PostgreSQL替代SQLite - 更好的并发性能
2. 启用Redis缓存 - 缓存常用查询结果
3. 配置反向代理 - 使用Nginx或Caddy，启用GZIP压缩
4. 启用生产模式 - ENVIRONMENT=production

### 监控和日志

- 后端日志位置: backend/logs/
- MCP服务日志: mcp-server/logs/
- 前端生产构建: frontend/build/

---

## 许可证

MIT License

---

## 联系方式

- 项目地址: https://github.com/MOONL0323/RAGStrict
- 问题反馈: https://github.com/MOONL0323/RAGStrict/issues
