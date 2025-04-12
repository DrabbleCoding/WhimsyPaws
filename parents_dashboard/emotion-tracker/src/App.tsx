import React, { useState, useEffect } from 'react';
import './styles/global.css';
import EmotionChart from './components/EmotionChart';
import SummaryList from './components/SummaryList';
import emotionsData from './data/emotions.json';

interface EmotionData {
  date: string;
  emotions: {
    [key: string]: number;
  };
}

interface SummaryData {
  date: string;
  description: string;
}

function App() {
  const [emotionData, setEmotionData] = useState<EmotionData[]>([]);
  const [summaryData, setSummaryData] = useState<SummaryData[]>([]);

  useEffect(() => {
    console.log('Loading emotion data:', emotionsData);
    
    // Load emotion data
    setEmotionData(emotionsData as EmotionData[]);

    // Generate summary data from emotion data
    const summaries: SummaryData[] = emotionsData.map((item: EmotionData) => ({
      date: item.date,
      description: `Emotional state recorded: ${Object.entries(item.emotions)
        .map(([emotion, value]) => `${emotion} (${value}/10)`)
        .join(', ')}`
    }));
    console.log('Generated summaries:', summaries);
    setSummaryData(summaries);
  }, []);

  console.log('Current emotion data:', emotionData);
  console.log('Current summary data:', summaryData);

  return (
    <div className="container">
      <header>
        <h1>Child Emotion Tracker</h1>
        <p className="subtitle">Monitor and understand your child's emotional patterns</p>
      </header>

      <main>
        <section className="chart-section">
          <h2 className="section-title">Emotion Tracker</h2>
          {emotionData.length > 0 ? (
            <EmotionChart data={emotionData} summaryData={summaryData} />
          ) : (
            <p>Loading emotion data...</p>
          )}
        </section>

        <section className="summary-section">
          <h2 className="section-title">Daily Summaries</h2>
          {summaryData.length > 0 ? (
            <SummaryList summaries={summaryData} />
          ) : (
            <p>Loading summaries...</p>
          )}
        </section>
      </main>

      <footer>
        <p>Data last updated: {new Date().toLocaleDateString()}</p>
      </footer>
    </div>
  );
}

export default App;
