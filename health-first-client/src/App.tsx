import React, { useState, useEffect } from 'react';
import ProviderRegistration from './components/ProviderRegistration';
import ProviderLogin from './components/ProviderLogin';
import PatientLogin from './components/PatientLogin';
import PatientRegistration from './components/PatientRegistration';
import ProviderAvailability from './components/ProviderAvailability';
import Navigation from './components/Navigation';

function App() {
  const [currentView, setCurrentView] = useState<'provider-login' | 'provider-registration' | 'patient-login' | 'patient-registration' | 'provider-availability'>('provider-availability');

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

  return (
    <div className="App">
      <Navigation currentView={currentView} onViewChange={handleViewChange} />
      
      {currentView === 'provider-registration' && <ProviderRegistration />}
      {currentView === 'provider-login' && <ProviderLogin />}
      {currentView === 'patient-login' && <PatientLogin />}
      {currentView === 'patient-registration' && <PatientRegistration />}
      {currentView === 'provider-availability' && <ProviderAvailability />}
    </div>
  );
}

export default App; 