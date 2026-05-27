# 🕉️ Spiritual Progress Tracking System

## Overview

The Daiva Anughara website now includes a comprehensive **Spiritual Progress Tracking System** that allows administrators to manage and track users' progression through the sacred stages of spiritual practice.

## 📊 System Features

### **6-Stage Progression Path**
1. **Mandala 1** 🕉️ - Foundation (Auto-granted to all users)
2. **Mandala 2** 🌟 - Advancement (Admin approval required)
3. **Mandala 3** ✨ - Mastery (Admin approval required)
4. **Rudraksha 8 Mukhi** 📿 - Purification (Admin approval required)
5. **Rudraksha 11 Mukhi** 🔮 - Protection (Admin approval required)
6. **Rudraksha 14 Mukhi** 💎 - Ultimate Mastery (Admin approval required)

### **Sequential Progression**
- Users must complete one stage before starting the next
- Admin manually approves each stage transition
- Automatic access granting to next stage upon completion

### **Progress Tracking**
- **Completion dates** for each stage
- **Duration tracking** (days spent on each stage)
- **Current stage detection**
- **Next required stage identification**

## 🔧 Technical Implementation

### **Database Schema Updates**

New fields added to the `User` model:

#### Access Control Fields
```python
rudraksha_8_mukhi_access = db.Column(db.Boolean, default=False)
rudraksha_11_mukhi_access = db.Column(db.Boolean, default=False)
rudraksha_14_mukhi_access = db.Column(db.Boolean, default=False)
```

#### Completion Tracking
```python
mandala_1_completed_at = db.Column(db.DateTime, nullable=True)
mandala_2_completed_at = db.Column(db.DateTime, nullable=True)
mandala_3_completed_at = db.Column(db.DateTime, nullable=True)
rudraksha_8_mukhi_completed_at = db.Column(db.DateTime, nullable=True)
rudraksha_11_mukhi_completed_at = db.Column(db.DateTime, nullable=True)
rudraksha_14_mukhi_completed_at = db.Column(db.DateTime, nullable=True)
```

#### Duration Tracking
```python
mandala_1_started_at = db.Column(db.DateTime, nullable=True)
mandala_2_started_at = db.Column(db.DateTime, nullable=True)
mandala_3_started_at = db.Column(db.DateTime, nullable=True)
rudraksha_8_mukhi_started_at = db.Column(db.DateTime, nullable=True)
rudraksha_11_mukhi_started_at = db.Column(db.DateTime, nullable=True)
rudraksha_14_mukhi_started_at = db.Column(db.DateTime, nullable=True)
```

### **New User Model Methods**

#### Core Methods
- `get_current_stage()` - Returns current stage (1-6)
- `get_next_required_stage()` - Returns next stage to complete
- `has_mandala_access(stage_number)` - Checks access to specific stage
- `is_stage_completed(stage_number)` - Checks if stage is completed

#### Stage Management
- `complete_stage(stage_number)` - Marks stage as completed
- `start_stage(stage_number)` - Marks stage as started
- `get_stage_duration_days(stage_number)` - Calculates duration in days
- `get_stage_info(stage_number)` - Returns comprehensive stage information

## 🎛️ Admin Interface

### **User Detail Page Enhancements**

#### Vertical Progress Bar
- **Visual progress tracking** with spiritual icons
- **Color-coded stages**: Completed (red), Current (gold), Locked (gray)
- **Completion dates** displayed for finished stages
- **Duration tracking** for each stage
- **Current status** with next required stage

#### Stage Management Controls
- **Toggle switches** for each stage access (Mandala 2-3, Rudraksha stages)
- **Complete stage buttons** for active stages
- **Reset stage buttons** for completed stages
- **Sequential approval** workflow

### **Stage Approval Process**

1. **Admin grants access** to next stage via toggle switch
2. **System automatically starts** the stage (sets start date)
3. **Admin completes stage** when user finishes requirements
4. **System automatically grants** access to subsequent stage
5. **Process continues** sequentially through all 6 stages

## 👤 User Experience

### **Padati Page Updates**

#### Enhanced Progress Section
- **Personal progress bar** showing spiritual journey
- **Stage-specific information** with completion dates
- **Duration tracking** for completed stages
- **Next stage guidance** with approval status

#### Dynamic Tab Interface
- **Access-controlled tabs** (only show available stages)
- **Smart tab activation** (first available tab becomes active)
- **No-access handling** (graceful message for pending users)

### **Access Information**
- **Updated status display** for all 6 stages
- **Admin approval status** for locked stages
- **Progressive access** messaging

## 🚀 Getting Started

### **1. Database Migration**

Run the migration script to add new fields:

```bash
python database_migration.py
```

**Note:** If columns already exist, the script will show warnings but complete successfully.

### **2. Admin Setup**

1. **Login as admin** and go to User Management
2. **Edit user details** to see the new progress interface
3. **Grant stage access** using the toggle switches
4. **Complete stages** as users finish their practice

### **3. User Experience**

1. **Users see progress** on the Padati page
2. **Access-controlled content** based on current stage
3. **Clear progression path** with visual indicators

## 📱 Responsive Design

### **Mobile Compatibility**
- **Responsive progress bar** adapts to mobile screens
- **Touch-friendly controls** for admin interface
- **Optimized layout** for small screens

### **Accessibility**
- **Screen reader support** with proper ARIA labels
- **Keyboard navigation** for all controls
- **High contrast** color scheme for visibility

## 🔒 Security & Permissions

### **Admin-Only Features**
- Stage completion and reset functionality
- Access control management
- Progress tracking and reporting

### **User Privacy**
- Progress visible only to user and admin
- Personal spiritual journey tracking
- Secure stage management

## 🧪 Testing

Run the test script to verify functionality:

```bash
python test_stage_system.py
```

This will test all stage methods and ensure the system works correctly.

## 📋 API Endpoints

### **Admin Routes**
- `POST /admin/user/<id>/stage-access` - Update stage access
- `POST /admin/user/<id>/complete-stage` - Complete a stage
- `POST /admin/user/<id>/reset-stage` - Reset stage and subsequent stages

## 🎨 Visual Design

### **Spiritual Theme Integration**
- **Sacred color palette** (reds, golds, spiritual colors)
- **Om symbols and spiritual icons** for each stage
- **Consistent styling** with existing application theme
- **Smooth animations** and transitions

### **Progress Visualization**
- **Vertical flow** representing spiritual ascent
- **Color-coded completion** status
- **Date and duration** information display
- **Intuitive visual hierarchy**

## 📈 Future Enhancements

### **Potential Features**
- **Stage requirements documentation**
- **Progress analytics and reporting**
- **Email notifications** for stage transitions
- **Spiritual milestone celebrations**
- **Integration with sadhana tracking**

## 🐛 Troubleshooting

### **Common Issues**
1. **Migration fails**: Columns may already exist (this is normal)
2. **Stage methods return None**: Check database schema
3. **Access not updating**: Verify admin permissions
4. **Progress not displaying**: Check user authentication

### **Debug Commands**
```python
# Test stage methods
user = User.query.get(user_id)
print(user.get_current_stage())
print(user.get_next_required_stage())
print(user.get_stage_info(1))
```

---

**🕉️ May this system help guide seekers on their sacred spiritual journey with clarity and divine grace.**
