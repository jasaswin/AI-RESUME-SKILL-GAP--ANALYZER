
import { useState } from "react";
import { chatWithBot } from "../services/api";

const Chatbot = ({ analysis }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input) return;

    const userMessage = { type: "user", text: input };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await chatWithBot({
        question: input,
        analysis: analysis,
      });

      const botMessage = { type: "bot", text: res.data.answer };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
    }

    setInput("");
  };

  return (
    <div style={{ marginTop: "30px" }}>
      <h3>Ask AI Career Assistant 🤖</h3>

      <div style={{
        height: "200px",
        overflowY: "auto",
        background: "#111",
        padding: "10px",
        borderRadius: "10px"
      }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            textAlign: msg.type === "user" ? "right" : "left",
            margin: "5px 0"
          }}>
            <span style={{
              background: msg.type === "user" ? "#8b5cf6" : "#333",
              padding: "8px",
              borderRadius: "10px",
              display: "inline-block"
            }}>
              {msg.text}
            </span>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", marginTop: "10px" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;