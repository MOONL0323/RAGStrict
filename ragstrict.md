---
description: "RAGStrict MCP 服务 - 团队知识库 AI 增强系统"
mcp_server_url: "http://localhost:8000"
mcp_server_name: "team-context-mcp-server"
version: "1.0.0"
---

# RAGStrict MCP 服务

RAGStrict 是一个基于 Graph RAG 的团队知识库 AI 增强系统，通过 Model Context Protocol (MCP) 为 AI Agent 提供代码示例、设计文档、编码规范和知识图谱查询能力。

## 🎯 核心功能

RAGStrict MCP 服务提供以下核心工具供 AI Agent 调用：

## 🚀 主要功能

### 1. 🔍 search_code_examples - 代码示例搜索

搜索团队代码库中的代码示例和最佳实践。

**MCP 工具调用:**
```json
{
  "name": "search_code_examples",
  "arguments": {
    "query": "如何使用 FastAPI 创建异步 REST API",
    "language": "python",
    "framework": "fastapi",
    "team": "backend",
    "project": "user-service",
    "limit": 5
  }
}
```

**后端 API 端点:** `POST /api/v1/mcp/search-code-examples`

**参数说明：**
- `query` (string, 必需): 搜索查询，描述需要的功能或代码模式
- `language` (string, 可选): 编程语言 - python | typescript | javascript | java | go | cpp
- `framework` (string, 可选): 框架名称 - fastapi | react | express | django | spring | gin 等
- `team` (string, 可选): 团队名称，用于过滤特定团队的代码
- `project` (string, 可选): 项目名称，用于过滤特定项目的代码
- `limit` (number, 可选): 返回结果数量限制 (1-20，默认 5)

**返回结果示例:**
```json
{
  "success": true,
  "data": [
    {
      "id": "doc_123",
      "title": "FastAPI 异步数据库操作示例",
      "content": "...",
      "code": "async def get_users(db: AsyncSession):\n    ...",
      "file_path": "backend/examples/fastapi_async.py",
      "score": 0.95,
      "metadata": {
        "language": "python",
        "framework": "fastapi",
        "team": "backend"
      }
    }
  ],
  "total": 1
}
```

### 2. 📄 get_design_docs - 设计文档查询

获取相关的设计文档和架构说明。

**MCP 工具调用:**
```json
{
  "name": "get_design_docs",
  "arguments": {
    "query": "用户认证模块的 API 设计",
    "doc_type": "api_design",
    "team": "backend",
    "project": "user-service",
    "component": "auth"
  }
}
```

**后端 API 端点:** 
- 主要: `POST /api/v1/design/design-docs`
- 备用: `GET /api/v1/documents/search`

**参数说明：**
- `query` (string, 必需): 查询描述，如功能模块、架构组件等
- `doc_type` (string, 可选): 文档类型 - api_design | architecture | database_design | business_logic
- `team` (string, 可选): 团队名称
- `project` (string, 可选): 项目名称
- `component` (string, 可选): 组件名称

**返回结果示例:**
```json
{
  "success": true,
  "data": [
    {
      "id": "design_456",
      "title": "用户认证 API 设计文档",
      "content": "## 认证流程\n...",
      "document_type": "api_design",
      "team": "backend",
      "project": "user-service",
      "tags": ["auth", "security", "jwt"],
      "score": 0.92
    }
  ]
}
```

### 3. 📋 get_coding_standards - 编码规范获取

获取团队编码规范和代码风格指南。

**MCP 工具调用:**
```json
{
  "name": "get_coding_standards",
  "arguments": {
    "language": "python",
    "category": "naming"
  }
}
```

**后端 API 端点:** 
- 主要: `GET /api/v1/mcp/coding-standards/{language}?category={category}`
- 备用: `GET /api/v1/documents/search`

**参数说明：**
- `language` (string, 必需): 编程语言 - python | typescript | javascript | java | go | cpp
- `category` (string, 可选): 规范类别 - naming | structure | testing | documentation | security

**返回结果示例:**
```json
{
  "success": true,
  "data": {
    "language": "python",
    "naming_conventions": {
      "variables": "snake_case",
      "functions": "snake_case",
      "classes": "PascalCase",
      "constants": "UPPER_SNAKE_CASE"
    },
    "code_structure": {
      "max_line_length": "88 (black)",
      "indentation": "4 spaces"
    },
    "best_practices": [
      "遵循 PEP 8 编码规范",
      "使用类型提示 (Type Hints)",
      "编写文档字符串 (Docstrings)"
    ],
    "tools": {
      "formatters": ["black", "autopep8"],
      "linters": ["pylint", "flake8", "mypy"],
      "test_frameworks": ["pytest", "unittest"]
    }
  }
}
```

### 4. 🕸️ query_knowledge_graph - 知识图谱查询

查询知识图谱中的实体关系和语义信息。

**MCP 工具调用:**
```json
{
  "name": "query_knowledge_graph",
  "arguments": {
    "entity": "UserService",
    "relation_type": "CALLS",
    "depth": 2
  }
}
```

**后端 API 端点:** 
- 实体查询: `GET /api/v1/graph/entity/{entity_name}`
- 关系查询: `GET /api/v1/graph/related/{entity_name}?max_depth={depth}`

**参数说明：**
- `entity` (string, 必需): 要查询的实体名称 (类名、函数名、模块名等)
- `relation_type` (string, 可选): 关系类型 - CALLS | INHERITS | USES | DEPENDS_ON | IMPLEMENTS
- `depth` (number, 可选): 查询深度 (1-5，默认 2)

**返回结果示例:**
```json
{
  "success": true,
  "data": {
    "entity_info": {
      "id": "UserService",
      "name": "UserService",
      "type": "class",
      "properties": {
        "file_path": "backend/services/user_service.py",
        "line_number": 15
      }
    },
    "relationships": [
      {
        "id": "rel_1",
        "source": "UserService",
        "target": "UserRepository",
        "type": "USES",
        "properties": {}
      }
    ],
    "related_entities": [
      {
        "id": "UserRepository",
        "name": "UserRepository",
        "type": "class",
        "relationship": "USES"
      }
    ],
    "usage_examples": []
  }
}
```

### 5. � get_knowledge_base_stats - 知识库统计

获取知识库的总体统计信息。

**MCP 工具调用:**
```json
{
  "name": "get_knowledge_base_stats",
  "arguments": {}
}
```

**后端 API 端点:** `GET /api/v1/stats/knowledge-base`

**返回结果示例:**
```json
{
  "success": true,
  "data": {
    "total_documents": 156,
    "total_chunks": 1247,
    "total_entities": 523,
    "total_relations": 892,
    "languages": ["python", "typescript", "javascript"],
    "teams": ["backend", "frontend", "devops"],
    "projects": ["user-service", "api-gateway", "web-app"],
    "last_updated": "2025-10-15T15:30:00"
  }
}
```

## 🔧 MCP 服务配置

### Claude Desktop 配置

在 Claude Desktop 中使用 RAGStrict MCP 服务，需要配置 `claude_desktop_config.json`:

**配置文件位置:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**配置内容:**
```json
{
  "mcpServers": {
    "ragstrict": {
      "command": "node",
      "args": [
        "D:/project/RAGStrict/mcp-server/dist/index.js"
      ],
      "env": {
        "RAG_ENGINE_URL": "http://localhost:8000",
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

**重要说明:**
1. 将 `D:/project/RAGStrict` 替换为你的实际项目路径
2. 确保 MCP Server 已编译: `cd mcp-server && npm run build`
3. 修改配置后需要重启 Claude Desktop

## 📋 使用前提

### 1. 启动后端服务
```bash
# 开发环境
python start.py

# 或直接运行
cd backend
python run_dev.py
```

**验证服务状态:**
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 2. 编译 MCP 服务器
```bash
cd mcp-server
npm install
npm run build
```

### 3. 配置并重启 Claude Desktop
- 按照上述配置编辑 `claude_desktop_config.json`
- 完全退出并重启 Claude Desktop
- 在 Claude 中验证 MCP 服务器已连接

## 🌟 AI Agent 使用场景

### 场景 1: 代码开发辅助
**用户提问:** "我需要实现一个用户认证的 API，有没有相关的代码示例?"

**AI Agent 调用流程:**
1. 调用 `search_code_examples` 搜索认证相关代码
2. 调用 `get_design_docs` 获取认证模块设计文档
3. 调用 `get_coding_standards` 获取 Python 编码规范
4. 综合以上信息给用户提供完整的实现方案

### 场景 2: 代码架构理解
**用户提问:** "UserService 这个类都调用了哪些其他模块?"

**AI Agent 调用流程:**
1. 调用 `query_knowledge_graph` 查询 UserService 实体
2. 分析返回的关系图谱
3. 对每个相关实体调用 `query_knowledge_graph` 获取详细信息
4. 生成架构关系图和说明文档

### 场景 3: 代码规范检查
**用户提问:** "这段 TypeScript 代码符合团队规范吗?"

**AI Agent 调用流程:**
1. 调用 `get_coding_standards` 获取 TypeScript 规范
2. 对照规范检查代码
3. 调用 `search_code_examples` 查找标准示例
4. 提供改进建议和代码重构方案

### 场景 4: 新功能开发
**用户提问:** "我要开发一个支付模块，需要参考哪些文档和代码?"

**AI Agent 调用流程:**
1. 调用 `get_design_docs` 搜索支付相关设计文档
2. 调用 `search_code_examples` 查找支付集成示例
3. 调用 `query_knowledge_graph` 查询相关模块依赖
4. 调用 `get_knowledge_base_stats` 确认可用资源
5. 提供完整的开发指南和参考资料

## 📚 后端 API 端点列表

以下是 MCP 服务调用的后端 API 端点:

| 功能 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 搜索代码示例 | POST | `/api/v1/mcp/search-code-examples` | 搜索 demo 代码和示例 |
| 设计文档查询 | POST | `/api/v1/design/design-docs` | 查询设计文档 |
| 文档搜索 (备用) | GET | `/api/v1/documents/search` | 通用文档搜索 |
| 获取编码规范 | GET | `/api/v1/mcp/coding-standards/{language}` | 获取指定语言规范 |
| 查询图谱实体 | GET | `/api/v1/graph/entity/{entity_name}` | 查询实体信息 |
| 查询关联实体 | GET | `/api/v1/graph/related/{entity_name}` | 查询实体关系 |
| 知识库统计 | GET | `/api/v1/stats/knowledge-base` | 获取知识库统计 |
| 仪表板统计 | GET | `/api/v1/stats/dashboard` | 获取总览统计 |

**完整 API 文档:** 启动后端后访问 http://localhost:8000/docs

## ⚠️ 注意事项

### AI Agent 使用建议

1. **首次使用前**: 确保知识库已上传相关文档
   - 设计文档 (API、架构、数据库设计)
   - 代码示例 (Demo、最佳实践)
   - 编码规范文档
   - 项目文档

2. **查询优化技巧**:
   - 使用具体的技术术语和关键词
   - 指定 language、framework、team 等过滤条件
   - 先用 `get_knowledge_base_stats` 了解可用资源
   - 组合使用多个工具获取全面信息

3. **错误处理**:
   - 捕获 API 调用异常并提供友好提示
   - 当主端点失败时,尝试备用端点
   - 记录失败原因,帮助用户排查问题

4. **性能考虑**:
   - 结果已在后端缓存,重复查询很快
   - 合理设置 limit 参数避免返回过多结果
   - 图谱查询设置合适的 depth 避免过深遍历

## 🐛 故障排除

### 常见问题及解决方案

#### 1. MCP 服务器连接失败
**症状:** Claude Desktop 无法连接到 RAGStrict MCP 服务器

**排查步骤:**
1. 检查后端服务是否运行: 访问 http://localhost:8000/health
2. 检查 MCP Server 是否编译: 查看 `mcp-server/dist/index.js` 是否存在
3. 检查 Claude 配置文件路径是否正确
4. 查看 Claude Desktop 日志 (Help -> Developer Tools -> Console)
5. 重启 Claude Desktop

#### 2. API 返回 404 错误
**症状:** MCP 调用返回 404 Not Found

**常见原因:**
- 端点路径错误: 检查 API 端点是否与文档一致
- 路由未注册: 确认 `backend/app/api/v1/__init__.py` 中已注册路由
- 服务未启动: 确认后端服务正在运行

**解决方法:**
```bash
# 查看后端日志
tail -f backend/logs/app.log

# 访问 API 文档确认端点
http://localhost:8000/docs
```

#### 3. 查询结果为空
**症状:** 调用成功但返回空结果

**可能原因:**
- 知识库没有相关文档
- 查询关键词不准确
- 过滤条件过于严格

**解决方法:**
```json
// 先调用统计接口查看可用资源
{
  "name": "get_knowledge_base_stats",
  "arguments": {}
}

// 放宽查询条件
{
  "name": "search_code_examples",
  "arguments": {
    "query": "API",  // 使用更宽泛的关键词
    "limit": 20      // 增加返回数量
  }
}
```

#### 4. 类型错误或验证失败
**症状:** 参数验证失败

**常见错误:**
- language 不在支持列表: 必须是 python/typescript/javascript/java/go/cpp
- limit 超出范围: 必须在 1-20 之间
- depth 超出范围: 必须在 1-5 之间

**正确调用示例:**
```json
{
  "name": "search_code_examples",
  "arguments": {
    "query": "database connection",
    "language": "python",  // ✓ 小写,支持的语言
    "limit": 5             // ✓ 在有效范围内
  }
}
```

### 日志文件位置

- **后端日志:** `backend/logs/`
  - `app.log` - 应用日志
  - `error.log` - 错误日志
  
- **MCP 服务日志:** `mcp-server/logs/`
  - `mcp-server-YYYY-MM-DD.log` - 按日期分割的日志

### 调试技巧

1. **启用详细日志:**
   ```bash
   # 设置环境变量
   export LOG_LEVEL=debug
   python start.py
   ```

2. **使用 API 文档测试:**
   - 访问 http://localhost:8000/docs
   - 直接在 Swagger UI 中测试 API
   - 确认端点可用后再通过 MCP 调用

3. **查看 MCP 调用日志:**
   - 打开 Claude Desktop 开发者工具
   - 查看 Network 标签查看请求详情
   - 检查 Console 标签查看错误信息

## 📚 相关文档

- [项目 README](README.md) - 项目概述和快速开始
- [MCP Server README](mcp-server/README.md) - MCP 服务器详细配置
- [API 文档](http://localhost:8000/docs) - FastAPI Swagger 文档
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 官方文档

## 🔄 版本更新日志

### v1.0.0 (2025-10-15)
- ✅ 修复所有 MCP 端点路径
- ✅ 添加 design_docs 路由注册
- ✅ 新增 /stats/knowledge-base 端点
- ✅ 优化知识图谱查询,使用现有 graph API
- ✅ 完善参数验证和类型定义
- ✅ 更新 MCP 配置文档