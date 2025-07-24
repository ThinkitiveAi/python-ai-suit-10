import React, { useState } from 'react';
import { Heart, Mail, Phone, Lock, Eye, EyeOff, User, Shield, AlertCircle, CheckCircle, Loader2, HelpCircle } from 'lucide-react';

interface PatientLoginFormData {
  emailOrPhone: string;
  password: string;
  rememberMe: boolean;
}

interface PatientLoginFormErrors {
  emailOrPhone?: string;
  password?: string;
  general?: string;
}

interface PatientLoginProps {
  onNavigateToRegistration?: () => void;
}

const PatientLogin: React.FC<PatientLoginProps> = ({ onNavigateToRegistration }) => {
  const [formData, setFormData] = useState<PatientLoginFormData>({
    emailOrPhone: '',
    password: '',
    rememberMe: false
  });

  const [errors, setErrors] = useState<PatientLoginFormErrors>({});
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePhone = (phone: string) => {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
  };

  const validateForm = () => {
    const newErrors: PatientLoginFormErrors = {};

    if (!formData.emailOrPhone.trim()) {
      newErrors.emailOrPhone = 'Please enter your email or phone number';
    } else {
      const isEmail = formData.emailOrPhone.includes('@');
      if (isEmail && !validateEmail(formData.emailOrPhone)) {
        newErrors.emailOrPhone = 'Please enter a valid email address';
      } else if (!isEmail && !validatePhone(formData.emailOrPhone)) {
        newErrors.emailOrPhone = 'Please enter a valid phone number';
      }
    }

    if (!formData.password) {
      newErrors.password = 'Please enter your password';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (field: keyof PatientLoginFormData, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Clear field-specific error when user starts typing
    if (errors[field as keyof PatientLoginFormErrors]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setIsLoading(true);
    setErrors({});

    // Simulate API call
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Simulate success
      setIsSuccess(true);
      setTimeout(() => {
        // Redirect to patient dashboard
        window.location.href = '/patient-dashboard';
      }, 1500);
      
    } catch (error) {
      setErrors({ general: 'Login failed. Please check your credentials and try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const getInputIcon = () => {
    if (formData.emailOrPhone.includes('@')) {
      return <Mail className="w-5 h-5 text-gray-400" />;
    }
    return <Phone className="w-5 h-5 text-gray-400" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-blue-100 p-3 rounded-full">
              <Heart className="w-8 h-8 text-blue-600" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome Back
          </h1>
          <p className="text-gray-600 text-lg">
            Access your healthcare information securely
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email/Phone Input */}
            <div>
              <label htmlFor="emailOrPhone" className="block text-sm font-medium text-gray-700 mb-2">
                Email or Phone Number
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  {getInputIcon()}
                </div>
                <input
                  id="emailOrPhone"
                  type="text"
                  value={formData.emailOrPhone}
                  onChange={(e) => handleInputChange('emailOrPhone', e.target.value)}
                  className={`w-full pl-10 pr-4 py-4 border rounded-xl text-lg transition-colors duration-200 ${
                    errors.emailOrPhone 
                      ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
                      : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
                  } focus:ring-2 focus:ring-opacity-20`}
                  placeholder="Enter your email or phone number"
                  disabled={isLoading}
                />
              </div>
              {errors.emailOrPhone && (
                <p className="mt-2 text-sm text-red-600 flex items-center">
                  <AlertCircle className="w-4 h-4 mr-1" />
                  {errors.emailOrPhone}
                </p>
              )}
            </div>

            {/* Password Input */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="w-5 h-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={formData.password}
                  onChange={(e) => handleInputChange('password', e.target.value)}
                  className={`w-full pl-10 pr-12 py-4 border rounded-xl text-lg transition-colors duration-200 ${
                    errors.password 
                      ? 'border-red-300 focus:border-red-500 focus:ring-red-500' 
                      : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
                  } focus:ring-2 focus:ring-opacity-20`}
                  placeholder="Enter your password"
                  disabled={isLoading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  disabled={isLoading}
                >
                  {showPassword ? (
                    <EyeOff className="w-5 h-5 text-gray-400 hover:text-gray-600" />
                  ) : (
                    <Eye className="w-5 h-5 text-gray-400 hover:text-gray-600" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="mt-2 text-sm text-red-600 flex items-center">
                  <AlertCircle className="w-4 h-4 mr-1" />
                  {errors.password}
                </p>
              )}
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={formData.rememberMe}
                  onChange={(e) => handleInputChange('rememberMe', e.target.checked)}
                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  disabled={isLoading}
                />
                <span className="ml-2 text-sm text-gray-700">Remember me</span>
              </label>
              <button
                type="button"
                className="text-sm text-blue-600 hover:text-blue-700 font-medium"
                disabled={isLoading}
              >
                Forgot password?
              </button>
            </div>

            {/* General Error */}
            {errors.general && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-4">
                <p className="text-sm text-red-600 flex items-center">
                  <AlertCircle className="w-4 h-4 mr-2" />
                  {errors.general}
                </p>
              </div>
            )}

            {/* Success Message */}
            {isSuccess && (
              <div className="bg-green-50 border border-green-200 rounded-xl p-4">
                <p className="text-sm text-green-600 flex items-center">
                  <CheckCircle className="w-4 h-4 mr-2" />
                  Login successful! Redirecting to your dashboard...
                </p>
              </div>
            )}

            {/* Login Button */}
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-4 px-6 rounded-xl text-lg font-medium transition-all duration-200 ${
                isLoading
                  ? 'bg-gray-300 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-xl'
              }`}
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Signing in...
                </div>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Registration Link */}
          <div className="text-center mt-6">
            <p className="text-sm text-gray-600">
              New to our platform?{' '}
              <button
                type="button"
                onClick={onNavigateToRegistration}
                className="text-blue-600 hover:text-blue-700 font-medium"
              >
                Create an account
              </button>
            </p>
          </div>

          {/* Help Section */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="text-center">
              <p className="text-sm text-gray-500 mb-3">
                Need help signing in?
              </p>
              <div className="flex justify-center space-x-4 text-sm">
                <button className="text-blue-600 hover:text-blue-700 flex items-center">
                  <HelpCircle className="w-4 h-4 mr-1" />
                  Help Center
                </button>
                <button className="text-blue-600 hover:text-blue-700 flex items-center">
                  <Phone className="w-4 h-4 mr-1" />
                  Contact Support
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8">
          <p className="text-xs text-gray-500">
            Your health information is protected with bank-level security
          </p>
          <div className="mt-2 flex justify-center space-x-4 text-xs">
            <a href="#privacy" className="text-gray-500 hover:text-gray-700">
              Privacy Policy
            </a>
            <a href="#terms" className="text-gray-500 hover:text-gray-700">
              Terms of Service
            </a>
            <a href="#security" className="text-gray-500 hover:text-gray-700">
              Security
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientLogin; 