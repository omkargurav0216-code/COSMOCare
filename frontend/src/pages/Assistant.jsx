import { useState, useRef, useEffect } from "react";
import {
  Bot,
  User,
  Send,
  Sparkles,
  Trash2,
  Info,
  ChevronDown,
} from "lucide-react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { initialMessages, suggestedQuestions } from "../data/mockChat";

import { getAstronauts } from "../services/astronautService";
import { sendChatMessage } from "../services/chatService";

function AssistantMarkdown({ content }) {
  // Convert HTML line breaks returned by the LLM into readable separators.
  const formattedContent = String(content || "").replace(/<br\s*\/?>/gi, " · ");

  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        h1: ({ children }) => (
          <h1 className="mb-3 mt-4 text-lg font-bold text-white">{children}</h1>
        ),
        h2: ({ children }) => (
          <h2 className="mb-2 mt-4 text-base font-semibold text-white">
            {children}
          </h2>
        ),
        h3: ({ children }) => (
          <h3 className="mb-2 mt-3 text-sm font-semibold text-cyan-300">
            {children}
          </h3>
        ),
        p: ({ children }) => (
          <p className="mb-3 leading-7 last:mb-0">{children}</p>
        ),
        strong: ({ children }) => (
          <strong className="font-semibold text-white">{children}</strong>
        ),
        ul: ({ children }) => (
          <ul className="mb-3 ml-5 list-disc space-y-1">{children}</ul>
        ),
        ol: ({ children }) => (
          <ol className="mb-3 ml-5 list-decimal space-y-1">{children}</ol>
        ),
        li: ({ children }) => <li className="pl-1">{children}</li>,
        blockquote: ({ children }) => (
          <blockquote className="my-3 border-l-2 border-cyan-500 pl-4 text-slate-400">
            {children}
          </blockquote>
        ),
        hr: () => <hr className="my-4 border-slate-700" />,
        table: ({ children }) => (
          <div className="my-4 max-w-full overflow-x-auto rounded-lg border border-slate-700">
            <table className="w-full border-collapse text-left text-xs">
              {children}
            </table>
          </div>
        ),
        thead: ({ children }) => (
          <thead className="bg-slate-800 text-cyan-300">{children}</thead>
        ),
        th: ({ children }) => (
          <th className="border border-slate-700 px-3 py-2 font-semibold">
            {children}
          </th>
        ),
        td: ({ children }) => (
          <td className="border border-slate-700 px-3 py-2 align-top">
            {children}
          </td>
        ),
        code: ({ children }) => (
          <code className="rounded bg-slate-800 px-1.5 py-0.5 text-cyan-300">
            {children}
          </code>
        ),
      }}
    >
      {formattedContent}
    </ReactMarkdown>
  );
}

function Assistant() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [astronauts, setAstronauts] = useState([]);
  const [selectedAstronaut, setSelectedAstronaut] = useState("");

  const [conversationId, setConversationId] = useState(null);
  const [astronautsLoading, setAstronautsLoading] = useState(true);
  const [apiError, setApiError] = useState("");

  const messagesEndRef = useRef(null);

  // Fetch astronauts from the backend.
  useEffect(() => {
    let cancelled = false;

    const fetchAstronauts = async () => {
      try {
        setAstronautsLoading(true);
        const data = await getAstronauts();

        if (!cancelled) {
          setAstronauts(data);
        }
      } catch (error) {
        console.error("Failed to fetch astronauts:", error);

        if (!cancelled) {
          setApiError(
            "Could not load astronauts. Check whether the COSMOCare backend is running.",
          );
        }
      } finally {
        if (!cancelled) {
          setAstronautsLoading(false);
        }
      }
    };

    fetchAstronauts();

    return () => {
      cancelled = true;
    };
  }, []);

  // Automatically scroll to the latest message.
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const resetConversation = () => {
    setConversationId(null);
    setMessages(initialMessages);
    setInput("");
    setApiError("");
  };

  const handleAstronautChange = (e) => {
    setSelectedAstronaut(e.target.value);
    resetConversation();
  };

  const handleSend = async (e) => {
    e.preventDefault();

    const question = input.trim();

    if (!question || loading) return;

    const userMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: question,
      time: "Now",
    };

    setMessages((previous) => [...previous, userMessage]);
    setInput("");
    setLoading(true);
    setApiError("");

    try {
      const response = await sendChatMessage({
        astronautId: selectedAstronaut || null,
        conversationId,
        message: question,
      });

      setConversationId(response.conversation_id);

      const assistantMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: response.message,
        time: "Now",
      };

      setMessages((previous) => [...previous, assistantMessage]);
    } catch (error) {
      console.error("Chat request failed:", error);

      const errorMessage =
        error.response?.data?.detail ||
        "Unable to connect to COSMOCare AI. Please check the backend and try again.";

      setApiError(errorMessage);

      // Keep the user's message visible, but do not invent a response.
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    if (loading) return;
    resetConversation();
  };

  return (
    <div className="space-y-6">
      {/* Heading */}
      <div>
        <p className="text-sm text-cyan-400">INTELLIGENT MISSION SUPPORT</p>

        <h1 className="mt-1 text-3xl font-bold text-white">AI Assistant</h1>

        <p className="mt-2 text-sm text-slate-400">
          Ask questions about astronaut health monitoring and mission data.
        </p>
      </div>

      {/* Integration information */}
      <div className="flex gap-3 rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-4">
        <Info className="mt-0.5 shrink-0 text-cyan-400" size={19} />

        <div>
          <p className="text-sm font-medium text-cyan-300">
            COSMOCare AI integration
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-400">
            Responses are requested through the COSMOCare backend.
            Astronaut-specific health context is included when an astronaut is
            selected.
          </p>
        </div>
      </div>

      {/* Chat container */}
      <div className="flex h-[650px] flex-col overflow-hidden rounded-xl border border-slate-800 bg-[#0b1425]">
        {/* Chat header */}
        <div className="flex flex-col gap-4 border-b border-slate-800 p-4 sm:p-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-cyan-400/10 p-3">
                <Bot size={22} className="text-cyan-400" />
              </div>

              <div>
                <h2 className="font-semibold text-white">
                  COSMOCare Assistant
                </h2>

                <div className="mt-1 flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-cyan-400" />
                  <span className="text-xs text-slate-500">
                    Backend connected interface
                  </span>
                </div>
              </div>
            </div>

            <button
              type="button"
              onClick={clearChat}
              disabled={loading}
              aria-label="Clear chat history"
              className="flex items-center gap-2 rounded-lg border border-slate-700 px-3 py-2 text-xs text-slate-400 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
            >
              <Trash2 size={15} />
              <span className="hidden sm:inline">Clear chat</span>
            </button>
          </div>

          {/* Astronaut selector */}
          <div>
            <label
              htmlFor="chat-astronaut"
              className="mb-2 block text-xs font-medium text-slate-400"
            >
              HEALTH CONTEXT
            </label>

            <div className="relative">
              <select
                id="chat-astronaut"
                value={selectedAstronaut}
                onChange={handleAstronautChange}
                disabled={loading || astronautsLoading}
                className="w-full appearance-none rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 pr-10 text-sm text-slate-200 outline-none focus:border-cyan-400 disabled:opacity-50"
              >
                <option value="">General mission questions</option>

                {astronauts.map((astronaut) => (
                  <option key={astronaut.id} value={astronaut.id}>
                    {astronaut.name} — {astronaut.mission}
                  </option>
                ))}
              </select>

              <ChevronDown
                size={16}
                className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-500"
              />
            </div>

            <p className="mt-2 text-[11px] text-slate-500">
              {astronautsLoading
                ? "Loading astronauts..."
                : selectedAstronaut
                  ? "Selected astronaut's available health context will be supplied."
                  : "No astronaut-specific health context will be supplied."}
            </p>
          </div>
        </div>

        {/* Messages */}
        <div
          role="log"
          aria-live="polite"
          aria-label="Chat conversation"
          className="flex-1 space-y-5 overflow-y-auto p-4 sm:p-6"
        >
          {messages.map((message) => {
            const isUser = message.role === "user";

            return (
              <div
                key={message.id}
                className={`flex gap-3 ${isUser ? "flex-row-reverse" : ""}`}
              >
                <div
                  className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${
                    isUser ? "bg-purple-400/10" : "bg-cyan-400/10"
                  }`}
                >
                  {isUser ? (
                    <User size={18} className="text-purple-400" />
                  ) : (
                    <Bot size={18} className="text-cyan-400" />
                  )}
                </div>

                <div
                  className={`max-w-[85%] sm:max-w-[75%] ${
                    isUser ? "text-right" : ""
                  }`}
                >
                  <div
                    className={`mb-1 text-xs ${
                      isUser ? "text-purple-400" : "text-cyan-400"
                    }`}
                  >
                    {isUser ? "You" : "COSMOCare Assistant"}
                  </div>

                  <div
                    className={`rounded-xl p-4 text-left text-sm leading-6 ${
                      isUser
                        ? "bg-purple-500/10 text-slate-200"
                        : "border border-slate-800 bg-slate-900/70 text-slate-300"
                    }`}
                  >
                    {isUser ? (
                      message.content
                    ) : (
                      <AssistantMarkdown content={message.content} />
                    )}
                  </div>

                  <p className="mt-1 text-[10px] text-slate-600">
                    {message.time}
                  </p>
                </div>
              </div>
            );
          })}

          {apiError && (
            <div
              role="alert"
              className="rounded-lg border border-red-500/20 bg-red-500/5 p-3 text-xs leading-5 text-red-300"
            >
              {apiError}
            </div>
          )}

          {loading && (
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-cyan-400/10">
                <Bot size={18} className="text-cyan-400" />
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900/70 px-4 py-3 text-sm text-slate-400">
                COSMOCare is preparing a response...
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggested questions */}
        {messages.length === 1 && (
          <div className="border-t border-slate-800 px-4 py-4">
            <div className="mb-3 flex items-center gap-2 text-xs text-slate-500">
              <Sparkles size={14} className="text-cyan-400" />
              Suggested questions
            </div>

            <div className="flex flex-wrap gap-2">
              {suggestedQuestions.map((question) => (
                <button
                  type="button"
                  key={question}
                  onClick={() => setInput(question)}
                  disabled={loading}
                  className="rounded-full border border-slate-700 px-3 py-2 text-xs text-slate-400 transition hover:border-cyan-400/50 hover:text-cyan-400 disabled:opacity-40"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <form
          onSubmit={handleSend}
          className="flex items-center gap-3 border-t border-slate-800 p-4"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask COSMOCare about astronaut health..."
            aria-label="Ask COSMOCare a question"
            disabled={loading}
            className="min-w-0 flex-1 rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-cyan-400 disabled:opacity-50"
          />

          <button
            type="submit"
            aria-label="Send message"
            disabled={!input.trim() || loading}
            className="flex items-center justify-center rounded-lg bg-cyan-500 p-3 text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <Send size={18} />
          </button>
        </form>
      </div>

      <p className="text-xs text-slate-500">
        COSMOCare is a research prototype and decision-support tool. Its
        responses are not medical diagnoses or a substitute for qualified
        mission health personnel.
      </p>
    </div>
  );
}

export default Assistant;

// import { useState, useRef, useEffect } from "react";
// import {
//   Bot,
//   User,
//   Send,
//   Sparkles,
//   Trash2,
//   Info,
// } from "lucide-react";

// import {
//   initialMessages,
//   suggestedQuestions,
// } from "../data/mockChat";

// function Assistant() {
//   const [messages, setMessages] = useState(initialMessages);
//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);

//   const messagesEndRef = useRef(null);
//   const responseTimerRef = useRef(null);

//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({
//       behavior: "smooth",
//     });
//   }, [messages, loading]);

//   // Temporary local demonstration response.
//   // Replace with chatService API after the backend contract is confirmed.
//   const generateDemoResponse = (question) => {
//     const text = question.toLowerCase();

//     if (text.includes("heart") || text.includes("cardio")) {
//       return "Heart rate is one of the indicators monitored by ASTRA. The current illustrative dashboard includes heart-rate readings and trend visualizations. Actual interpretation should use validated mission-specific thresholds and the backend risk assessment.";
//     }

//     if (text.includes("sleep") || text.includes("fatigue")) {
//       return "Sleep duration and fatigue are important monitoring indicators. ASTRA's prototype displays sleep telemetry and fatigue-related risk information. Actual fatigue assessment requires validated data and the integrated ML model.";
//     }

//     if (text.includes("radiation")) {
//       return "ASTRA includes radiation exposure as a monitored health-related parameter. The prototype can display radiation measurements and trends. Actual exposure assessment requires mission-specific limits and validated radiation data.";
//     }

//     if (text.includes("risk") || text.includes("score")) {
//       return "ASTRA's Risk Assessment module presents an illustrative risk score and contributing indicators. These prototype values are not clinical predictions. The final risk assessment will use the integrated backend and ML pipeline.";
//     }

//     if (text.includes("alert")) {
//       return "The Alerts module displays sample health and monitoring alerts. You can filter alerts by severity and status, acknowledge them or mark them resolved. Actual alerts will be populated through backend integration.";
//     }

//     return "I'm currently running in frontend demonstration mode. I can show example information about heart rate, sleep, fatigue, radiation, risk assessment and alerts. The actual AI assistant will be connected through the ASTRA backend API.";
//   };

//   // Clean up any pending response if the page unmounts.
//   useEffect(() => {
//     return () => {
//       if (responseTimerRef.current) {
//         clearTimeout(responseTimerRef.current);
//       }
//     };
//   }, []);

//   const handleSend = (e) => {
//     e.preventDefault();

//     const question = input.trim();

//     if (!question || loading) return;

//     const messageId = Date.now();

//     const userMessage = {
//       id: messageId,
//       role: "user",
//       content: question,
//       time: "Now",
//     };

//     setMessages((previous) => [...previous, userMessage]);
//     setInput("");
//     setLoading(true);

//     // Simulated response delay for frontend demonstration.
//     responseTimerRef.current = setTimeout(() => {
//       const assistantMessage = {
//         id: messageId + 1,
//         role: "assistant",
//         content: generateDemoResponse(question),
//         time: "Now",
//       };

//       setMessages((previous) => [
//         ...previous,
//         assistantMessage,
//       ]);

//       setLoading(false);
//       responseTimerRef.current = null;
//     }, 700);
//   };

//   const clearChat = () => {
//     if (loading) return;

//     setMessages(initialMessages);
//     setInput("");
//   };

//   return (
//     <div className="space-y-6">
//       {/* Heading */}
//       <div>
//         <p className="text-sm text-cyan-400">
//           INTELLIGENT MISSION SUPPORT
//         </p>

//         <h1 className="mt-1 text-3xl font-bold text-white">
//           AI Assistant
//         </h1>

//         <p className="mt-2 text-sm text-slate-400">
//           Ask questions about astronaut health monitoring and mission data.
//         </p>
//       </div>

//       {/* Demo notice */}
//       <div className="flex gap-3 rounded-xl border border-amber-500/20 bg-amber-500/5 p-4">
//         <Info
//           className="mt-0.5 shrink-0 text-amber-400"
//           size={19}
//         />

//         <div>
//           <p className="text-sm font-medium text-amber-300">
//             Demonstration mode
//           </p>

//           <p className="mt-1 text-xs leading-5 text-slate-400">
//             Responses are generated locally using sample rules.
//             The actual AI assistant will be connected through the backend API.
//           </p>
//         </div>
//       </div>

//       {/* Chat container */}
//       <div className="flex h-[650px] flex-col overflow-hidden rounded-xl border border-slate-800 bg-[#0b1425]">

//         {/* Chat header */}
//         <div className="flex items-center justify-between border-b border-slate-800 p-4 sm:p-5">
//           <div className="flex items-center gap-3">
//             <div className="rounded-xl bg-cyan-400/10 p-3">
//               <Bot size={22} className="text-cyan-400" />
//             </div>

//             <div>
//               <h2 className="font-semibold text-white">
//                 ASTRA Assistant
//               </h2>

//               <div className="mt-1 flex items-center gap-2">
//                 <span className="h-2 w-2 rounded-full bg-amber-400" />

//                 <span className="text-xs text-slate-500">
//                   Demo mode · Not connected to backend
//                 </span>
//               </div>
//             </div>
//           </div>

//           <button
//             type="button"
//             onClick={clearChat}
//             disabled={loading}
//             aria-label="Clear chat history"
//             className="flex items-center gap-2 rounded-lg border border-slate-700 px-3 py-2 text-xs text-slate-400 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
//           >
//             <Trash2 size={15} />
//             <span className="hidden sm:inline">
//               Clear chat
//             </span>
//           </button>
//         </div>

//         {/* Messages */}
//         <div
//           role="log"
//           aria-live="polite"
//           aria-label="Chat conversation"
//           className="flex-1 space-y-5 overflow-y-auto p-4 sm:p-6"
//         >
//           {messages.map((message) => {
//             const isUser = message.role === "user";

//             return (
//               <div
//                 key={message.id}
//                 className={`flex gap-3 ${
//                   isUser ? "flex-row-reverse" : ""
//                 }`}
//               >
//                 <div
//                   className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${
//                     isUser
//                       ? "bg-purple-400/10"
//                       : "bg-cyan-400/10"
//                   }`}
//                 >
//                   {isUser ? (
//                     <User size={18} className="text-purple-400" />
//                   ) : (
//                     <Bot size={18} className="text-cyan-400" />
//                   )}
//                 </div>

//                 <div
//                   className={`max-w-[85%] sm:max-w-[75%] ${
//                     isUser ? "text-right" : ""
//                   }`}
//                 >
//                   <div
//                     className={`mb-1 text-xs ${
//                       isUser
//                         ? "text-purple-400"
//                         : "text-cyan-400"
//                     }`}
//                   >
//                     {isUser ? "You" : "ASTRA Assistant"}
//                   </div>

//                   <div
//                     className={`rounded-xl p-4 text-left text-sm leading-6 ${
//                       isUser
//                         ? "bg-purple-500/10 text-slate-200"
//                         : "border border-slate-800 bg-slate-900/70 text-slate-300"
//                     }`}
//                   >
//                     {message.content}
//                   </div>

//                   <p className="mt-1 text-[10px] text-slate-600">
//                     {message.time}
//                   </p>
//                 </div>
//               </div>
//             );
//           })}

//           {loading && (
//             <div className="flex items-center gap-3">
//               <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-cyan-400/10">
//                 <Bot size={18} className="text-cyan-400" />
//               </div>

//               <div className="rounded-xl border border-slate-800 bg-slate-900/70 px-4 py-3 text-sm text-slate-400">
//                 ASTRA is preparing a demo response...
//               </div>
//             </div>
//           )}

//           <div ref={messagesEndRef} />
//         </div>

//         {/* Suggested questions */}
//         {messages.length === 1 && (
//           <div className="border-t border-slate-800 px-4 py-4">
//             <div className="mb-3 flex items-center gap-2 text-xs text-slate-500">
//               <Sparkles size={14} className="text-cyan-400" />
//               Suggested questions
//             </div>

//             <div className="flex flex-wrap gap-2">
//               {suggestedQuestions.map((question) => (
//                 <button
//                   type="button"
//                   key={question}
//                   onClick={() => setInput(question)}
//                   disabled={loading}
//                   className="rounded-full border border-slate-700 px-3 py-2 text-xs text-slate-400 transition hover:border-cyan-400/50 hover:text-cyan-400 disabled:opacity-40"
//                 >
//                   {question}
//                 </button>
//               ))}
//             </div>
//           </div>
//         )}

//         {/* Input */}
//         <form
//           onSubmit={handleSend}
//           className="flex items-center gap-3 border-t border-slate-800 p-4"
//         >
//           <input
//             type="text"
//             value={input}
//             onChange={(e) => setInput(e.target.value)}
//             placeholder="Ask ASTRA about astronaut health..."
//             aria-label="Ask ASTRA a question"
//             disabled={loading}
//             className="min-w-0 flex-1 rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-cyan-400 disabled:opacity-50"
//           />

//           <button
//             type="submit"
//             aria-label="Send message"
//             disabled={!input.trim() || loading}
//             className="flex items-center justify-center rounded-lg bg-cyan-500 p-3 text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-40"
//           >
//             <Send size={18} />
//           </button>
//         </form>
//       </div>

//       <p className="text-xs text-slate-500">
//         Prototype notice: Do not use demonstration responses for medical
//         decisions. Actual AI responses and supporting data will come
//         from the integrated backend.
//       </p>
//     </div>
//   );
// }

// export default Assistant;
