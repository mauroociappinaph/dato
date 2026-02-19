import os
import sys

def generate_html(output_path):
    html_content = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dude AI - Web Command Center</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
        
        body {
            background: radial-gradient(circle at top left, #0f172a, #020617);
            font-family: 'Inter', sans-serif;
            color: #e2e8f0;
            overflow: hidden;
        }

        .glass {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
        }

        .neon-border-cyan { border-color: #06b6d4; box-shadow: 0 0 15px rgba(6, 182, 212, 0.3); }
        .neon-border-pink { border-color: #ec4899; box-shadow: 0 0 15px rgba(236, 72, 153, 0.3); }
        
        .title-font { font-family: 'Orbitron', sans-serif; }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
        
        .log-line { border-left: 2px solid #06b6d4; padding-left: 8px; margin-bottom: 4px; font-family: monospace; font-size: 0.75rem; }
    </style>
</head>
<body class="h-screen w-screen flex">

    <!-- Sidebar: Specialists -->
    <aside class="w-72 h-full p-6 flex flex-col gap-6 glass border-r border-white/10 m-2">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-cyan-500 rounded-lg flex items-center justify-center neon-border-cyan">
                <i class="fas fa-brain text-white"></i>
            </div>
            <h1 class="title-font font-bold text-xl tracking-wider text-cyan-400">DUDE AI</h1>
        </div>

        <nav class="flex-1 overflow-y-auto">
            <p class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Departamentos</p>
            <div class="space-y-2">
                <div class="flex items-center gap-3 p-3 rounded-lg bg-white/5 border border-white/5 hover:border-cyan-500/50 transition-all cursor-pointer group">
                    <i class="fas fa-code text-cyan-400 group-hover:scale-110 transition-transform"></i>
                    <span>Frontend Dev</span>
                </div>
                <div class="flex items-center gap-3 p-3 rounded-lg bg-white/5 border border-white/5 hover:border-pink-500/50 transition-all cursor-pointer group">
                    <i class="fas fa-server text-pink-400 group-hover:scale-110 transition-transform"></i>
                    <span>Backend Arch</span>
                </div>
                <div class="flex items-center gap-3 p-3 rounded-lg bg-white/5 border border-white/5 hover:border-purple-500/50 transition-all cursor-pointer group">
                    <i class="fas fa-shield-alt text-purple-400 group-hover:scale-110 transition-transform"></i>
                    <span>Security Audit</span>
                </div>
            </div>
        </nav>

        <div class="p-4 glass bg-white/5 text-xs text-slate-400">
            <p><i class="fas fa-microchip mr-2"></i> Pipeline v7.0 Active</p>
            <p id="redis-status"><i class="fas fa-memory mr-2"></i> Sincronizando...</p>
        </div>
    </aside>

    <!-- Main Command Center -->
    <main class="flex-1 h-full p-6 flex flex-col gap-6 m-2 overflow-hidden">
        
        <!-- Header -->
        <header class="h-20 glass flex items-center justify-between px-8">
            <div>
                <h2 class="title-font text-lg text-slate-200 uppercase tracking-tighter">Web Command Center</h2>
                <p id="system-status" class="text-xs text-cyan-400 animate-pulse">● System Live: Real-time monitoring active</p>
            </div>
            <div class="flex items-center gap-4">
                <div class="flex flex-col items-end">
                    <span class="text-xs font-bold text-cyan-400">MAURO (OWNER)</span>
                    <span class="text-[10px] text-slate-500 italic">Session Industrial v7.0</span>
                </div>
                <div class="w-10 h-10 rounded-full bg-slate-800 border border-cyan-500/50 flex items-center justify-center overflow-hidden">
                    <i class="fas fa-user-tie text-cyan-400"></i>
                </div>
            </div>
        </header>

        <!-- Dynamic Content Grid -->
        <div class="flex-1 grid grid-cols-2 gap-6 overflow-hidden">
            <!-- Event Stream -->
            <div class="glass p-6 flex flex-col gap-4 overflow-hidden border-cyan-500/20">
                <div class="flex items-center justify-between">
                    <h3 class="title-font text-xs font-bold text-slate-400 uppercase tracking-widest">Live Event Stream</h3>
                    <span class="text-[10px] bg-cyan-500/20 text-cyan-400 px-2 py-1 rounded">WebSocket Active</span>
                </div>
                <div id="event-stream" class="flex-1 overflow-y-auto space-y-2 pr-2">
                    <div class="log-line text-slate-400">Initializing connection to backend...</div>
                </div>
            </div>

            <!-- Health & Memory -->
            <div class="flex flex-col gap-6 overflow-hidden">
                <div class="glass p-6 h-1/2 border-pink-500/20">
                    <h3 class="title-font text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Infrastructure Health</h3>
                    <div id="health-stats" class="space-y-4">
                        <div class="flex justify-between text-xs">
                            <span class="text-slate-500">API Gateway</span>
                            <span class="text-matrix_green">Operational</span>
                        </div>
                        <div class="w-full bg-white/5 h-1 rounded-full overflow-hidden">
                            <div class="bg-cyan-500 h-full w-[98%]"></div>
                        </div>
                    </div>
                </div>
                <div class="glass p-6 h-1/2 border-purple-500/20">
                    <h3 class="title-font text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Recent Autonomous Fixes</h3>
                    <div id="recent-fixes" class="text-xs text-slate-500 space-y-2">
                        <p class="text-cyan-400">● AGENT_SALES: Tracing timeout increased to 5s</p>
                        <p>● Waiting for next failure...</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Input Area -->
        <footer class="h-24 glass p-4 flex items-center gap-4 border-t border-white/5">
            <div class="flex-1 relative">
                <input type="text" placeholder="Escribí tu comando aquí, Mauro..." 
                       class="w-full h-12 bg-white/5 border border-white/10 rounded-xl px-6 focus:outline-none focus:border-cyan-500 transition-all text-sm">
                <div class="absolute right-4 top-3 text-slate-500 flex gap-3">
                    <i class="fas fa-microphone cursor-pointer hover:text-cyan-400"></i>
                    <i class="fas fa-paperclip cursor-pointer hover:text-cyan-400"></i>
                </div>
            </div>
            <button class="h-12 w-12 bg-cyan-500 hover:bg-cyan-400 transition-colors rounded-xl flex items-center justify-center neon-border-cyan text-white">
                <i class="fas fa-paper-plane"></i>
            </button>
        </footer>

    </main>

    <script>
        const eventStream = document.getElementById('event-stream');
        const redisStatus = document.getElementById('redis-status');
        
        function connectWS() {
            const ws = new WebSocket('ws://localhost:8000/ws/events');
            
            ws.onopen = () => {
                eventStream.innerHTML += '<div class="log-line text-matrix_green">Connected to The Dude Core.</div>';
                redisStatus.innerHTML = '<i class="fas fa-memory mr-2 text-cyan-400"></i> Redis Online';
            };
            
            ws.onmessage = (event) => {
                const payload = JSON.parse(event.data);
                if (payload.type === 'LOG_UPDATE') {
                    payload.data.forEach(log => {
                        const div = document.createElement('div');
                        div.className = 'log-line text-slate-300';
                        div.innerHTML = `<span class="text-cyan-500 text-[10px]">[${log.file}]</span> ${log.preview.split('\n').pop()}`;
                        eventStream.prepend(div);
                    });
                }
            };
            
            ws.onclose = () => {
                eventStream.innerHTML += '<div class="log-line text-pink-500">Connection lost. Retrying...</div>';
                setTimeout(connectWS, 3000);
            };
        }
        
        connectWS();
    </script>
</body>
</html>"""
    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"UI generated at: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = os.path.join(os.path.expanduser("~/.gemini/workspace/dude-command-center.html"))
    generate_html(target)
