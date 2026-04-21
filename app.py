<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VĂN HIẾN AI 3.5</title>
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @keyframes bounce-slow { 0%, 100% { transform: translateY(-5%); } 50% { transform: translateY(0); } }
        .animate-bounce-slow { animation: bounce-slow 4s infinite ease-in-out; }
        .custom-scrollbar::-webkit-scrollbar { width: 5px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: #fff1f2; border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #fecdd3; border-radius: 10px; }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;

        const App = () => {
            const [activeTab, setActiveTab] = useState('outline');
            const [prompt, setPrompt] = useState('');
            const [studentEssay, setStudentEssay] = useState('');
            const [essayType, setEssayType] = useState('nghi-luan-van-hoc');
            const [loading, setLoading] = useState(false);
            const [result, setResult] = useState(null);
            const [error, setError] = useState(null);

            // BẢO MẬT: Nhập key qua prompt nếu không tìm thấy trong bộ nhớ
            // Cách này giúp bạn không bị lộ Key khi đẩy code công khai lên GitHub
            const getApiKey = () => {
                let key = localStorage.getItem('GEMINI_KEY');
                if (!key) {
                    key = window.prompt("Vui lòng nhập Gemini API Key của bạn (Key sẽ được lưu trong trình duyệt của bạn, không lộ ra ngoài):");
                    if (key) localStorage.setItem('GEMINI_KEY', key);
                }
                return key;
            };

            const fetchGeminiResponse = async (userQuery, mode) => {
                const apiKey = getApiKey();
                if (!apiKey) throw new Error("Chưa có API Key");

                let systemPrompt = "";
                switch(mode) {
                    case 'outline': systemPrompt = "Bạn là giáo viên dạy Ngữ văn THPT. Lập dàn ý chi tiết..."; break;
                    case 'evaluate': systemPrompt = "Bạn là chuyên gia chấm thi Ngữ văn..."; break;
                    case 'evidence': systemPrompt = "Hãy cung cấp 3-5 dẫn chứng thời sự mới nhất..."; break;
                    default: systemPrompt = "Hỗ trợ học tập Ngữ văn.";
                }

                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        contents: [{ parts: [{ text: userQuery }] }],
                        systemInstruction: { parts: [{ text: systemPrompt }] }
                    })
                });

                const data = await response.json();
                if (data.error) throw new Error(data.error.message);
                return data.candidates[0].content.parts[0].text;
            };

            const handleAction = async () => {
                setLoading(true);
                setError(null);
                try {
                    const text = await fetchGeminiResponse(prompt, activeTab);
                    setResult(text);
                } catch (err) {
                    setError(err.message);
                    if (err.message.includes("API key")) localStorage.removeItem('GEMINI_KEY');
                } finally {
                    setLoading(false);
                }
            };

            return (
                <div className="min-h-screen bg-[#fff1f2] p-4 font-sans">
                    <div className="max-w-4xl mx-auto">
                        <header className="text-center mb-8">
                            <h1 className="text-3xl font-black text-rose-600">VĂN HIẾN AI <span className="text-rose-300">3.5</span></h1>
                            <button onClick={() => {localStorage.removeItem('GEMINI_KEY'); location.reload();}} className="text-[10px] text-rose-400 underline">Đổi API Key</button>
                        </header>

                        <div className="bg-white rounded-[30px] p-6 shadow-xl border border-rose-100">
                            <textarea 
                                className="w-full p-4 bg-rose-50 rounded-2xl outline-none mb-4 h-32"
                                placeholder="Nhập đề bài vào đây..."
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)}
                            />
                            
                            <button 
                                onClick={handleAction}
                                disabled={loading}
                                className="w-full py-4 bg-rose-500 text-white rounded-2xl font-bold hover:bg-rose-600 transition-all"
                            >
                                {loading ? "Đang xử lý..." : "Bắt đầu phân tích"}
                            </button>
                        </div>

                        {result && (
                            <div className="mt-8 bg-white p-6 rounded-[30px] shadow-lg animate-in fade-in">
                                <pre className="whitespace-pre-wrap text-slate-700 leading-relaxed font-sans">{result}</pre>
                            </div>
                        )}
                        
                        {error && <p className="text-red-500 text-center mt-4">{error}</p>}
                    </div>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
