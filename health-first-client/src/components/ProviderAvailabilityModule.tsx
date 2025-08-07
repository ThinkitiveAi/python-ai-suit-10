import React, { useState } from 'react';
import { 
  Calendar, 
  Clock, 
  MapPin, 
  DollarSign, 
  User, 
  Settings, 
  Plus, 
  Trash2, 
  Edit3,
  Search,
  Bell,
  MessageCircle,
  ChevronDown,
  CheckCircle,
  AlertCircle,
  Loader2
} from 'lucide-react';

interface DayAvailability {
  day: string;
  from: string;
  till: string;
  enabled: boolean;
}

interface BlockDay {
  date: string;
  from: string;
  till: string;
}

interface SlotSettings {
  timeZone: string;
  slotDuration: number;
  breakDuration: number;
  maxAppointmentsPerSlot: number;
  appointmentTypes: string[];
  locations: string[];
  pricing: {
    fee: number;
    currency: string;
    insuranceAccepted: boolean;
  };
}

const ProviderAvailabilityModule: React.FC = () => {
  const [selectedProvider, setSelectedProvider] = useState('John Doe');
  const [dayWiseAvailability, setDayWiseAvailability] = useState<DayAvailability[]>([
    { day: 'Monday', from: '09:00', till: '18:00', enabled: true },
    { day: 'Tuesday', from: '09:00', till: '18:00', enabled: true },
    { day: 'Wednesday', from: '09:00', till: '18:00', enabled: true },
    { day: 'Thursday', from: '09:00', till: '18:00', enabled: true },
    { day: 'Friday', from: '09:00', till: '18:00', enabled: true },
    { day: 'Saturday', from: '09:00', till: '18:00', enabled: true },
    { day: 'Sunday', from: '09:00', till: '18:00', enabled: false }
  ]);

  const [blockDays, setBlockDays] = useState<BlockDay[]>([
    { date: '', from: '', till: '' }
  ]);

  const [slotSettings, setSlotSettings] = useState<SlotSettings>({
    timeZone: 'America/New_York',
    slotDuration: 30,
    breakDuration: 15,
    maxAppointmentsPerSlot: 1,
    appointmentTypes: ['Consultation', 'Follow-up', 'Emergency'],
    locations: ['Main Clinic', 'Virtual'],
    pricing: {
      fee: 150,
      currency: 'USD',
      insuranceAccepted: true
    }
  });

  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const daysOfWeek = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
  ];

  const timeZones = [
    { value: 'America/New_York', label: 'Eastern Time (ET)' },
    { value: 'America/Chicago', label: 'Central Time (CT)' },
    { value: 'America/Denver', label: 'Mountain Time (MT)' },
    { value: 'America/Los_Angeles', label: 'Pacific Time (PT)' },
    { value: 'America/Anchorage', label: 'Alaska Time (AKT)' },
    { value: 'Pacific/Honolulu', label: 'Hawaii Time (HST)' }
  ];

  const handleSave = async () => {
    setIsLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      setIsSuccess(true);
      setTimeout(() => setIsSuccess(false), 3000);
    } catch (error) {
      console.error('Save error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const addBlockDay = () => {
    setBlockDays([...blockDays, { date: '', from: '', till: '' }]);
  };

  const removeBlockDay = (index: number) => {
    const updated = blockDays.filter((_, i) => i !== index);
    setBlockDays(updated);
  };

  const updateDayAvailability = (index: number, field: keyof DayAvailability, value: string | boolean) => {
    const updated = [...dayWiseAvailability];
    updated[index] = { ...updated[index], [field]: value };
    setDayWiseAvailability(updated);
  };

  const updateBlockDay = (index: number, field: keyof BlockDay, value: string) => {
    const updated = [...blockDays];
    updated[index] = { ...updated[index], [field]: value };
    setBlockDays(updated);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-blue-900 text-white">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-8">
              <h1 className="text-xl font-semibold">Sample EMR</h1>
              <nav className="flex space-x-6">
                <button className="text-gray-300 hover:text-white transition-colors">Dashboard</button>
                <button className="text-gray-300 hover:text-white transition-colors">Scheduling</button>
                <button className="text-gray-300 hover:text-white transition-colors">Patients</button>
                <button className="text-gray-300 hover:text-white transition-colors">Communications</button>
                <button className="text-gray-300 hover:text-white transition-colors">Billing</button>
                <button className="text-gray-300 hover:text-white transition-colors">Referral</button>
                <button className="text-gray-300 hover:text-white transition-colors">Reports</button>
                <button className="text-white font-medium bg-blue-800 px-4 py-2 rounded-lg">Settings</button>
              </nav>
            </div>
            <div className="flex items-center space-x-4">
              <button className="text-gray-300 hover:text-white">
                <Search className="w-5 h-5" />
              </button>
              <button className="text-gray-300 hover:text-white">
                <MessageCircle className="w-5 h-5" />
              </button>
              <button className="text-gray-300 hover:text-white">
                <Bell className="w-5 h-5" />
              </button>
              <button className="flex items-center space-x-2 text-gray-300 hover:text-white">
                <div className="w-8 h-8 bg-blue-700 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4" />
                </div>
                <ChevronDown className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-lg">
          {/* Success Message */}
          {isSuccess && (
            <div className="bg-green-50 border border-green-200 rounded-t-xl p-4">
              <div className="flex items-center">
                <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                <p className="text-green-700 font-medium">Provider availability updated successfully!</p>
              </div>
            </div>
          )}

          <div className="p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-8">Provider Availability</h2>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Left Side - Day Wise Availability */}
              <div>
                {/* Provider Selection */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Provider</label>
                  <select
                    value={selectedProvider}
                    onChange={(e) => setSelectedProvider(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="John Doe">John Doe</option>
                    <option value="Jane Smith">Jane Smith</option>
                    <option value="Dr. Johnson">Dr. Johnson</option>
                    <option value="Dr. Williams">Dr. Williams</option>
                  </select>
                </div>

                {/* Day Wise Availability */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Day Wise Availability</h3>
                  <div className="space-y-3">
                    {dayWiseAvailability.map((day, index) => (
                      <div key={day.day} className="grid grid-cols-4 gap-4 items-center p-3 border border-gray-200 rounded-lg">
                        <div>
                          <select
                            value={day.day}
                            onChange={(e) => updateDayAvailability(index, 'day', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          >
                            {daysOfWeek.map(d => (
                              <option key={d} value={d}>{d}</option>
                            ))}
                          </select>
                        </div>
                        <div>
                          <input
                            type="time"
                            value={day.from}
                            onChange={(e) => updateDayAvailability(index, 'from', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <input
                            type="time"
                            value={day.till}
                            onChange={(e) => updateDayAvailability(index, 'till', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <button
                            onClick={() => {
                              const updated = dayWiseAvailability.filter((_, i) => i !== index);
                              setDayWiseAvailability(updated);
                            }}
                            className="text-red-600 hover:text-red-700 p-2"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Right Side - Slot Creation Setting */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Slot Creation Setting</h3>
                
                {/* Time Zone */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Time Zone</label>
                  <select
                    value={slotSettings.timeZone}
                    onChange={(e) => setSlotSettings({...slotSettings, timeZone: e.target.value})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    {timeZones.map(tz => (
                      <option key={tz.value} value={tz.value}>{tz.label}</option>
                    ))}
                  </select>
                </div>

                {/* Slot Duration */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Slot Duration (minutes)</label>
                  <select
                    value={slotSettings.slotDuration}
                    onChange={(e) => setSlotSettings({...slotSettings, slotDuration: parseInt(e.target.value)})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value={15}>15 minutes</option>
                    <option value={30}>30 minutes</option>
                    <option value={45}>45 minutes</option>
                    <option value={60}>60 minutes</option>
                  </select>
                </div>

                {/* Break Duration */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Break Duration (minutes)</label>
                  <select
                    value={slotSettings.breakDuration}
                    onChange={(e) => setSlotSettings({...slotSettings, breakDuration: parseInt(e.target.value)})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value={5}>5 minutes</option>
                    <option value={10}>10 minutes</option>
                    <option value={15}>15 minutes</option>
                    <option value={30}>30 minutes</option>
                  </select>
                </div>

                {/* Max Appointments Per Slot */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Max Appointments Per Slot</label>
                  <input
                    type="number"
                    value={slotSettings.maxAppointmentsPerSlot}
                    onChange={(e) => setSlotSettings({...slotSettings, maxAppointmentsPerSlot: parseInt(e.target.value)})}
                    min="1"
                    max="10"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                {/* Pricing */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Consultation Fee</label>
                  <div className="flex space-x-2">
                    <select
                      value={slotSettings.pricing.currency}
                      onChange={(e) => setSlotSettings({
                        ...slotSettings, 
                        pricing: {...slotSettings.pricing, currency: e.target.value}
                      })}
                      className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="USD">USD</option>
                      <option value="EUR">EUR</option>
                      <option value="GBP">GBP</option>
                    </select>
                    <input
                      type="number"
                      value={slotSettings.pricing.fee}
                      onChange={(e) => setSlotSettings({
                        ...slotSettings, 
                        pricing: {...slotSettings.pricing, fee: parseInt(e.target.value)}
                      })}
                      className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Fee amount"
                    />
                  </div>
                </div>

                {/* Insurance Accepted */}
                <div className="mb-6">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={slotSettings.pricing.insuranceAccepted}
                      onChange={(e) => setSlotSettings({
                        ...slotSettings, 
                        pricing: {...slotSettings.pricing, insuranceAccepted: e.target.checked}
                      })}
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span className="ml-2 text-sm text-gray-700">Accept Insurance</span>
                  </label>
                </div>

                {/* Block Days */}
                <div>
                  <h4 className="text-md font-medium text-gray-900 mb-4">Block Days</h4>
                  <div className="space-y-4">
                    {blockDays.map((block, index) => (
                      <div key={index} className="grid grid-cols-4 gap-4 items-center p-3 border border-gray-200 rounded-lg">
                        <div>
                          <input
                            type="date"
                            value={block.date}
                            onChange={(e) => updateBlockDay(index, 'date', e.target.value)}
                            placeholder="Select Date"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <input
                            type="time"
                            value={block.from}
                            onChange={(e) => updateBlockDay(index, 'from', e.target.value)}
                            placeholder="Start Time"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <input
                            type="time"
                            value={block.till}
                            onChange={(e) => updateBlockDay(index, 'till', e.target.value)}
                            placeholder="End Time"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                        <div>
                          <button
                            onClick={() => removeBlockDay(index)}
                            className="text-red-600 hover:text-red-700 p-2"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    ))}
                    <button
                      onClick={addBlockDay}
                      className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200 flex items-center"
                    >
                      <Plus className="w-4 h-4 mr-2" />
                      + Add Block Days
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex justify-end space-x-4 pt-8 border-t border-gray-200 mt-8">
              <button className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors duration-200">
                Close
              </button>
              <button
                onClick={handleSave}
                disabled={isLoading}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 flex items-center"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Saving...
                  </>
                ) : (
                  'Save'
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProviderAvailabilityModule; 