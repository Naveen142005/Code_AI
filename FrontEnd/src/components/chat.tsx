import { useState, useRef, useEffect } from "react";
import "./Chat.css";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Message = {
  text: string;
  sender: "user" | "bot";
};

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hi... How can I help you with this repo?", sender: "bot" },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = () => {
    if (!input.trim()) return;

    const userMsg: Message = { text: input, sender: "user" };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    setLoading(true);

    fetch("http://localhost:8000/qa_chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_msg: input }),
    })
      .then((res) => res.json())
      .then((data) => {
        setMessages((prev) => {
          return [
            ...prev,
            {
              text: data,
              sender: "bot",
            },
          ];
        });
      })
      .catch((err) => alert(`Error in the Fetch api. ${err}`))
      .finally(() => setLoading((t) => (t = false)));
  };

  return (
    <div className="page">
      <div className="chatBox">
        <div className="messages">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`message ${msg.sender === "user" ? "user" : "bot"}`}
            >
              {msg.sender === "bot" ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.text}
                </ReactMarkdown>
              ) : (
                <span>{msg.text}</span>
              )}
            </div>
          ))}

          {loading && <div className="message bot">Typing...</div>}

          <div ref={messagesEndRef} />
        </div>

        <div className="inputBox">
          <input
            className="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Type your message..."
          />
          <button className="button" onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
