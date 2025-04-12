import React, { useState } from 'react';
import './PasscodeModal.css';

interface PasscodeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (passcode: string) => void;
  targetDashboard: 'parent' | 'child';
}

const PasscodeModal: React.FC<PasscodeModalProps> = ({ isOpen, onClose, onSubmit, targetDashboard }) => {
  const [passcode, setPasscode] = useState('');
  const [error, setError] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value.length <= 4 && /^\d*$/.test(value)) {
      setPasscode(value);
      setError('');
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (passcode.length === 4) {
      onSubmit(passcode);
      setPasscode('');
    } else {
      setError('Please enter a 4-digit passcode');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Enter Passcode</h2>
        <p>Please enter the 4-digit passcode to access the {targetDashboard}'s dashboard</p>
        <form onSubmit={handleSubmit}>
          <input
            type="password"
            value={passcode}
            onChange={handleInputChange}
            placeholder="Enter 4-digit passcode"
            maxLength={4}
            pattern="[0-9]*"
            inputMode="numeric"
            autoFocus
          />
          {error && <p className="error-message">{error}</p>}
          <div className="button-group">
            <button type="button" onClick={onClose} className="cancel-button">
              Cancel
            </button>
            <button type="submit" className="submit-button">
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PasscodeModal; 