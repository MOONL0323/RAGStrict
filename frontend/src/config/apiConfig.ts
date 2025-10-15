/**
 * API配置
 * 统一管理所有API相关配置
 */

// API基础URL
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// API版本前缀
export const API_V1_PREFIX = '/api/v1';

// 完整的API基础路径
export const API_V1_BASE = `${API_BASE_URL}${API_V1_PREFIX}`;

// 超时配置
export const API_TIMEOUT = 30000; // 30秒

// API端点配置
export const API_ENDPOINTS = {
  // 认证相关
  AUTH: {
    LOGIN: `${API_V1_BASE}/auth/login`,
    REGISTER: `${API_V1_BASE}/auth/register`,
    ME: `${API_V1_BASE}/auth/me`,
    LOGOUT: `${API_V1_BASE}/auth/logout`,
  },
  
  // 文档相关
  DOCUMENTS: {
    UPLOAD: `${API_V1_BASE}/documents/upload`,
    LIST: `${API_V1_BASE}/documents/list`,
    SEARCH: `${API_V1_BASE}/documents/search`,
    DETAIL: (id: string) => `${API_V1_BASE}/documents/${id}`,
    FULL_DETAIL: (id: string) => `${API_V1_BASE}/documents/${id}/detail`,
    DOWNLOAD: (id: string) => `${API_V1_BASE}/documents/${id}/download`,
    DELETE: (id: string) => `${API_V1_BASE}/documents/${id}`,
    CHUNKS: (id: string) => `${API_V1_BASE}/documents/${id}/chunks`,
    CHUNK: (id: string) => `${API_V1_BASE}/documents/${id}/chunk`,
    EMBED: (id: string) => `${API_V1_BASE}/documents/${id}/embed`,
  },
  
  // 分类相关
  CLASSIFICATIONS: {
    OPTIONS: `${API_V1_BASE}/classifications/options`,
    DEV_TYPES: `${API_V1_BASE}/classifications/dev-types`,
    TEAMS: `${API_V1_BASE}/classifications/teams`,
  },
  
  // 统计相关
  STATS: {
    DASHBOARD: `${API_V1_BASE}/stats/dashboard`,
    DOCUMENTS: `${API_V1_BASE}/stats/documents`,
    ENTITIES: `${API_V1_BASE}/stats/entities`,
    CHUNKS: `${API_V1_BASE}/stats/chunks`,
    USERS: `${API_V1_BASE}/stats/users`,
  },
  
  // 搜索相关
  SEARCH: {
    SEMANTIC: `${API_V1_BASE}/search/semantic`,
    HYBRID: `${API_V1_BASE}/search/hybrid`,
  },
  
  // 知识图谱相关
  GRAPH: {
    STATS: `${API_V1_BASE}/graph/stats`,
    NODES: `${API_V1_BASE}/graph/nodes`,
    RELATIONSHIPS: `${API_V1_BASE}/graph/relationships`,
  },
  
  // 实体相关
  ENTITIES: {
    EXTRACT: `${API_V1_BASE}/entities/extract`,
  },
};

export default {
  API_BASE_URL,
  API_V1_PREFIX,
  API_V1_BASE,
  API_TIMEOUT,
  API_ENDPOINTS,
};
