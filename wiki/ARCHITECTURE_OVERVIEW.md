# 🏗️ Architecture Overview - Yourl.Cloud Inc.

## 🎯 System Architecture

### **Core Components**

#### **1. Application Layer**
- **Framework**: Python Flask 3.0.2
- **WSGI Server**: Gunicorn (Unix) / Waitress (Windows)
- **Runtime**: Google Cloud Run
- **Language**: Python 3.9+

#### **2. Data Layer**
- **Primary Storage**: Google Cloud SQL (PostgreSQL)
- **Secret Management**: Google Secret Manager
- **Caching**: In-memory (future: Redis)
- **Backup**: Automated Cloud SQL backups

#### **3. Security Layer**
- **Authentication**: Marketing code-based
- **Authorization**: Role-based access control
- **Encryption**: TLS 1.3, data at rest
- **Audit**: Complete access logging

#### **4. Infrastructure Layer**
- **Platform**: Google Cloud Platform
- **Region**: us-west1
- **Domain**: yourl.cloud
- **CDN**: Cloud CDN (future)

## 🔄 Data Flow Architecture

### **Request Flow**
```
User Request → Cloud Load Balancer → Cloud Run → Flask App → Database/Secrets
                ↓
            X-Forwarded Headers → Domain Detection → Response
```

### **Authentication Flow**
```
Landing Page → Marketing Code Input → Validation → Session Creation → Access Granted
                ↓
            Database Logging → Audit Trail → Analytics
```

### **Data Storage Flow**
```
Application → Secret Manager (Credentials) → Cloud SQL → Encrypted Storage
                ↓
            Backup → Cross-region Replication → Disaster Recovery
```

## 🏛️ Component Architecture

### **Frontend Components**
- **Landing Page**: Marketing code entry, visitor tracking
- **Data Stream**: Vertical scrolling, wiki interpretations
- **API Interface**: Visual inspection, device detection
- **Status Dashboard**: Health checks, service status

### **Backend Services**
- **Authentication Service**: Code validation, session management
- **Data Service**: Database operations, caching
- **Logging Service**: Audit trails, analytics
- **Notification Service**: Email alerts, status updates

### **Infrastructure Services**
- **Load Balancer**: Traffic distribution, SSL termination
- **CDN**: Static content delivery, caching
- **Monitoring**: Health checks, performance metrics
- **Backup**: Automated backups, disaster recovery

## 🔐 Security Architecture

### **Authentication & Authorization**
- **Multi-factor**: Marketing codes + session tokens
- **Role-based**: Visitor, Authenticated, Admin
- **Time-based**: Session expiration, token rotation
- **Device-aware**: Device type detection, access control

### **Data Protection**
- **Encryption**: TLS 1.3 in transit, AES-256 at rest
- **Secrets**: Secret Manager for credentials
- **Audit**: Complete access logging, audit trails
- **Compliance**: GDPR, SOC 2, ISO 27001 ready

### **Network Security**
- **Firewall**: Cloud Armor, VPC firewall rules
- **DDoS Protection**: Cloud Armor, rate limiting
- **SSL/TLS**: Automatic certificate management
- **VPN**: Cloud VPN for admin access

## 📊 Data Architecture

### **Database Schema**
```sql
-- Core Tables
marketing_codes          -- Current/next codes
marketing_code_history   -- Code rotation history
visitor_tracking         -- Visitor analytics
code_usage_logs         -- Usage analytics
authorization_records    -- Access control
landing_page_versions    -- Page version tracking

-- Audit Tables
audit_logs              -- System audit trail
access_logs             -- Access patterns
error_logs              -- Error tracking
```

### **Data Relationships**
```
Visitor → Visits → Codes → Usage → Analytics
  ↓
Tracking → History → Patterns → Insights
```

## 🚀 Performance Architecture

### **Scaling Strategy**
- **Horizontal**: Cloud Run auto-scaling
- **Vertical**: Resource optimization
- **Caching**: Multi-layer caching strategy
- **CDN**: Global content delivery

### **Monitoring & Alerting**
- **Metrics**: Response time, throughput, errors
- **Logging**: Structured logging, log aggregation
- **Alerting**: PagerDuty integration, email alerts
- **Dashboard**: Real-time monitoring, historical trends

## 🔄 Deployment Architecture

### **CI/CD Pipeline**
```
GitHub → Cloud Build → Container Registry → Cloud Run → Production
  ↓
Testing → Security Scan → Deployment → Health Check
```

### **Environment Strategy**
- **Development**: Local development, testing
- **Staging**: Pre-production validation
- **Production**: Live environment, monitoring

## 🌐 Network Architecture

### **Domain Structure**
- **Primary**: yourl.cloud
- **API**: api.yourl.cloud (future)
- **Admin**: admin.yourl.cloud (future)
- **CDN**: cdn.yourl.cloud (future)

### **Load Balancing**
- **Global**: Cloud Load Balancer
- **Regional**: Cloud Run load balancing
- **Health Checks**: Automatic health monitoring
- **Failover**: Cross-region failover

## 📈 Scalability Architecture

### **Auto-scaling**
- **CPU-based**: Automatic scaling based on CPU usage
- **Memory-based**: Memory utilization scaling
- **Request-based**: Request rate scaling
- **Custom metrics**: Business metrics scaling

### **Resource Management**
- **Resource limits**: CPU, memory, storage limits
- **Cost optimization**: Resource utilization monitoring
- **Performance tuning**: Database optimization
- **Capacity planning**: Growth forecasting

## 🔍 Observability Architecture

### **Logging Strategy**
- **Application logs**: Structured JSON logging
- **Access logs**: Request/response logging
- **Error logs**: Error tracking, debugging
- **Audit logs**: Security audit trails

### **Monitoring Strategy**
- **Infrastructure**: Cloud monitoring, alerting
- **Application**: Custom metrics, performance
- **Business**: User analytics, conversion tracking
- **Security**: Security monitoring, threat detection

## 🛡️ Disaster Recovery

### **Backup Strategy**
- **Database**: Automated daily backups
- **Configuration**: Infrastructure as code
- **Secrets**: Secret Manager versioning
- **Documentation**: Wiki version control

### **Recovery Strategy**
- **RTO**: 4 hours recovery time objective
- **RPO**: 1 hour recovery point objective
- **Failover**: Cross-region failover
- **Testing**: Regular disaster recovery testing

## 🎯 Future Architecture

### **Planned Enhancements**
- **Microservices**: Service decomposition
- **Event-driven**: Event sourcing, CQRS
- **AI/ML**: Predictive analytics, automation
- **Blockchain**: Decentralized identity, smart contracts

### **Technology Evolution**
- **Kubernetes**: Container orchestration
- **Service Mesh**: Istio, traffic management
- **Serverless**: Cloud Functions, Eventarc
- **Edge Computing**: Cloud CDN, edge functions

---

*Last Updated: 2025-08-08 | Architecture Version: 2.0 | Status: Production Ready*
