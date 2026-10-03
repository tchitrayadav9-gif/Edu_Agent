const API_BASE = "http://localhost:8000";

// Helper to get active user ID and token from localStorage
export const getStoredAuth = () => {
  try {
    const token = localStorage.getItem("edumind_token") || "";
    const userStr = localStorage.getItem("edumind_user");
    const user = userStr ? JSON.parse(userStr) : null;
    return {
      token,
      user,
      userId: user?.user_id || user?.id || "chitra_demo_user"
    };
  } catch (e) {
    return { token: "", user: null, userId: "chitra_demo_user" };
  }
};

export const setStoredAuth = (token, user) => {
  if (token) localStorage.setItem("edumind_token", token);
  if (user) localStorage.setItem("edumind_user", JSON.stringify(user));
};

export const clearStoredAuth = () => {
  localStorage.removeItem("edumind_token");
  localStorage.removeItem("edumind_user");
};

const getHeaders = (customHeaders = {}) => {
  const { token, userId } = getStoredAuth();
  const headers = {
    "Content-Type": "application/json",
    "X-User-Id": userId,
    ...customHeaders
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
};

export const api = {
  // Auth
  register: async (userData) => {
    const res = await fetch(`${API_BASE}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Registration failed");
    if (data.access_token && data.user) {
      setStoredAuth(data.access_token, data.user);
    }
    return data;
  },

  login: async (username, password) => {
    const res = await fetch(`${API_BASE}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Invalid login credentials");
    if (data.access_token) {
      const userObj = data.user || {
        id: data.user_id,
        user_id: data.user_id,
        username: data.username,
        name: data.name
      };
      setStoredAuth(data.access_token, userObj);
    }
    return data;
  },

  getMe: async () => {
    const { token } = getStoredAuth();
    if (!token) return null;
    const res = await fetch(`${API_BASE}/api/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) return null;
    return res.json();
  },

  // Central Agent Chat
  chat: async (message, conversationId, provider = "auto", userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: getHeaders({ "X-User-Id": targetUserId }),
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
        provider
      })
    });
    return res.json();
  },

  // Dashboard
  getDashboard: async (userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/dashboard`, {
      headers: getHeaders({ "X-User-Id": targetUserId })
    });
    return res.json();
  },

  // Student Profile
  getProfile: async (userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/student/profile`, {
      headers: getHeaders({ "X-User-Id": targetUserId })
    });
    return res.json();
  },
  updateProfile: async (updates, userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/student/profile`, {
      method: "PUT",
      headers: getHeaders({ "X-User-Id": targetUserId }),
      body: JSON.stringify(updates)
    });
    return res.json();
  },
  getKnowledgeGraph: async (userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/student/graph`, {
      headers: getHeaders({ "X-User-Id": targetUserId })
    });
    return res.json();
  },

  // Memory
  getMemories: async (userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/memory`, {
      headers: getHeaders({ "X-User-Id": targetUserId })
    });
    return res.json();
  },
  createMemory: async (memoryData, userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/memory`, {
      method: "POST",
      headers: getHeaders({ "X-User-Id": targetUserId }),
      body: JSON.stringify(memoryData)
    });
    return res.json();
  },
  deleteMemory: async (memoryId, userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/memory/${memoryId}`, {
      method: "DELETE",
      headers: getHeaders({ "X-User-Id": targetUserId })
    });
    return res.json();
  },

  // Career
  analyzeCareer: async (targetRole = "AI Engineer", userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/career/analyze`, {
      method: "POST",
      headers: getHeaders({ "X-User-Id": targetUserId }),
      body: JSON.stringify({ target_role: targetRole })
    });
    return res.json();
  },

  // Study
  generateStudyPlan: async (options = {}, userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/study/generate`, {
      method: "POST",
      headers: getHeaders({ "X-User-Id": targetUserId }),
      body: JSON.stringify(options)
    });
    return res.json();
  },
  getStudyProgress: async (userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/study/progress`, {
      headers: getHeaders({ "X-User-Id": targetUserId })
    });
    return res.json();
  },
  updateStudyProgress: async (topic, progress, userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/study/progress`, {
      method: "PUT",
      headers: getHeaders({ "X-User-Id": targetUserId }),
      body: JSON.stringify({ topic, progress })
    });
    return res.json();
  },

  // Documents / RAG
  getDocuments: async (userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/documents`, {
      headers: getHeaders({ "X-User-Id": targetUserId })
    });
    return res.json();
  },
  uploadDocument: async (file, userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const formData = new FormData();
    formData.append("file", file);
    const { token } = getStoredAuth();
    const headers = { "X-User-Id": targetUserId };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(`${API_BASE}/api/documents/upload`, {
      method: "POST",
      headers,
      body: formData
    });
    return res.json();
  },
  queryDocuments: async (query, userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/documents/query`, {
      method: "POST",
      headers: getHeaders({ "X-User-Id": targetUserId }),
      body: JSON.stringify({ query })
    });
    return res.json();
  },

  // Interview
  startInterview: async (targetRole = "AI Engineer", topic = "Machine Learning", userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/interview/start`, {
      method: "POST",
      headers: getHeaders({ "X-User-Id": targetUserId }),
      body: JSON.stringify({ target_role: targetRole, topic })
    });
    return res.json();
  },
  submitAnswer: async (sessionId, answer, userId = null) => {
    const targetUserId = userId || getStoredAuth().userId;
    const res = await fetch(`${API_BASE}/api/interview/answer`, {
      method: "POST",
      headers: getHeaders({ "X-User-Id": targetUserId }),
      body: JSON.stringify({ session_id: sessionId, answer })
    });
    return res.json();
  },

  // Classical Search
  runSearch: async (startTopic, goalTopic, algorithm) => {
    const res = await fetch(`${API_BASE}/api/search/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start_topic: startTopic, goal_topic: goalTopic, algorithm })
    });
    return res.json();
  },
  compareSearch: async (startTopic, goalTopic) => {
    const res = await fetch(`${API_BASE}/api/search/compare`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start_topic: startTopic, goal_topic: goalTopic })
    });
    return res.json();
  },

  // Reasoning
  runForwardChaining: async (facts) => {
    const res = await fetch(`${API_BASE}/api/reasoning/forward`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ facts })
    });
    return res.json();
  },
  runBackwardChaining: async (goalKey, goalValue, facts) => {
    const res = await fetch(`${API_BASE}/api/reasoning/backward`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal_key: goalKey, goal_value: goalValue, facts })
    });
    return res.json();
  },

  // Evaluation
  runEvaluation: async (sampleSize = 50, provider = "auto") => {
    const res = await fetch(`${API_BASE}/api/evaluation/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sample_size: sampleSize, provider })
    });
    return res.json();
  },
  getLatestEvaluation: async () => {
    const res = await fetch(`${API_BASE}/api/evaluation/latest`);
    return res.json();
  },

  // MCP & Ollama
  getMcpTools: async () => {
    const res = await fetch(`${API_BASE}/api/mcp/tools`);
    return res.json();
  },
  getOllamaStatus: async () => {
    const res = await fetch(`${API_BASE}/api/mcp/ollama/status`);
    return res.json();
  }
};
