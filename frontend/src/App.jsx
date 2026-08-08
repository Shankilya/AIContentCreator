import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Bot, Sparkles } from 'lucide-react';
import Background3D from './components/Background3D';
import AgentFeed from './components/AgentFeed';

function App() {
  const [agentId, setAgentId] = useState(localStorage.getItem('agentId') || null);
  const [name, setName] = useState('Ada');
  const [domain, setDomain] = useState('AI Security');
  const [initializing, setInitializing] = useState(false);

  const handleInit = async (e) => {
    e.preventDefault();
    setInitializing(true);
    try {
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
      const res = await fetch(`${API_BASE_URL}/api/agent/init`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ persona: { name, domain } })
      });
      const data = await res.json();
      if (data.agentId) {
        setAgentId(data.agentId);
        localStorage.setItem('agentId', data.agentId);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setInitializing(false);
    }
  };

  return (
    <div className="min-h-screen text-white font-sans selection:bg-purple-500/30">
      <Background3D />
      
      <main className="relative z-10 container mx-auto px-4 min-h-screen flex flex-col pt-12">
        <header className="flex items-center gap-3 mb-12">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg shadow-purple-500/20">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-tight">ABTalks AI Creator</h1>
        </header>

        {!agentId ? (
          <div className="flex-1 flex items-center justify-center pb-32">
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, ease: "easeOut" }}
              className="glass-panel p-8 rounded-3xl w-full max-w-md relative overflow-hidden"
            >
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-purple-500" />
              <div className="mb-8">
                <h2 className="text-3xl font-bold mb-2">Initialize Persona</h2>
                <p className="text-gray-400 text-sm">Deploy an autonomous technology thinker.</p>
              </div>

              <form onSubmit={handleInit} className="space-y-5">
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Agent Name</label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
                    placeholder="e.g. Ada"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Domain Expertise</label>
                  <input
                    type="text"
                    value={domain}
                    onChange={(e) => setDomain(e.target.value)}
                    className="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
                    placeholder="e.g. AI Security"
                    required
                  />
                </div>
                <button
                  type="submit"
                  disabled={initializing}
                  className="w-full mt-4 bg-white text-black hover:bg-gray-100 font-bold rounded-xl px-4 py-3.5 transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {initializing ? 'Deploying...' : (
                    <>Deploy Agent <Sparkles className="w-4 h-4" /></>
                  )}
                </button>
              </form>
            </motion.div>
          </div>
        ) : (
          <AgentFeed agentId={agentId} />
        )}
      </main>
    </div>
  );
}

export default App;
