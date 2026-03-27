

import { useLocation } from "react-router-dom";
import SkillMatchCard from "../components/SkillMatchCard";
import GapList from "../components/gaplist";
import RoadmapView from "../components/roadmapview";
import SkillChart from "../components/SkillChart";
import Chatbot from "../components/Chatbot";

const Result = () => {
  const { state } = useLocation();

  if (!state) return <h2 style={{ textAlign: "center" }}>No Data Found</h2>;

  return (
    <div className="container">
      <div
        className="card"
        style={{
          width: "700px",
          maxWidth: "90%",
          margin: "auto",
        }}
      >
        <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
          Analysis Result
        </h2>

        {/* 🎯 Skill Match */}
        <SkillMatchCard percentage={state.final_match} />

        {/* 🧠 Explanation */}
        <p
          style={{
            textAlign: "center",
            color: "#aaa",
            marginTop: "10px",
          }}
        >
          {state.explanation?.summary}
        </p>

        {/* 📊 Chart */}
        <div style={{ marginTop: "20px" }}>
          <SkillChart
            matched={state.matched_skills}
            missing={state.missing_skills}
          />
        </div>

        {/* ✅ Skills */}
        <div style={{ marginTop: "25px" }}>
          <GapList gaps={state.matched_skills} title="Matched Skills" />
        </div>

        <div style={{ marginTop: "15px" }}>
          <GapList gaps={state.missing_skills} title="Missing Skills" />
        </div>

        {/* 🛣️ Roadmap */}
        <div style={{ marginTop: "25px" }}>
          <RoadmapView roadmap={state.roadmap} />
        </div>

        <Chatbot analysis={state} />
      </div>
    </div>
  );
};

export default Result;


// We are looking for a passionate and skilled Full Stack Software Engineer to join our dynamic team. The ideal candidate will be responsible for developing scalable web applications, collaborating with cross-functional teams, and delivering high-quality software solutions.

// 🔧 Responsibilities:
// Develop and maintain web applications using modern frameworks
// Build responsive user interfaces using React.js
// Design and develop RESTful APIs using Node.js / FastAPI
// Work with databases like MongoDB, MySQL, or PostgreSQL
// Collaborate with designers, product managers, and backend teams
// Write clean, maintainable, and efficient code
// Debug and optimize application performance
// 🧠 Required Skills:
// Strong knowledge of JavaScript (ES6+)
// Experience with React.js
// Backend experience with Node.js or Python (FastAPI)
// Understanding of REST APIs
// Familiarity with MongoDB / MySQL
// Basic knowledge of Git & GitHub
// Problem-solving and debugging skills
// ⭐ Good to Have:
// Experience with Docker
// Knowledge of AWS / Cloud deployment
// Understanding of CI/CD pipelines
// Familiarity with TypeScript
// 🎓 Qualifications:
// B.Tech / B.E in Computer Science or related field
// 0–2 years experience (Freshers can apply)
// 🚀 What You’ll Gain:
// Hands-on experience with real-world projects
// Exposure to scalable system design
// Opportunity to work with modern technologies