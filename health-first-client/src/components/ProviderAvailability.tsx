import React, { useState, useEffect } from 'react';
import { 
  Calendar, 
  Clock, 
  Plus, 
  Edit, 
  Trash2, 
  Copy, 
  Settings, 
  ChevronLeft, 
  ChevronRight, 
  CheckCircle, 
  AlertCircle, 
  Info, 
  Stethoscope,
  Users,
  CalendarDays,
  Clock3,
  Repeat,
  Save,
  X,
  MoreHorizontal,
  Filter,
  Search,
  Download,
  Upload
} from 'lucide-react';

interface TimeSlot {
  id: string;
  startTime: string;
  endTime: string;
  duration: number;
  status: 'available' | 'booked' | 'blocked' | 'tentative' | 'break';
  date: string;
  notes?: string;
}

interface AvailabilityTemplate {
  id: string;
  name: string;
  slots: Omit<TimeSlot, 'id' | 'date'>[];
}

type CalendarView = 'month' | 'week' | 'day';

const ProviderAvailability: React.FC = () => {
  const [currentView, setCurrentView] = useState<CalendarView>('week');
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedSlots, setSelectedSlots] = useState<string[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingSlot, setEditingSlot] = useState<TimeSlot | null>(null);
  const [timeSlots, setTimeSlots] = useState<TimeSlot[]>([]);
  const [templates, setTemplates] = useState<AvailabilityTemplate[]>([]);
  const [showTemplateModal, setShowTemplateModal] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<AvailabilityTemplate | null>(null);

  // Generate time slots for the current week
  const generateTimeSlots = () => {
    const slots: TimeSlot[] = [];
    const startOfWeek = new Date(currentDate);
    startOfWeek.setDate(currentDate.getDate() - currentDate.getDay());
    
    for (let day = 0; day < 7; day++) {
      const currentDay = new Date(startOfWeek);
      currentDay.setDate(startOfWeek.getDate() + day);
      
      // Generate slots from 8 AM to 6 PM
      for (let hour = 8; hour < 18; hour++) {
        for (let minute = 0; minute < 60; minute += 30) {
          const startTime = `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
          const endTime = minute === 30 
            ? `${(hour + 1).toString().padStart(2, '0')}:00`
            : `${hour.toString().padStart(2, '0')}:30`;
          
          slots.push({
            id: `${currentDay.toISOString().split('T')[0]}-${startTime}`,
            startTime,
            endTime,
            duration: 30,
            status: 'available',
            date: currentDay.toISOString().split('T')[0]
          });
        }
      }
    }
    
    setTimeSlots(slots);
  };

  useEffect(() => {
    generateTimeSlots();
  }, [currentDate]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available': return 'bg-green-100 border-green-300 text-green-800';
      case 'booked': return 'bg-blue-100 border-blue-300 text-blue-800';
      case 'blocked': return 'bg-red-100 border-red-300 text-red-800';
      case 'tentative': return 'bg-yellow-100 border-yellow-300 text-yellow-800';
      case 'break': return 'bg-gray-100 border-gray-300 text-gray-800';
      default: return 'bg-gray-100 border-gray-300 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'available': return <CheckCircle className="w-4 h-4" />;
      case 'booked': return <Users className="w-4 h-4" />;
      case 'blocked': return <X className="w-4 h-4" />;
      case 'tentative': return <AlertCircle className="w-4 h-4" />;
      case 'break': return <Clock3 className="w-4 h-4" />;
      default: return <Info className="w-4 h-4" />;
    }
  };

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', { 
      weekday: 'short', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const formatTime = (time: string) => {
    const [hours, minutes] = time.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour;
    return `${displayHour}:${minutes} ${ampm}`;
  };

  const handleSlotClick = (slot: TimeSlot) => {
    setEditingSlot(slot);
    setShowEditModal(true);
  };

  const handleAddSlot = () => {
    setShowAddModal(true);
  };

  const handleDeleteSlots = () => {
    setTimeSlots(prev => prev.filter(slot => !selectedSlots.includes(slot.id)));
    setSelectedSlots([]);
  };

  const handleCopySlots = () => {
    // Implementation for copying slots
    console.log('Copying slots:', selectedSlots);
  };

  const handleTemplateApply = () => {
    if (selectedTemplate) {
      // Apply template to current week
      const newSlots = selectedTemplate.slots.map(slot => ({
        ...slot,
        id: `${currentDate.toISOString().split('T')[0]}-${slot.startTime}`,
        date: currentDate.toISOString().split('T')[0]
      }));
      setTimeSlots(prev => [...prev, ...newSlots]);
      setShowTemplateModal(false);
      setSelectedTemplate(null);
    }
  };

  const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const timeSlotOptions = ['8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', 
                     '12:00', '12:30', '1:00', '1:30', '2:00', '2:30', '3:00', '3:30', 
                     '4:00', '4:30', '5:00', '5:30', '6:00'];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Stethoscope className="w-8 h-8 text-primary-600" />
                <h1 className="text-2xl font-bold text-gray-900">Provider Availability</h1>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
                <Save className="w-4 h-4" />
                <span>Save Changes</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Calendar Views</h2>
              
              <div className="space-y-2 mb-6">
                {[
                  { id: 'month', label: 'Month View', icon: CalendarDays },
                  { id: 'week', label: 'Week View', icon: Calendar },
                  { id: 'day', label: 'Day View', icon: Clock }
                ].map((view) => (
                  <button
                    key={view.id}
                    onClick={() => setCurrentView(view.id as CalendarView)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                      currentView === view.id
                        ? 'bg-primary-100 text-primary-700 border border-primary-300'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <view.icon className="w-5 h-5" />
                    <span className="font-medium">{view.label}</span>
                  </button>
                ))}
              </div>

              <div className="border-t border-gray-200 pt-4">
                <h3 className="text-sm font-semibold text-gray-900 mb-3">Quick Actions</h3>
                <div className="space-y-2">
                  <button
                    onClick={handleAddSlot}
                    className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-green-700 hover:bg-green-50 rounded-lg transition-colors"
                  >
                    <Plus className="w-4 h-4" />
                    <span>Add Availability</span>
                  </button>
                  
                  {selectedSlots.length > 0 && (
                    <>
                      <button
                        onClick={handleDeleteSlots}
                        className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-red-700 hover:bg-red-50 rounded-lg transition-colors"
                      >
                        <Trash2 className="w-4 h-4" />
                        <span>Delete Selected ({selectedSlots.length})</span>
                      </button>
                      
                      <button
                        onClick={handleCopySlots}
                        className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-blue-700 hover:bg-blue-50 rounded-lg transition-colors"
                      >
                        <Copy className="w-4 h-4" />
                        <span>Copy Selected</span>
                      </button>
                    </>
                  )}
                </div>
              </div>

              <div className="border-t border-gray-200 pt-4 mt-4">
                <h3 className="text-sm font-semibold text-gray-900 mb-3">Templates</h3>
                <button
                  onClick={() => setShowTemplateModal(true)}
                  className="w-full flex items-center space-x-2 px-3 py-2 text-sm text-purple-700 hover:bg-purple-50 rounded-lg transition-colors"
                >
                  <Repeat className="w-4 h-4" />
                  <span>Apply Template</span>
                </button>
              </div>
            </div>
          </div>

          {/* Main Calendar Area */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              {/* Calendar Header */}
              <div className="flex items-center justify-between p-4 border-b border-gray-200">
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => {
                      const newDate = new Date(currentDate);
                      newDate.setDate(currentDate.getDate() - 7);
                      setCurrentDate(newDate);
                    }}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    <ChevronLeft className="w-5 h-5" />
                  </button>
                  
                  <h2 className="text-xl font-semibold text-gray-900">
                    {currentDate.toLocaleDateString('en-US', { 
                      month: 'long', 
                      year: 'numeric' 
                    })}
                  </h2>
                  
                  <button
                    onClick={() => {
                      const newDate = new Date(currentDate);
                      newDate.setDate(currentDate.getDate() + 7);
                      setCurrentDate(newDate);
                    }}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    <ChevronRight className="w-5 h-5" />
                  </button>
                </div>
                
                <button
                  onClick={() => setCurrentDate(new Date())}
                  className="px-4 py-2 text-sm font-medium text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                >
                  Today
                </button>
              </div>

              {/* Calendar Grid */}
              <div className="overflow-x-auto">
                <div className="min-w-[800px]">
                  {/* Day Headers */}
                  <div className="grid grid-cols-8 border-b border-gray-200">
                    <div className="p-3"></div>
                    {weekDays.map((day, index) => {
                      const date = new Date(currentDate);
                      date.setDate(currentDate.getDate() - currentDate.getDay() + index);
                      return (
                        <div key={day} className="p-3 text-center">
                          <div className="text-sm font-medium text-gray-900">{day}</div>
                          <div className={`text-lg font-bold ${
                            date.toDateString() === new Date().toDateString() 
                              ? 'text-primary-600' 
                              : 'text-gray-700'
                          }`}>
                            {date.getDate()}
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Time Slots */}
                  <div className="grid grid-cols-8">
                    {timeSlotOptions.map((time) => (
                      <React.Fragment key={time}>
                        <div className="p-2 text-xs text-gray-500 border-r border-gray-200">
                          {formatTime(time)}
                        </div>
                        {weekDays.map((day, dayIndex) => {
                          const date = new Date(currentDate);
                          date.setDate(currentDate.getDate() - currentDate.getDay() + dayIndex);
                          const slotId = `${date.toISOString().split('T')[0]}-${time}`;
                          const slot = timeSlots.find(s => s.id === slotId);
                          
                          return (
                            <div
                              key={`${day}-${time}`}
                              className={`p-1 border-r border-gray-200 border-b border-gray-100 min-h-[40px] ${
                                slot ? 'cursor-pointer' : 'cursor-pointer hover:bg-gray-50'
                              }`}
                              onClick={() => {
                                if (slot) {
                                  handleSlotClick(slot);
                                } else {
                                  // Create new slot
                                  const newSlot: TimeSlot = {
                                    id: slotId,
                                    startTime: time,
                                    endTime: timeSlotOptions[timeSlotOptions.indexOf(time) + 1] || '18:00',
                                    duration: 30,
                                    status: 'available',
                                    date: date.toISOString().split('T')[0]
                                  };
                                  setEditingSlot(newSlot);
                                  setShowEditModal(true);
                                }
                              }}
                            >
                              {slot && (
                                <div className={`p-1 rounded text-xs border ${getStatusColor(slot.status)}`}>
                                  <div className="flex items-center space-x-1">
                                    {getStatusIcon(slot.status)}
                                    <span>{formatTime(slot.startTime)}</span>
                                  </div>
                                  <div className="text-xs opacity-75">
                                    {slot.duration}min
                                  </div>
                                </div>
                              )}
                            </div>
                          );
                        })}
                      </React.Fragment>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Add/Edit Modal */}
      {(showAddModal || showEditModal) && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">
                {showAddModal ? 'Add Availability' : 'Edit Availability'}
              </h3>
              <button
                onClick={() => {
                  setShowAddModal(false);
                  setShowEditModal(false);
                  setEditingSlot(null);
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Date
                  </label>
                  <input
                    type="date"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    value={editingSlot?.date || ''}
                    onChange={(e) => setEditingSlot(prev => prev ? {...prev, date: e.target.value} : null)}
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Start Time
                    </label>
                    <input
                      type="time"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      value={editingSlot?.startTime || ''}
                      onChange={(e) => setEditingSlot(prev => prev ? {...prev, startTime: e.target.value} : null)}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      End Time
                    </label>
                    <input
                      type="time"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      value={editingSlot?.endTime || ''}
                      onChange={(e) => setEditingSlot(prev => prev ? {...prev, endTime: e.target.value} : null)}
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Status
                  </label>
                  <select
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    value={editingSlot?.status || 'available'}
                    onChange={(e) => setEditingSlot(prev => prev ? {...prev, status: e.target.value as any} : null)}
                  >
                    <option value="available">Available</option>
                    <option value="booked">Booked</option>
                    <option value="blocked">Blocked</option>
                    <option value="tentative">Tentative</option>
                    <option value="break">Break</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Notes (Optional)
                  </label>
                  <textarea
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    rows={3}
                    value={editingSlot?.notes || ''}
                    onChange={(e) => setEditingSlot(prev => prev ? {...prev, notes: e.target.value} : null)}
                    placeholder="Add any notes about this time slot..."
                  />
                </div>
              </div>
            </div>
            
            <div className="flex items-center justify-end space-x-3 p-6 border-t border-gray-200">
              <button
                onClick={() => {
                  setShowAddModal(false);
                  setShowEditModal(false);
                  setEditingSlot(null);
                }}
                className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (editingSlot) {
                    if (showAddModal) {
                      setTimeSlots(prev => [...prev, editingSlot]);
                    } else {
                      setTimeSlots(prev => prev.map(slot => 
                        slot.id === editingSlot.id ? editingSlot : slot
                      ));
                    }
                  }
                  setShowAddModal(false);
                  setShowEditModal(false);
                  setEditingSlot(null);
                }}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                {showAddModal ? 'Add Slot' : 'Save Changes'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Template Modal */}
      {showTemplateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Apply Template</h3>
              <button
                onClick={() => setShowTemplateModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select Template
                  </label>
                  <select
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    onChange={(e) => {
                      const template = templates.find(t => t.id === e.target.value);
                      setSelectedTemplate(template || null);
                    }}
                  >
                    <option value="">Choose a template...</option>
                    {templates.map(template => (
                      <option key={template.id} value={template.id}>
                        {template.name}
                      </option>
                    ))}
                  </select>
                </div>
                
                {selectedTemplate && (
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <h4 className="font-medium text-gray-900 mb-2">{selectedTemplate.name}</h4>
                    <div className="text-sm text-gray-600">
                      {selectedTemplate.slots.length} time slots
                    </div>
                  </div>
                )}
              </div>
            </div>
            
            <div className="flex items-center justify-end space-x-3 p-6 border-t border-gray-200">
              <button
                onClick={() => setShowTemplateModal(false)}
                className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
              >
                Cancel
              </button>
              <button
                onClick={handleTemplateApply}
                disabled={!selectedTemplate}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Apply Template
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProviderAvailability; 