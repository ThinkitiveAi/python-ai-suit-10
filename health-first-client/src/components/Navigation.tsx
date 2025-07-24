import React from 'react';
import { Stethoscope, Heart, Calendar } from 'lucide-react';

interface NavigationProps {
  currentView: 'provider-login' | 'provider-registration' | 'patient-login' | 'patient-registration' | 'provider-availability';
  onViewChange: (view: 'provider-login' | 'provider-registration' | 'patient-login' | 'patient-registration' | 'provider-availability') => void;
}

const Navigation: React.FC<NavigationProps> = ({ currentView, onViewChange }) => {
  return (
    <div className="fixed top-4 right-4 z-50">
      <div className="bg-white rounded-lg shadow-lg border border-gray-200 p-2">
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-2 px-3 py-2">
            <Stethoscope className="w-5 h-5 text-primary-600" />
            <span className="text-sm font-medium text-gray-700">Healthcare Portal</span>
          </div>
          
          <div className="border-l border-gray-300 h-6"></div>
          
          <div className="flex items-center space-x-1">
            <button
              onClick={() => onViewChange('provider-login')}
              className={`px-3 py-1 text-xs rounded-md transition-colors ${
                currentView === 'provider-login'
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              Provider Login
            </button>
            
            <button
              onClick={() => onViewChange('provider-registration')}
              className={`px-3 py-1 text-xs rounded-md transition-colors ${
                currentView === 'provider-registration'
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              Provider Reg
            </button>
            
            <button
              onClick={() => onViewChange('patient-login')}
              className={`px-3 py-1 text-xs rounded-md transition-colors ${
                currentView === 'patient-login'
                  ? 'bg-secondary-100 text-secondary-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              Patient Login
            </button>
            
            <button
              onClick={() => onViewChange('patient-registration')}
              className={`px-3 py-1 text-xs rounded-md transition-colors ${
                currentView === 'patient-registration'
                  ? 'bg-secondary-100 text-secondary-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              Patient Reg
            </button>
            
            <button
              onClick={() => onViewChange('provider-availability')}
              className={`px-3 py-1 text-xs rounded-md transition-colors ${
                currentView === 'provider-availability'
                  ? 'bg-green-100 text-green-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              }`}
            >
              <Calendar className="w-3 h-3 inline mr-1" />
              Availability
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Navigation; 