import React, { useState, useEffect } from 'react';
import ProviderRegistration from './components/ProviderRegistration';
import ProviderLogin from './components/ProviderLogin';
import PatientLogin from './components/PatientLogin';
import PatientRegistration from './components/PatientRegistration';
import ProviderAvailability from './components/ProviderAvailability';
import Navigation from './components/Navigation';

function App() {
  const [currentView, setCurrentView] = useState<'provider-login' | 'provider-registration' | 'patient-login' | 'patient-registration' | 'provider-availability'>('provider-login');

  // Handle URL parameters on component mount
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const viewParam = urlParams.get('view');
    
    if (viewParam === 'provider-registration') {
      setCurrentView('provider-registration');
    } else if (viewParam === 'provider-login') {
      setCurrentView('provider-login');
    } else if (viewParam === 'patient-login') {
      setCurrentView('patient-login');
    } else if (viewParam === 'patient-registration') {
      setCurrentView('patient-registration');
    } else if (viewParam === 'provider-availability') {
      setCurrentView('provider-availability');
    }
  }, []);

  // Update URL when view changes
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('view', currentView);
    window.history.replaceState(null, '', `?${urlParams.toString()}`);
  }, [currentView]);

  const handleViewChange = (view: 'provider-login' | 'provider-registration' | 'patient-login' | 'patient-registration' | 'provider-availability') => {
    setCurrentView(view);
  };

  // Navigation functions for components
  const handleNavigateToProviderLogin = () => {
    setCurrentView('provider-login');
  };

  const handleNavigateToProviderRegistration = () => {
    setCurrentView('provider-registration');
  };

  const handleNavigateToPatientLogin = () => {
    setCurrentView('patient-login');
  };

  const handleNavigateToPatientRegistration = () => {
    setCurrentView('patient-registration');
  };

  return (
    <div className="App">
      <Navigation currentView={currentView} onViewChange={handleViewChange} />
      
      {currentView === 'provider-registration' && (
        <ProviderRegistration onNavigateToLogin={handleNavigateToProviderLogin} />
      )}
      {currentView === 'provider-login' && (
        <ProviderLogin onNavigateToRegistration={handleNavigateToProviderRegistration} />
      )}
      {currentView === 'patient-login' && (
        <PatientLogin onNavigateToRegistration={handleNavigateToPatientRegistration} />
      )}
      {currentView === 'patient-registration' && (
        <PatientRegistration onNavigateToLogin={handleNavigateToPatientLogin} />
      )}
      {currentView === 'provider-availability' && <ProviderAvailability />}
    </div>
  );
}

export default App; 