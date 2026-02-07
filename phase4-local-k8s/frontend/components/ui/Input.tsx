import React from 'react';

interface InputProps {
  label?: string;
  placeholder?: string;
  type?: 'text' | 'email' | 'password' | 'textarea';
  value: string;
  onChange: (value: string) => void;
  error?: string;
  required?: boolean;
}

const Input: React.FC<InputProps> = ({
  label,
  placeholder,
  type = 'text',
  value,
  onChange,
  error,
  required = false
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    onChange(e.target.value);
  };

  const inputProps = {
    value,
    onChange: handleChange,
    placeholder,
    required,
  };

  return (
    <div className="mb-5">
      {label && (
        <label className="block text-gray-700 text-sm font-medium mb-2">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}

      {type === 'textarea' ? (
        <textarea
          {...inputProps}
          className={`w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 shadow-sm ${
            error
              ? 'border-red-500 focus:ring-red-300'
              : 'border-gray-300 focus:ring-blue-300'
          }`}
        />
      ) : (
        <input
          {...inputProps}
          type={type}
          className={`w-full px-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 shadow-sm ${
            error
              ? 'border-red-500 focus:ring-red-300'
              : 'border-gray-300 focus:ring-blue-300'
          }`}
        />
      )}

      {error && <p className="text-red-500 text-xs italic mt-2">{error}</p>}
    </div>
  );
};

export default Input;