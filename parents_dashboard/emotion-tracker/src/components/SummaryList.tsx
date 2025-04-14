import React from 'react';

interface SummaryData {
  date: string;
  description: string;
}

interface SummaryListProps {
  summaries: SummaryData[];
}

const SummaryList: React.FC<SummaryListProps> = ({ summaries }) => {
  return (
    <ul className="summary-list">
      {summaries.map((summary, index) => (
        <li key={index} className="summary-item">
          <div className="summary-date">{summary.date}</div>
          <div className="summary-description">{summary.description}</div>
        </li>
      ))}
    </ul>
  );
};

export default SummaryList; 