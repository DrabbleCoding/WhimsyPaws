import React, { useState, useEffect } from 'react';
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

// Import monkey icons
import monkeyNeutral from '../images/icons/monkey_neutral.png';
import monkeyHappy from '../images/icons/monkey_happy.png';
import monkeySad from '../images/icons/monkey_sad.png';
import monkeySleepy from '../images/icons/monkey_sleepy.png';

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
  const [bearEmotion, setBearEmotion] = useState<'neutral' | 'happy' | 'sad' | 'sleepy'>('neutral');

  // Function to determine bear emotion based on message
  const updateBearEmotion = (message: string) => {
    const lowerMessage = message.toLowerCase();
    
    // Check for mean/negative words
    if (lowerMessage.includes('hate') || lowerMessage.includes('stupid') || 
        lowerMessage.includes('bad') || lowerMessage.includes('angry') ||
        lowerMessage.includes('sorry') || lowerMessage.includes('wasn\'t fun')) {
      setBearEmotion('sad');
    }
    // Check for positive/exciting words
    else if (lowerMessage.includes('happy') || lowerMessage.includes('excited') || 
             lowerMessage.includes('fun') || lowerMessage.includes('great') ||
             lowerMessage.includes('wonderful') || lowerMessage.includes('awesome')) {
      setBearEmotion('happy');
    }
    // Check for sleepy/tired message
    else if (lowerMessage.includes('sleepy') || lowerMessage.includes('tired') || 
             lowerMessage.includes('bye') || lowerMessage.includes('goodbye') ||
             lowerMessage.includes('talk to you again')) {
      setBearEmotion('sleepy');
    }
    // Default to neutral
    else {
      setBearEmotion('neutral');
    }
  };

  // Poll for new messages from the server
  useEffect(() => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch('http://localhost:5000/api/poll');
        const data = await response.json();
        
        if (data.status === 'success' && data.message) {
          setMessage(data.message);
          // Update bear emotion based on the bot's response
          updateBearEmotion(data.message);
        }
      } catch (error) {
        console.error('Error polling for messages:', error);
      }
    }, 1000); // Poll every second

    return () => clearInterval(pollInterval);
  }, []);

  const handleEmotionClick = (emotion: string) => {
    setSelectedEmotion(emotion);
    const newMessage = `You're feeling ${emotion.toLowerCase()}! Would you like to tell me more?`;
    setMessage(newMessage);
    updateBearEmotion(newMessage);
  };

  const handleSubmit = async () => {
    if (!inputText.trim()) return;

    try {
      // Update bear emotion based on user input before sending
      updateBearEmotion(inputText);
      
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputText }),
      });

      if (response.ok) {
        setInputText('');
      } else {
        setMessage('Sorry, there was an error sending your message. Please try again.');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessage('Sorry, there was an error sending your message. Please try again.');
    }
  };

  // Get the appropriate monkey image based on emotion
  const getMonkeyImage = () => {
    switch (bearEmotion) {
      case 'happy':
        return monkeyHappy;
      case 'sad':
        return monkeySad;
      case 'sleepy':
        return monkeySleepy;
      default:
        return monkeyNeutral;
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
            <img src={getMonkeyImage()} alt="Monkey" className="bear-image" />
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