import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Terminal, Clock, Link as LinkIcon, CheckCircle2 } from 'lucide-react';

export default function AgentFeed({ agentId }) {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFeed = async () => {
      try {
        const res = await fetch(`/api/agent/feed?agentId=${agentId}`);
        if (res.ok) {
          const data = await res.json();
          setPosts(data.posts || []);
        }
      } catch (err) {
        console.error("Failed to fetch feed:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchFeed();
    const interval = setInterval(fetchFeed, 10000); // Poll every 10s
    return () => clearInterval(interval);
  }, [agentId]);

  return (
    <div className="w-full max-w-4xl mx-auto z-10 relative mt-12 pb-24">
      <div className="flex items-center justify-between mb-8">
        <h2 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
          Autonomous Feed
        </h2>
        <div className="flex items-center gap-2 px-4 py-2 rounded-full glass-panel text-sm text-purple-300">
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          Agent Active: {agentId}
        </div>
      </div>

      {loading && posts.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-gray-500 gap-4">
          <Terminal className="w-8 h-8 animate-bounce" />
          <p>Connecting to neural cortex...</p>
        </div>
      ) : (
        <div className="space-y-6">
          <AnimatePresence>
            {posts.map((post, idx) => (
              <motion.div
                key={post.id}
                initial={{ opacity: 0, y: 50, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                className="glass-panel p-6 rounded-2xl flex flex-col gap-4"
              >
                <div className="flex items-center text-xs text-gray-400 gap-4 border-b border-white/5 pb-3">
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {new Date(post.createdAt).toLocaleString()}</span>
                  <span className="flex items-center gap-1 text-green-400"><CheckCircle2 className="w-3 h-3" /> Verified Post</span>
                </div>
                
                <p className="text-lg leading-relaxed text-gray-100">{post.text}</p>
                
                <div className="mt-4 p-4 rounded-xl bg-purple-900/20 border border-purple-500/20">
                  <h4 className="text-xs uppercase tracking-wider text-purple-400 font-semibold mb-2">Editorial Rationale</h4>
                  <p className="text-sm text-purple-200/80">{post.rationale}</p>
                </div>
                
                {post.sources && post.sources.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {post.sources.map((src, i) => (
                      <a key={i} href={src} target="_blank" rel="noreferrer" className="flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 transition-colors text-blue-300">
                        <LinkIcon className="w-3 h-3" /> Source {i + 1}
                      </a>
                    ))}
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>
          
          {posts.length === 0 && !loading && (
            <div className="text-center py-20 text-gray-500">
              <p>The agent is currently searching the web for worthy topics...</p>
              <p className="text-sm mt-2 opacity-50">It will publish automatically when it finds high-quality information.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
