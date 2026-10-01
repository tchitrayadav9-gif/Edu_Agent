const API_BASE = "http://localhost:8000";

export const api = {
  // Auth
  login: async (username, password) => {
    const res = await fetch(`${API_BASE}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    return res.json();
  },

  // Central Agent Chat
  chat: async (message, conversationId, provider = "auto", userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": userId
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
        provider
      })
    });
    return res.json();
  },

  // Dashboard
  getDashboard: async (userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/dashboard`, {
      headers: { "X-User-Id": userId }
    });
    return res.json();
  },

  // Student Profile
  getProfile: async (userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/student/profile`, {
      headers: { "X-User-Id": userId }
    });
    return res.json();
  },
  updateProfile: async (updates, userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/student/profile`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", "X-User-Id": userId },
      body: JSON.stringify(updates)
    });
    return res.json();
  },
  getKnowledgeGraph: async (userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/student/graph`, {
      headers: { "X-User-Id": userId }
    });
    return res.json();
  },

  // Memory
  getMemories: async (userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/memory`, {
      headers: { "X-User-Id": userId }
    });
    return res.json();
  },
  createMemory: async (memoryData, userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/memory`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-User-Id": userId },
      body: JSON.stringify(memoryData)
    });
    return res.json();
  },
  deleteMemory: async (memoryId, userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/memory/${memoryId}`, {
      method: "DELETE",
      headers: { "X-User-Id": userId }
    });
    return res.json();
  },

  // Career
  analyzeCareer: async (targetRole = "AI Engineer", userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/career/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-User-Id": userId },
      body: JSON.stringify({ target_role: targetRole })
    });
    return res.json();
  },

  // Study
  generateStudyPlan: async (options = {}, userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/study/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-User-Id": userId },
      body: JSON.stringify(options)
    });
    return res.json();
  },
  getStudyProgress: async (userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/study/progress`, {
      headers: { "X-User-Id": userId }
    });
    return res.json();
  },
  updateStudyProgress: async (topic, progress, userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/study/progress`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", "X-User-Id": userId },
      body: JSON.stringify({ topic, progress })
    });
    return res.json();
  },

  // Documents / RAG
  getDocuments: async (userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/documents`, {
      headers: { "X-User-Id": userId }
    });
    return res.json();
  },
  uploadDocument: async (file, userId = "chitra_demo_user") => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch(`${API_BASE}/api/documents/upload`, {
      method: "POST",
      headers: { "X-User-Id": userId },
      body: formData
    });
    return res.json();
  },
  queryDocuments: async (query, userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/documents/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-User-Id": userId },
      body: JSON.stringify({ query })
    });
    return res.json();
  },

  // Interview
  startInterview: async (targetRole = "AI Engineer", topic = "Machine Learning", userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/interview/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-User-Id": userId },
      body: JSON.stringify({ target_role: targetRole, topic })
    });
    return res.json();
  },
  submitAnswer: async (sessionId, answer, userId = "chitra_demo_user") => {
    const res = await fetch(`${API_BASE}/api/interview/answer`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-User-Id": userId },
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
