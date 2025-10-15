---
description: "调用 RAGStrict MCP 服务，搜索代码示例、设计文档、编码规范和知识图谱"
---

# RAGStrict MCP 服务调用命令

此命令用于调用 RAGStrict MCP 服务，提供以下功能：

## 🚀 主要功能

### 1. 代码示例搜索
搜索团队代码库中的代码示例和最佳实践

**用法示例：**
```
/ragstrict search_code_examples "如何使用 FastAPI 创建 REST API" --language python --framework fastapi
/ragstrict search_code_examples "React 组件状态管理" --language typescript --framework react
/ragstrict search_code_examples "数据库连接池配置" --language java --limit 3
```

**参数说明：**
- `query` (必需): 搜索查询，描述需要的功能或代码模式
- `--language` (可选): 编程语言 (python/typescript/javascript/java/go/cpp)
- `--framework` (可选): 框架名称 (fastapi/react/express等)
- `--limit` (可选): 返回结果数量限制 (1-20，默认5)

### 2. 设计文档查询
获取相关的设计文档和架构说明

**用法示例：**
```
/ragstrict get_design_docs "用户认证模块设计" --doc_type api_design --team backend
/ragstrict get_design_docs "数据库架构设计" --doc_type database_design --project user-service
/ragstrict get_design_docs "微服务架构" --doc_type architecture
```

**参数说明：**
- `query` (必需): 查询描述，如功能模块、架构组件等
- `--doc_type` (可选): 文档类型 (api_design/architecture/database_design/business_logic)
- `--team` (可选): 团队名称
- `--project` (可选): 项目名称

### 3. 编码规范获取
获取团队编码规范和代码风格指南

**用法示例：**
```
/ragstrict get_coding_standards --language python --category naming
/ragstrict get_coding_standards --language typescript --category testing
/ragstrict get_coding_standards --language java --category security
```

**参数说明：**
- `--language` (必需): 编程语言 (python/typescript/javascript/java/go/cpp)
- `--category` (可选): 规范类别 (naming/structure/testing/documentation/security)

### 4. 知识图谱查询
查询知识图谱中的实体关系和语义信息

**用法示例：**
```
/ragstrict query_knowledge_graph "UserService" --relation_type CALLS --depth 2
/ragstrict query_knowledge_graph "UserController" --relation_type USES
/ragstrict query_knowledge_graph "AuthMiddleware" --depth 3
```

**参数说明：**
- `entity` (必需): 要查询的实体名称
- `--relation_type` (可选): 关系类型 (CALLS/INHERITS/USES/DEPENDS_ON/IMPLEMENTS)
- `--depth` (可选): 查询深度 (1-5，默认2)

## 🔧 服务状态

### 检查服务状态
```
/ragstrict status
```

### 显示帮助信息
```
/ragstrict help
```

## 📋 使用前提

1. **启动后端服务**：
   ```bash
   python start.py
   ```

2. **确保 MCP 服务运行**：
   - 后端 API: http://localhost:8000
   - MCP 服务: http://localhost:3001

3. **配置 Claude Desktop**（如需在 Claude 中使用）：
   - 编辑 `%APPDATA%\Claude\claude_desktop_config.json`
   - 添加 RAGStrict MCP 服务器配置

## 🌟 使用场景

### 开发时
- 查找代码示例和最佳实践
- 了解项目架构和设计决策
- 遵循团队编码规范
- 理解代码模块间的关系

### 代码审查
- 检查代码是否符合规范
- 查找相关的设计文档
- 理解代码变更的影响范围

### 新成员入职
- 快速了解项目架构
- 学习团队编码规范
- 查找相关代码示例

## ⚠️ 注意事项

1. **首次使用前**：确保已上传相关文档到知识库
2. **网络连接**：确保后端服务和 MCP 服务正常运行
3. **查询优化**：使用具体的关键词可以获得更准确的结果
4. **结果缓存**：查询结果会被缓存以提高性能

## 🐛 故障排除

### 常见问题
1. **服务无响应**：检查后端服务是否在 8000 端口运行
2. **查询结果为空**：确保知识库中已包含相关文档
3. **权限错误**：检查文件访问权限和服务配置

### 日志位置
- 后端日志: `backend/logs/`
- MCP 服务日志: `mcp-server/logs/`

## 📚 相关文档

- [项目 README](README.md)
- [MCP 服务配置](mcp-server/README.md)
- [API 文档](http://localhost:8000/docs)