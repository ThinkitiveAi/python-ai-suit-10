import React from 'react';

interface FormSectionProps {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}

const FormSection: React.FC<FormSectionProps> = ({ title, icon, children }) => {
  return (
    <div className="form-section">
      <div className="flex items-center space-x-2 mb-6">
        <div className="medical-icon">
          {icon}
        </div>
        <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
      </div>
      {children}
    </div>
  );
};

export default FormSection; 