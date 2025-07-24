import React, { useState } from 'react';
import { User, Mail, Phone, Shield, Building, GraduationCap, Stethoscope, CheckCircle } from 'lucide-react';
import PhotoUpload from './PhotoUpload';
import PasswordStrength from './PasswordStrength';
import FormSection from './FormSection';

interface FormData {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  profilePhoto: File | null;
  licenseNumber: string;
  specialization: string;
  yearsExperience: string;
  qualifications: string;
  clinicName: string;
  street: string;
  city: string;
  state: string;
  zipCode: string;
  practiceType: string;
  password: string;
  confirmPassword: string;
  termsAccepted: boolean;
}

interface FormErrors {
  [key: string]: string;
}

const specializations = [
  'Cardiology',
  'Dermatology',
  'Pediatrics',
  'Neurology',
  'Orthopedics',
  'Oncology',
  'Psychiatry',
  'General Practice',
  'Emergency Medicine',
  'Internal Medicine',
  'Surgery',
  'Radiology',
  'Anesthesiology',
  'Obstetrics & Gynecology',
  'Ophthalmology',
  'ENT',
  'Urology',
  'Gastroenterology',
  'Endocrinology',
  'Rheumatology'
];

const practiceTypes = [
  'Private Practice',
  'Hospital',
  'Clinic',
  'Medical Center',
  'Urgent Care',
  'Specialty Practice',
  'Academic Medical Center',
  'Government Facility'
];

interface ProviderRegistrationProps {
  onNavigateToLogin?: () => void;
}

const ProviderRegistration: React.FC<ProviderRegistrationProps> = ({ onNavigateToLogin }) => {
  const [formData, setFormData] = useState<FormData>({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    profilePhoto: null,
    licenseNumber: '',
    specialization: '',
    yearsExperience: '',
    qualifications: '',
    clinicName: '',
    street: '',
    city: '',
    state: '',
    zipCode: '',
    practiceType: '',
    password: '',
    confirmPassword: '',
    termsAccepted: false
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const validateField = (name: string, value: string): string => {
    switch (name) {
      case 'firstName':
      case 'lastName':
        return value.trim() ? '' : 'This field is required';
      case 'email':
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(value) ? '' : 'Please enter a valid email address';
      case 'phone':
        const phoneRegex = /^\(\d{3}\) \d{3}-\d{4}$/;
        return phoneRegex.test(value) ? '' : 'Please enter a valid phone number (XXX) XXX-XXXX';
      case 'licenseNumber':
        return value.trim() ? '' : 'Medical license number is required';
      case 'password':
        if (value.length < 8) return 'Password must be at least 8 characters long';
        if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
          return 'Password must contain uppercase, lowercase, and number';
        }
        return '';
      case 'confirmPassword':
        return value === formData.password ? '' : 'Passwords do not match';
      default:
        return value.trim() ? '' : 'This field is required';
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handlePhotoUpload = (file: File) => {
    setFormData(prev => ({
      ...prev,
      profilePhoto: file
    }));
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};
    
    Object.keys(formData).forEach(key => {
      if (key !== 'profilePhoto' && key !== 'termsAccepted') {
        const error = validateField(key, formData[key as keyof FormData] as string);
        if (error) newErrors[key] = error;
      }
    });

    if (!formData.termsAccepted) {
      newErrors.termsAccepted = 'You must accept the terms and conditions';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      setIsSubmitting(false);
      setSubmitSuccess(true);
    }, 2000);
  };

  if (submitSuccess) {
    return (
      <div className="min-h-screen bg-medical-gray flex items-center justify-center">
        <div className="card max-w-md w-full text-center">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Registration Successful!</h2>
          <p className="text-gray-600 mb-6">
            Thank you for registering. We've sent a verification email to {formData.email}. 
            Please check your inbox and follow the instructions to complete your registration.
          </p>
          <button 
            onClick={() => setSubmitSuccess(false)}
            className="btn-primary w-full"
          >
            Register Another Provider
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-medical-gray py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Stethoscope className="w-8 h-8 text-primary-500 mr-3" />
            <h1 className="text-3xl font-bold text-gray-900">Provider Registration</h1>
          </div>
          <p className="text-gray-600">Join our healthcare network and start providing exceptional care</p>
        </div>

        <form onSubmit={handleSubmit} className="card">
          {/* Personal Information */}
          <FormSection 
            title="Personal Information" 
            icon={<User className="w-5 h-5" />}
          >
            <div className="form-row">
              <div>
                <label htmlFor="firstName" className="form-label">First Name *</label>
                <input
                  type="text"
                  id="firstName"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleInputChange}
                  className={`form-input ${errors.firstName ? 'border-red-500' : ''}`}
                  placeholder="Enter first name"
                />
                {errors.firstName && <div className="error-message">{errors.firstName}</div>}
              </div>
              <div>
                <label htmlFor="lastName" className="form-label">Last Name *</label>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleInputChange}
                  className={`form-input ${errors.lastName ? 'border-red-500' : ''}`}
                  placeholder="Enter last name"
                />
                {errors.lastName && <div className="error-message">{errors.lastName}</div>}
              </div>
            </div>

            <div className="form-row">
              <div>
                <label htmlFor="email" className="form-label">Email Address *</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className={`form-input pl-10 ${errors.email ? 'border-red-500' : ''}`}
                    placeholder="Enter email address"
                  />
                </div>
                {errors.email && <div className="error-message">{errors.email}</div>}
              </div>
              <div>
                <label htmlFor="phone" className="form-label">Phone Number *</label>
                <div className="relative">
                  <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className={`form-input pl-10 ${errors.phone ? 'border-red-500' : ''}`}
                    placeholder="(XXX) XXX-XXXX"
                  />
                </div>
                {errors.phone && <div className="error-message">{errors.phone}</div>}
              </div>
            </div>

            <div>
              <label className="form-label">Profile Photo</label>
              <PhotoUpload onPhotoUpload={handlePhotoUpload} />
            </div>
          </FormSection>

          {/* Professional Information */}
          <FormSection 
            title="Professional Information" 
            icon={<GraduationCap className="w-5 h-5" />}
          >
            <div className="form-row">
              <div>
                <label htmlFor="licenseNumber" className="form-label">Medical License Number *</label>
                <input
                  type="text"
                  id="licenseNumber"
                  name="licenseNumber"
                  value={formData.licenseNumber}
                  onChange={handleInputChange}
                  className={`form-input ${errors.licenseNumber ? 'border-red-500' : ''}`}
                  placeholder="Enter license number"
                />
                {errors.licenseNumber && <div className="error-message">{errors.licenseNumber}</div>}
              </div>
              <div>
                <label htmlFor="specialization" className="form-label">Specialization *</label>
                <select
                  id="specialization"
                  name="specialization"
                  value={formData.specialization}
                  onChange={handleInputChange}
                  className={`form-input ${errors.specialization ? 'border-red-500' : ''}`}
                >
                  <option value="">Select specialization</option>
                  {specializations.map(spec => (
                    <option key={spec} value={spec}>{spec}</option>
                  ))}
                </select>
                {errors.specialization && <div className="error-message">{errors.specialization}</div>}
              </div>
            </div>

            <div className="form-row">
              <div>
                <label htmlFor="yearsExperience" className="form-label">Years of Experience *</label>
                <select
                  id="yearsExperience"
                  name="yearsExperience"
                  value={formData.yearsExperience}
                  onChange={handleInputChange}
                  className={`form-input ${errors.yearsExperience ? 'border-red-500' : ''}`}
                >
                  <option value="">Select experience</option>
                  {Array.from({ length: 50 }, (_, i) => i + 1).map(year => (
                    <option key={year} value={year}>{year} {year === 1 ? 'year' : 'years'}</option>
                  ))}
                </select>
                {errors.yearsExperience && <div className="error-message">{errors.yearsExperience}</div>}
              </div>
              <div>
                <label htmlFor="qualifications" className="form-label">Medical Degree/Qualifications *</label>
                <textarea
                  id="qualifications"
                  name="qualifications"
                  value={formData.qualifications}
                  onChange={handleInputChange}
                  className={`form-input ${errors.qualifications ? 'border-red-500' : ''}`}
                  placeholder="Enter your medical degrees and qualifications"
                  rows={3}
                />
                {errors.qualifications && <div className="error-message">{errors.qualifications}</div>}
              </div>
            </div>
          </FormSection>

          {/* Practice Information */}
          <FormSection 
            title="Practice Information" 
            icon={<Building className="w-5 h-5" />}
          >
            <div>
              <label htmlFor="clinicName" className="form-label">Clinic/Hospital Name *</label>
              <input
                type="text"
                id="clinicName"
                name="clinicName"
                value={formData.clinicName}
                onChange={handleInputChange}
                className={`form-input ${errors.clinicName ? 'border-red-500' : ''}`}
                placeholder="Enter clinic or hospital name"
              />
              {errors.clinicName && <div className="error-message">{errors.clinicName}</div>}
            </div>

            <div className="form-row">
              <div>
                <label htmlFor="practiceType" className="form-label">Practice Type *</label>
                <select
                  id="practiceType"
                  name="practiceType"
                  value={formData.practiceType}
                  onChange={handleInputChange}
                  className={`form-input ${errors.practiceType ? 'border-red-500' : ''}`}
                >
                  <option value="">Select practice type</option>
                  {practiceTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
                {errors.practiceType && <div className="error-message">{errors.practiceType}</div>}
              </div>
            </div>

            <div>
              <label className="form-label">Clinic Address *</label>
              <div className="space-y-4">
                <div>
                  <input
                    type="text"
                    name="street"
                    value={formData.street}
                    onChange={handleInputChange}
                    className={`form-input ${errors.street ? 'border-red-500' : ''}`}
                    placeholder="Street address"
                  />
                  {errors.street && <div className="error-message">{errors.street}</div>}
                </div>
                <div className="form-row">
                  <div>
                    <input
                      type="text"
                      name="city"
                      value={formData.city}
                      onChange={handleInputChange}
                      className={`form-input ${errors.city ? 'border-red-500' : ''}`}
                      placeholder="City"
                    />
                    {errors.city && <div className="error-message">{errors.city}</div>}
                  </div>
                  <div>
                    <input
                      type="text"
                      name="state"
                      value={formData.state}
                      onChange={handleInputChange}
                      className={`form-input ${errors.state ? 'border-red-500' : ''}`}
                      placeholder="State"
                    />
                    {errors.state && <div className="error-message">{errors.state}</div>}
                  </div>
                  <div>
                    <input
                      type="text"
                      name="zipCode"
                      value={formData.zipCode}
                      onChange={handleInputChange}
                      className={`form-input ${errors.zipCode ? 'border-red-500' : ''}`}
                      placeholder="ZIP Code"
                    />
                    {errors.zipCode && <div className="error-message">{errors.zipCode}</div>}
                  </div>
                </div>
              </div>
            </div>
          </FormSection>

          {/* Account Security */}
          <FormSection 
            title="Account Security" 
            icon={<Shield className="w-5 h-5" />}
          >
            <div className="form-row">
              <div>
                <label htmlFor="password" className="form-label">Password *</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  className={`form-input ${errors.password ? 'border-red-500' : ''}`}
                  placeholder="Create a strong password"
                />
                <PasswordStrength password={formData.password} />
                {errors.password && <div className="error-message">{errors.password}</div>}
              </div>
              <div>
                <label htmlFor="confirmPassword" className="form-label">Confirm Password *</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  className={`form-input ${errors.confirmPassword ? 'border-red-500' : ''}`}
                  placeholder="Confirm your password"
                />
                {errors.confirmPassword && <div className="error-message">{errors.confirmPassword}</div>}
              </div>
            </div>
          </FormSection>

          {/* Terms and Conditions */}
          <div className="border-t pt-6">
            <div className="flex items-start space-x-3">
              <input
                type="checkbox"
                id="termsAccepted"
                name="termsAccepted"
                checked={formData.termsAccepted}
                onChange={handleInputChange}
                className="mt-1 h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <div className="flex-1">
                <label htmlFor="termsAccepted" className="text-sm text-gray-700">
                  I agree to the{' '}
                  <a href="#" className="text-primary-600 hover:text-primary-500 underline">
                    Terms and Conditions
                  </a>
                  {' '}and{' '}
                  <a href="#" className="text-primary-600 hover:text-primary-500 underline">
                    Privacy Policy
                  </a>
                </label>
                {errors.termsAccepted && <div className="error-message">{errors.termsAccepted}</div>}
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="border-t pt-6">
            <button
              type="submit"
              disabled={isSubmitting}
              className="btn-primary w-full flex items-center justify-center"
            >
              {isSubmitting ? (
                <>
                  <div className="loading-spinner mr-2"></div>
                  Processing...
                </>
              ) : (
                'Complete Registration'
              )}
            </button>
          </div>

          {/* Footer */}
          <div className="text-center mt-6">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <button 
                type="button"
                onClick={onNavigateToLogin}
                className="text-primary-600 hover:text-primary-500 font-medium bg-transparent border-none cursor-pointer underline"
              >
                Sign in here
              </button>
            </p>
            <div className="mt-4 flex justify-center space-x-6 text-sm">
              <a href="#privacy" className="text-gray-500 hover:text-gray-700">
                Privacy Policy
              </a>
              <a href="#terms" className="text-gray-500 hover:text-gray-700">
                Terms of Service
              </a>
              <a href="#support" className="text-gray-500 hover:text-gray-700">
                Support
              </a>
            </div>
            <p className="text-xs text-gray-400 mt-2">
              © 2024 Healthcare Provider Portal. All rights reserved.
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProviderRegistration; 