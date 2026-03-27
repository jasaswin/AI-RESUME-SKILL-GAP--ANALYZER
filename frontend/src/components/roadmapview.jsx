

// const RoadmapView = ({ roadmap }) => {
//   // ✅ Convert to array safely
//   let roadmapArray = [];

//   if (Array.isArray(roadmap)) {
//     roadmapArray = roadmap;
//   } else if (typeof roadmap === "string") {
//     roadmapArray = roadmap.split(","); // split if string
//   } else if (typeof roadmap === "object" && roadmap !== null) {
//     roadmapArray = Object.values(roadmap);
//   }

//   return (
//     <div>
//       <h3>Learning Roadmap</h3>
//       <ul>
//         {roadmapArray.map((step, index) => (
//           <li key={index}>{step}</li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default RoadmapView;


// const RoadmapView = ({ roadmap }) => {
//   if (!Array.isArray(roadmap)) return null;

//   return (
//     <div>
//       <h3>Learning Roadmap</h3>

//       {roadmap.map((step, index) => (
//         <div key={index} style={{
//           marginBottom: "15px",
//           padding: "10px",
//           background: "#222",
//           borderRadius: "10px"
//         }}>
//           <h4 style={{ color: "#8b5cf6" }}>{step.skill}</h4>

//           <p><b>Duration:</b> {step.estimated_weeks} weeks</p>
//           <p><b>Difficulty:</b> {step.difficulty}</p>
//           <p><b>Why:</b> {step.reason}</p>

//           {/* Optional: show resources */}
//           {step.resources && (
//             <ul>
//               {step.resources.map((res, i) => (
//                 <li key={i}>{res}</li>
//               ))}
//             </ul>
//           )}
//         </div>
//       ))}
//     </div>
//   );
// };

// export default RoadmapView;


// const RoadmapView = ({ roadmap }) => {
//   if (!roadmap || typeof roadmap !== "object") return null;

//   return (
//     <div>
//       <h3>Learning Roadmap</h3>

//       {Object.entries(roadmap).map(([phase, steps], index) => (
//         <div key={index} style={{ marginBottom: "20px" }}>
//           <h4 style={{ color: "#8b5cf6" }}>{phase}</h4>

//           {steps.map((step, i) => (
//             <div key={i} style={{
//               background: "#222",
//               padding: "10px",
//               borderRadius: "10px",
//               marginBottom: "10px"
//             }}>
//               <b>{step.skill}</b>
//               <p>⏱ {step.estimated_weeks} weeks</p>
//               <p>📊 {step.difficulty}</p>
//               <p>{step.reason}</p>
//             </div>
//           ))}
//         </div>
//       ))}
//     </div>
//   );
// };

// export default RoadmapView;


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