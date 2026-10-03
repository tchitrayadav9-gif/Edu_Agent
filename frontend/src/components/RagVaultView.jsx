import React, { useState, useEffect } from 'react';
import { BookOpen, Upload, FileText, Search, CheckCircle, Trash2, RefreshCw } from 'lucide-react';
import { api } from '../api';

export default function RagVaultView({ currentUser }) {
  const targetUserId = currentUser?.user_id || currentUser?.id || "chitra_demo_user";
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState('What does my AI notes say about search algorithms and A*?');
  const [ragResult, setRagResult] = useState(null);
  const [querying, setQuerying] = useState(false);

  const fetchDocs = async () => {
    setLoading(true);
    try {
      const res = await api.getDocuments(targetUserId);
      setDocs(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocs();
  }, [targetUserId]);


  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    try {
      await api.uploadDocument(file);
      setFile(null);
      fetchDocs();
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setQuerying(true);
    try {
      const res = await api.queryDocuments(query);
      setRagResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setQuerying(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-teal-400" /> RAG Academic Document Vault
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Upload course notes, textbook chapters, and resumes (PDF, DOCX, TXT) for vector chunk indexing and grounded citation Q&A.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Upload & Document List */}
        <div className="space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Upload className="w-4 h-4 text-teal-400" /> Upload Document
            </h3>
            <form onSubmit={handleUpload} className="space-y-3">
              <input
                type="file"
                accept=".pdf,.docx,.doc,.txt,.md"
                onChange={(e) => setFile(e.target.files[0])}
                className="block w-full text-xs text-slate-400 file:mr-3 file:py-2 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-slate-800 file:text-teal-400 hover:file:bg-slate-700 cursor-pointer"
              />
              <button
                type="submit"
                disabled={!file || uploading}
                className="w-full bg-teal-500 hover:bg-teal-600 disabled:opacity-50 text-slate-950 font-bold text-xs py-2 px-3 rounded-lg transition"
              >
                {uploading ? 'Chunking & Indexing...' : 'Upload to Vector Store'}
              </button>
            </form>
          </div>

          {/* Document List */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <FileText className="w-4 h-4 text-teal-400" /> Indexed Documents ({docs.length})
            </h3>
            <div className="space-y-2">
              {docs.length === 0 ? (
                <p className="text-xs text-slate-500 italic">No custom documents uploaded yet.</p>
              ) : (
                docs.map((doc, idx) => (
                  <div key={idx} className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-between text-xs">
                    <div>
                      <span className="font-medium text-slate-200 block">{doc.filename}</span>
                      <span className="text-[10px] text-slate-400">{doc.chunk_count || 3} Chunks Indexed • {doc.file_type?.toUpperCase()}</span>
                    </div>
                    <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Right Column: RAG Query & Grounded Answer */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow">
            <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Search className="w-4 h-4 text-teal-400" /> Test RAG Semantic Retrieval & Citations
            </h3>

            <form onSubmit={handleQuery} className="flex gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask a question about your uploaded notes..."
                className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-teal-500"
              />
              <button
                type="submit"
                disabled={querying}
                className="bg-teal-500 hover:bg-teal-600 text-slate-950 font-bold text-xs px-4 py-2 rounded-lg transition"
              >
                {querying ? 'Searching...' : 'Run RAG'}
              </button>
            </form>

            {/* Answer Display */}
            {ragResult && (
              <div className="mt-4 p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-teal-400">Grounded Agent Answer</span>
                  <span className="text-[11px] text-slate-400">{ragResult.citations?.length || 0} Sources Cited</span>
                </div>

                <div className="text-xs text-slate-200 whitespace-pre-wrap leading-relaxed">
                  {ragResult.answer}
                </div>

                {ragResult.citations?.length > 0 && (
                  <div className="pt-2 border-t border-slate-800/80">
                    <span className="text-[10px] text-slate-500 font-semibold block mb-1">Source Citations:</span>
                    <div className="flex flex-wrap gap-2">
                      {ragResult.citations.map((c, i) => (
                        <span key={i} className="text-[10px] bg-slate-800 text-teal-300 px-2 py-0.5 rounded border border-slate-700">
                          📄 {c.filename} (Chunk #{c.chunk_index + 1})
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
