import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { format } from 'date-fns';
import './App.css';
import { Observation, ParentInputState } from './types';

const API_BASE_URL = 'http://localhost:5000/api';

const App: React.FC = () => {
  const [state, setState] = useState<ParentInputState>({
    observations: [],
    currentMessage: '',
    isLoading: false,
    error: null
  });

  useEffect(() => {
    fetchObservations();
  }, []);

  const fetchObservations = async () => {
    try {
      setState(prev => ({ ...prev, isLoading: true }));
      const response = await axios.get(`${API_BASE_URL}/observations`);
      setState(prev => ({
        ...prev,
        observations: response.data,
        isLoading: false
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: 'Failed to fetch observations',
        isLoading: false
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!state.currentMessage.trim()) return;

    try {
      setState(prev => ({ ...prev, isLoading: true }));
      await axios.post(`${API_BASE_URL}/observations`, {
        message: state.currentMessage
      });
      
      setState(prev => ({
        ...prev,
        currentMessage: '',
        isLoading: false
      }));
      
      fetchObservations();
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: 'Failed to save observation',
        isLoading: false
      }));
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Child Well-being Tracker</h1>
        <p className="date-display">
          Today's Date: {format(new Date(), 'dd/MM/yyyy')}
        </p>
      </header>

      <main className="main-content">
        <section className="input-section">
          <h2>Enter your observations</h2>
          <form onSubmit={handleSubmit} className="observation-form">
            <textarea
              value={state.currentMessage}
              onChange={(e) => setState(prev => ({ ...prev, currentMessage: e.target.value }))}
              placeholder="Enter your observations here..."
              className="observation-input"
              rows={10}
            />
            <button
              type="submit"
              className="submit-button"
              disabled={state.isLoading || !state.currentMessage.trim()}
            >
              {state.isLoading ? 'Saving...' : 'Save Observation'}
            </button>
          </form>
        </section>

        <section className="observations-section">
          <h2>Recent Observations</h2>
          {state.error && <p className="error-message">{state.error}</p>}
          {state.isLoading ? (
            <p>Loading...</p>
          ) : (
            <div className="observations-list">
              {state.observations.map((observation) => (
                <div key={observation.id} className="observation-card">
                  <p className="observation-date">
                    {format(new Date(observation.date), 'dd/MM/yyyy HH:mm')}
                  </p>
                  <p className="observation-message">{observation.message}</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
};

export default App; 