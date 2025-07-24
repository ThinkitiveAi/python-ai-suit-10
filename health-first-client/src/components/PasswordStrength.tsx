import React from 'react';
import { Shield, AlertCircle } from 'lucide-react';

interface PasswordStrengthProps {
  password: string;
}

const PasswordStrength: React.FC<PasswordStrengthProps> = ({ password }) => {
  const getPasswordStrength = (password: string) => {
    if (password.length === 0) return { strength: 'none', score: 0, message: '' };
    
    let score = 0;
    const checks = {
      length: password.length >= 8,
      lowercase: /[a-z]/.test(password),
      uppercase: /[A-Z]/.test(password),
      number: /\d/.test(password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };

    score += checks.length ? 1 : 0;
    score += checks.lowercase ? 1 : 0;
    score += checks.uppercase ? 1 : 0;
    score += checks.number ? 1 : 0;
    score += checks.special ? 1 : 0;

    if (score <= 2) return { strength: 'weak', score, message: 'Password is too weak' };
    if (score <= 3) return { strength: 'medium', score, message: 'Password could be stronger' };
    return { strength: 'strong', score, message: 'Strong password' };
  };

  const strength = getPasswordStrength(password);

  if (password.length === 0) return null;

  return (
    <div className="mt-2 space-y-2">
      <div className="flex items-center space-x-2">
        <div className="flex-1 bg-gray-200 rounded-full h-2">
          <div
            className={`password-strength ${strength.strength} h-2 rounded-full transition-all duration-300`}
            style={{ width: `${(strength.score / 5) * 100}%` }}
          />
        </div>
        <div className="flex items-center space-x-1">
          {strength.strength === 'weak' && <AlertCircle className="w-4 h-4 text-red-500" />}
          {strength.strength === 'medium' && <AlertCircle className="w-4 h-4 text-yellow-500" />}
          {strength.strength === 'strong' && <Shield className="w-4 h-4 text-green-500" />}
          <span className={`text-xs font-medium ${
            strength.strength === 'weak' ? 'text-red-600' :
            strength.strength === 'medium' ? 'text-yellow-600' :
            'text-green-600'
          }`}>
            {strength.strength.charAt(0).toUpperCase() + strength.strength.slice(1)}
          </span>
        </div>
      </div>
      <p className={`text-xs ${
        strength.strength === 'weak' ? 'text-red-600' :
        strength.strength === 'medium' ? 'text-yellow-600' :
        'text-green-600'
      }`}>
        {strength.message}
      </p>
    </div>
  );
};

export default PasswordStrength; 