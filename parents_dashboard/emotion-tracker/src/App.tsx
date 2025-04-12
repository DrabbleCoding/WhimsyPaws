import React, { useState, useEffect } from 'react';
import './styles/global.css';
import EmotionChart from './components/EmotionChart';
import SummaryList from './components/SummaryList';
import ChildPage from './components/ChildPage';
import PasscodeModal from './components/PasscodeModal';

// Import the data files from the src directory
import emotionsData from './emotions.json';
import summaryData from './summary.json';

interface EmotionData {
  date: string;
  emotions: {
    anger: number;
    disgust: number;
    fear: number;
    joy: number;
    neutral: number;
    sadness: number;
    surprise: number;
  };
}

interface SummaryData {
  date: string;
  description: string;
}

function App() {
  const [emotionData, setEmotionData] = useState<EmotionData[]>([]);
  const [summaries, setSummaries] = useState<SummaryData[]>([]);
  const [currentPage, setCurrentPage] = useState<'parent' | 'child'>('parent');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [targetDashboard, setTargetDashboard] = useState<'parent' | 'child'>('parent');

  // In a real app, these would be stored securely and possibly different for each user
  const PARENT_PASSCODE = '1234';
  const CHILD_PASSCODE = '5678';

  useEffect(() => {
    // Convert the emotions data to the format we need
    const formattedData: EmotionData[] = Object.entries(emotionsData).map(([date, emotions]: [string, any]) => ({
      date,
      emotions: {
        anger: emotions.anger || 0,
        disgust: emotions.disgust || 0,
        fear: emotions.fear || 0,
        joy: emotions.joy || 0,
        neutral: emotions.neutral || 0,
        sadness: emotions.sadness || 0,
        surprise: emotions.surprise || 0
      }
    }));
    
    setEmotionData(formattedData);

    // Convert the summary data to the format we need
    const formattedSummaries: SummaryData[] = Object.entries(summaryData).map(([date, description]) => ({
      date,
      description: description as string
    }));
    
    setSummaries(formattedSummaries);
  }, []);

  const handleDashboardSwitch = (target: 'parent' | 'child') => {
    setTargetDashboard(target);
    setIsModalOpen(true);
  };

  const handlePasscodeSubmit = (passcode: string) => {
    const correctPasscode = targetDashboard === 'parent' ? PARENT_PASSCODE : CHILD_PASSCODE;
    
    if (passcode === correctPasscode) {
      setCurrentPage(targetDashboard);
      setIsModalOpen(false);
    } else {
      // In a real app, you might want to handle incorrect passcodes differently
      alert('Incorrect passcode. Please try again.');
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Emotion Tracker</h1>
        <p className="subtitle">Track and visualize emotional patterns over time</p>
        <div className="navigation-buttons">
          <button 
            className={`nav-button ${currentPage === 'parent' ? 'active' : ''}`}
            onClick={() => handleDashboardSwitch('parent')}
          >
            Parent's Dashboard
          </button>
          <button 
            className={`nav-button ${currentPage === 'child' ? 'active' : ''}`}
            onClick={() => handleDashboardSwitch('child')}
          >
            Child's Dashboard
          </button>
        </div>
      </header>
      
      <main className="main-content">
        {currentPage === 'parent' ? (
          <>
            <section className="chart-section">
              <EmotionChart data={emotionData} summaryData={summaries} />
            </section>
            
            <section className="summary-section">
              <SummaryList summaries={summaries} />
            </section>
          </>
        ) : (
          <ChildPage />
        )}
      </main>
      
      <footer className="app-footer">
        <p>Data last updated: {new Date().toLocaleDateString()}</p>
      </footer>

      <PasscodeModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handlePasscodeSubmit}
        targetDashboard={targetDashboard}
      />
    </div>
  );
}

export default App;
