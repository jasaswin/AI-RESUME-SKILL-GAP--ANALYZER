

// const GapList = ({ gaps }) => {
//   if (!Array.isArray(gaps)) return null;

//   return (
//     <div>
//       <h3>Missing Skills</h3>
//       <ul>
//         {gaps.map((skill, index) => (
//           <li key={index}>{skill}</li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default GapList;


// const GapList = ({ gaps }) => {
//   if (!Array.isArray(gaps)) return null;

//   return (
//     <div>
//       <h3>Skills</h3>
//       <ul>
//         {gaps.map((skill, index) => (
//           <li key={index}>
//             {typeof skill === "object" ? skill.skill : skill}
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default GapList;


const GapList = ({ gaps, title }) => {
  if (!Array.isArray(gaps)) return null;

  return (
    <div className="section">
      <h3>{title}</h3>

      <div>
        {gaps.map((skill, index) => (
          <span key={index} className="tag">
            {typeof skill === "object" ? skill.skill : skill}
          </span>
        ))}
      </div>
    </div>
  );
};

export default GapList;