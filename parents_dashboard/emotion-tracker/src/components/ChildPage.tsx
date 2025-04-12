import React, { useState } from 'react';
import './ChildPage.css';

// Import cloud assets
import happySun from '../images/assets/happy_sun.png';
import sadCloud from '../images/assets/sad_cloud.png';
import angryCloud from '../images/assets/angry_cloud.png';
import fearfulCloud from '../images/assets/fearful_cloud.png';
import disgustedCloud from '../images/assets/disgusted_cloud.png';
import surprisedCloud from '../images/assets/surprised_cloud.png';
import neutralCloud from '../images/assets/neutral_cloud.png';
import grass from '../images/assets/grass.png';

// Import bear icon
import bearNeutral from '../images/icons/bear_neutral.png';

const emotions = [
  { name: 'Happy', image: happySun, color: '#FFD700', position: 'top-right' },
  { name: 'Sad', image: sadCloud, color: '#87CEEB', position: 'random' },
  { name: 'Angry', image: angryCloud, color: '#FF6B6B', position: 'random' },
  { name: 'Fearful', image: fearfulCloud, color: '#FFB6C1', position: 'random' },
  { name: 'Disgusted', image: disgustedCloud, color: '#98FB98', position: 'random' },
  { name: 'Surprised', image: surprisedCloud, color: '#DDA0DD', position: 'random' },
  { name: 'Neutral', image: neutralCloud, color: '#F5F5F5', position: 'random' }
];

const ChildPage: React.FC = () => {
  const [selectedEmotion, setSelectedEmotion] = useState<string | null>(null);
  const [message, setMessage] = useState<string>('How are you feeling today?');
  const [inputText, setInputText] = useState<string>('');

  const handleEmotionClick = (emotion: string) => {
    setSelectedEmotion(emotion);
    setMessage(`You're feeling ${emotion.toLowerCase()}! Would you like to tell me more?`);
  };

  const handleSubmit = async () => {
    if (!inputText.trim()) return;

    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputText }),
      });

      if (response.ok) {
        setInputText('');
        setMessage('Thank you for sharing! How else are you feeling?');
      } else {
        setMessage('Sorry, there was an error sending your message. Please try again.');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessage('Sorry, there was an error sending your message. Please try again.');
    }
  };

  return (
    <div className="child-page">
      <div className="scene">
        <div className="sky">
          {emotions.map((emotion) => (
            <button
              key={emotion.name}
              className={`emotion-cloud ${emotion.position}`}
              onClick={() => handleEmotionClick(emotion.name)}
            >
              <img src={emotion.image} alt={emotion.name} className="cloud-image" />
              <span className="cloud-text">{emotion.name}</span>
            </button>
          ))}
        </div>
        
        <div className="ground">
          <img src={grass} alt="Grass" className="grass-image" />
          <div className="mascot">
            <img src={bearNeutral} alt="Bear" className="bear-image" />
            <div className="thought-bubble">
              {message}
            </div>
          </div>
          
          <div className="chat-input">
            <input
              type="text"
              className="feeling-input"
              placeholder="Tell me more about how you feel..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
            />
            <button className="submit-button" onClick={handleSubmit}>
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChildPage; 