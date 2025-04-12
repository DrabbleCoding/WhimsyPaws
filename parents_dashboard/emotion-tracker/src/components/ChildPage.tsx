import React, { useState } from 'react';
import './ChildPage.css';

const ChildPage: React.FC = () => {
  const [message, setMessage] = useState('');

  const emotions = [
    { name: 'Neutral', color: '#87CEEB', textColor: '#4A90E2' },
    { name: 'Disgusted', color: '#98FB98', textColor: '#2E8B57' },
    { name: 'Happy', color: '#FFD700', textColor: '#FF8C00' },
    { name: 'Fearful', color: '#D3D3D3', textColor: '#FF7F50' },
    { name: 'Angry', color: '#A9A9A9', textColor: '#FF0000' },
    { name: 'Surprised', color: '#FFFFFF', textColor: '#228B22' },
    { name: 'Sad', color: '#D3D3D3', textColor: '#4B0082' }
  ];

  const handleEmotionClick = (emotion: string) => {
    setMessage(`I feel ${emotion.toLowerCase()}...`);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you can handle sending the emotion data
    console.log('Submitted feeling:', message);
  };

  return (
    <div className="child-page">
      <div className="scene">
        <div className="sky">
          {emotions.map((emotion, index) => (
            <button
              key={index}
              className="emotion-cloud"
              style={{
                backgroundColor: emotion.color,
                color: emotion.textColor
              }}
              onClick={() => handleEmotionClick(emotion.name)}
            >
              {emotion.name}
            </button>
          ))}
          {/* Sun for Happy */}
          <div className="sun">
            <button
              className="emotion-sun"
              onClick={() => handleEmotionClick('Happy')}
            >
              Happy
            </button>
          </div>
        </div>
        
        <div className="ground">
          <div className="mascot">
            <div className="speech-bubble">
              Hi Sam! How are you feeling right now?
            </div>
          </div>
          
          <form className="chat-input" onSubmit={handleSubmit}>
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="I feel..."
              className="feeling-input"
            />
            <button type="submit" className="submit-button">
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChildPage; 