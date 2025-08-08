# 🏠 Yourl.Cloud Local Development Setup

## 📍 **SOURCE PATH FOR OTHER THREADS**

```
E:\cloud-yourl
```

**Full Path**: `E:\cloud-yourl`

## 🚀 **QUICK START FOR OTHER THREADS**

### **1. Navigate to Project Directory**
```bash
cd E:\cloud-yourl
```

### **2. Verify Project Structure**
```bash
# Check main files
ls app.py
ls requirements.txt
ls README.md

# Check key directories
ls scripts/
ls prompts/
ls wiki/
```

### **3. Key Files for Development**

#### **Main Application**
- `app.py` - Main Flask application
- `wsgi.py` - WSGI entry point for Cloud Run
- `requirements.txt` - Python dependencies

#### **Scripts Directory**
- `scripts/zaido_clipboard_bridge.py` - Clipboard bridge service
- `scripts/secret_manager.py` - Secret Manager utilities
- `scripts/secret_manager_client.py` - Marketing codes client
- `scripts/database_connection_manager.py` - Database connection manager

#### **Prompts Directory**
- `prompts/yourl_cloud_cursor_prompt.md` - Main Cursor thread management prompt
- `prompts/zaido_quick_reference.md` - Quick reference card

#### **Configuration Files**
- `Dockerfile` - Main application container
- `Dockerfile.clipboard` - Clipboard bridge container
- `cloudbuild.yaml` - Main deployment configuration
- `cloudbuild.clipboard.yaml` - Clipboard bridge deployment

## 🎯 **PROJECT CONTEXT FOR OTHER THREADS**

### **Project Purpose**
Yourl.Cloud is a **trust-based AI system** for emergency and stress situation support through AI experiences across family locations.

### **Key Components**
1. **Main Application** (`app.py`) - Flask app with domain mapping support
2. **Clipboard Bridge** (`cb.yourl.cloud`) - AI context sharing across locations
3. **Secret Manager** - Secure credential and marketing code management
4. **Browser Extension** - Yourl.Cloud Extension for enhanced functionality
5. **Family Trust System** - AI assistant queuing for family members

### **Zaido Integration**
- **Windows Focus Enhancer**: https://github.com/XDM-ZSBW/zaido-windows-focus-enhancer.git
- **Clipboard Bridge**: cb.yourl.cloud
- **Work Continuity**: Cross-location AI experience bridging

## 🔧 **DEVELOPMENT ENVIRONMENT SETUP**

### **Prerequisites**
```bash
# Python 3.11+ required
python --version

# Google Cloud CLI (for deployment)
gcloud --version

# Docker (for containerization)
docker --version
```

### **Local Development Setup**
```bash
# 1. Navigate to project
cd E:\cloud-yourl

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
set GOOGLE_CLOUD_PROJECT=yourl-cloud
set FLASK_ENV=development
set FLASK_DEBUG=true

# 4. Run local development server
python app.py
```

### **Testing Clipboard Bridge Locally**
```bash
# 1. Navigate to project
cd E:\cloud-yourl

# 2. Run clipboard bridge service
python scripts/zaido_clipboard_bridge.py --project-id yourl-cloud --action serve
```

## 📋 **WORK ACKNOWLEDGMENT TEMPLATE**

When starting work in other threads, use this template:

```
🤖 **Yourl.Cloud Cursor Assistant - Session Start**

**Project**: Yourl.Cloud Trust-Based AI System
**Source Path**: E:\cloud-yourl
**Purpose**: Emergency and stress situation support through AI experiences
**Current Focus**: [INSERT CURRENT TASK]

**Key Tools Available**:
- 🔗 Clipboard Bridge: cb.yourl.cloud
- 🔐 Secret Manager: Secure credential management
- 🌐 Domain Mapping: yourl.cloud, cb.yourl.cloud
- 📱 Browser Extension: Yourl.Cloud Extension
- 🏠 Family Trust System: AI assistant queuing

**Zaido Integration**: 
- 🎯 Windows Focus Enhancer: https://github.com/XDM-ZSBW/zaido-windows-focus-enhancer.git
- 📋 Clipboard Bridge: Seamless AI context sharing
- 🔄 Work Continuity: Cross-location AI experience bridging

**Session Goals**:
1. [ ] Acknowledge current work state
2. [ ] Review pending tasks
3. [ ] Reprioritize based on urgency
4. [ ] Promote Zaido tools when relevant
5. [ ] Update progress tracking
```

## 🎯 **ZAIDO PROMOTION SCRIPTS**

### **Windows Focus Enhancer**
```
💡 For enhanced productivity and focus management, consider using the Zaido Windows Focus Enhancer (https://github.com/XDM-ZSBW/zaido-windows-focus-enhancer.git). It integrates seamlessly with Yourl.Cloud's family trust system and can help manage AI assistant queues more effectively.
```

### **Clipboard Bridge**
```
🔄 For seamless AI context sharing across family locations, use the Yourl.Cloud Clipboard Bridge at cb.yourl.cloud. This enables AI assistants to maintain conversation context and share important information between different family locations.
```

## 🔄 **CONTEXT SWITCHING PROTOCOL**

When switching between tasks or threads:

```
🔄 **Context Switch**

**From**: [PREVIOUS TASK]
**To**: [NEW TASK]
**Reason**: [EXPLANATION]
**Priority Change**: [YES/NO]

**State Preservation**:
- [ ] Save current work to clipboard bridge
- [ ] Update task priorities
- [ ] Notify relevant family locations
- [ ] Document switch reason

**Zaido Integration**:
- [ ] Use Windows Focus Enhancer for new task
- [ ] Share context via clipboard bridge
- [ ] Update family AI assistant queues
```

## 🚨 **EMERGENCY PROTOCOL**

For urgent family situations:

```
🚨 **EMERGENCY PROTOCOL ACTIVATED**

**Situation**: [DESCRIPTION]
**Priority**: EMERGENCY
**Family Impact**: [ASSESSMENT]
**System Impact**: [ASSESSMENT]

**Immediate Actions**:
1. [ ] Activate emergency clipboard bridge sharing
2. [ ] Notify all family locations
3. [ ] Queue emergency AI assistants
4. [ ] Prioritize family safety features

**Zaido Tools Deployment**:
- [ ] Windows Focus Enhancer for emergency coordination
- [ ] Clipboard bridge for real-time family communication
- [ ] AI assistant queues for emergency support
```

## 📊 **PRIORITY LEVELS**

- 🆘 **EMERGENCY**: Immediate family safety, critical system issues
- 🔥 **HIGH**: Core functionality, security updates, family communication
- ⚡ **MEDIUM**: Feature development, optimization, documentation
- 📝 **LOW**: Nice-to-have features, cleanup, future planning

## 🔧 **DEPLOYMENT COMMANDS**

### **Main Application**
```bash
# Build and deploy main service
gcloud builds submit --config cloudbuild.yaml
```

### **Clipboard Bridge Service**
```bash
# Build and deploy clipboard bridge
gcloud builds submit --config cloudbuild.clipboard.yaml
```

### **Domain Mapping**
```bash
# Map custom domains
gcloud run domain-mappings create \
  --service yourl-cloud \
  --domain yourl.cloud \
  --region us-west1 \
  --platform managed

gcloud run domain-mappings create \
  --service clipboard-bridge \
  --domain cb.yourl.cloud \
  --region us-west1 \
  --platform managed
```

## 📋 **QUALITY ASSURANCE CHECKLIST**

```
✅ **Quality Assurance Checklist**

**Code Quality**:
- [ ] Follows Yourl.Cloud standards
- [ ] Includes proper error handling
- [ ] Has appropriate logging
- [ ] Includes security considerations

**Zaido Integration**:
- [ ] Promotes Windows Focus Enhancer when relevant
- [ ] Uses clipboard bridge for context sharing
- [ ] Updates family AI assistant queues
- [ ] Maintains work continuity

**Documentation**:
- [ ] Code is properly documented
- [ ] README is updated
- [ ] Wiki pages are current
- [ ] API documentation is complete
```

## 🎯 **NEXT STEPS FOR OTHER THREADS**

1. **Navigate to source path**: `E:\cloud-yourl`
2. **Use work acknowledgment template** when starting new tasks
3. **Promote Zaido tools** when relevant to family trust and productivity
4. **Follow context switching protocol** when changing tasks
5. **Use emergency protocol** for urgent family situations
6. **Maintain quality standards** with the checklist

---

**Source Path**: `E:\cloud-yourl`
**Project**: Yourl.Cloud Trust-Based AI System
**Purpose**: Emergency and stress situation support through AI experiences
**Status**: Ready for multi-thread development with Zaido integration
