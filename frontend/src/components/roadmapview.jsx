


const RoadmapView = ({ roadmap }) => {
  if (!roadmap || typeof roadmap !== "object") return null;

  return (
    <div className="section">
      <h3>Learning Roadmap</h3>

      {Object.entries(roadmap).map(([phase, steps], index) => (
        <div key={index}>
          <h4 style={{ color: "#8b5cf6" }}>{phase}</h4>

          {steps.map((step, i) => (
            <div key={i} className="roadmap-card">
              <b>{step.skill}</b>
              <p>⏱ {step.estimated_weeks} weeks</p>
              <p>📊 {step.difficulty}</p>
              <p>{step.reason}</p>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default RoadmapView;
