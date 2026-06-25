# Azure Deployment Guide — Employee Management System

## Architecture

```
Browser
    │
    ▼
Azure Blob Storage       ← Frontend (HTML/CSS/JS)
    │
    ▼
Azure App Service        ← Backend (Flask API)
    │
    ▼
Azure SQL Database       ← Database (SQL Server)
```

---

## Prerequisites

- Azure Account
- Azure CLI installed → `az login`
- Python 3.12+

---

## Step 1 — Create a Resource Group

```bash
az group create \
  --name employee-management-rg \
  --location eastus
```

---

## Step 2 — Create Azure SQL Database

```bash
# Create SQL Server
az sql server create \
  --name employee-sql-server \
  --resource-group employee-management-rg \
  --location eastus \
  --admin-user sqladmin \
  --admin-password YourPassword@123

# Allow Azure services to access SQL Server
az sql server firewall-rule create \
  --resource-group employee-management-rg \
  --server employee-sql-server \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Create database
az sql db create \
  --resource-group employee-management-rg \
  --server employee-sql-server \
  --name EmployeeDB \
  --service-objective Basic
```

### Get the Connection String

```bash
az sql db show-connection-string \
  --server employee-sql-server \
  --name EmployeeDB \
  --client ado.net
```

Note the server hostname — it will look like:
`employee-sql-server.database.windows.net`

### Create Tables

Connect using Azure Cloud Shell or sqlcmd:

```bash
sqlcmd -S employee-sql-server.database.windows.net \
  -U sqladmin -P 'YourPassword@123' -d EmployeeDB \
  -Q "
CREATE TABLE Employees (
    Id INT IDENTITY PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Department VARCHAR(100),
    Salary DECIMAL(10,2)
);
CREATE TABLE Users (
    Id INT IDENTITY PRIMARY KEY,
    Username VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(256) NOT NULL
);"
```

---

## Step 3 — Update Backend Config

Edit `backend/config.py`:

```python
DB_CONFIG = {
    "server": "employee-sql-server.database.windows.net",
    "port": 1433,
    "user": "sqladmin",
    "password": "YourPassword@123",
    "database": "EmployeeDB",
}
```

---

## Step 4 — Deploy Flask Backend to Azure App Service

### Create App Service Plan

```bash
az appservice plan create \
  --name employee-app-plan \
  --resource-group employee-management-rg \
  --sku B1 \
  --is-linux
```

### Create Web App

```bash
az webapp create \
  --resource-group employee-management-rg \
  --plan employee-app-plan \
  --name employee-management-api \
  --runtime "PYTHON:3.12"
```

### Add Startup Command

```bash
az webapp config set \
  --resource-group employee-management-rg \
  --name employee-management-api \
  --startup-file "cd backend && pip install -r requirements.txt && python app.py"
```

### Deploy Code via GitHub

```bash
az webapp deployment source config \
  --name employee-management-api \
  --resource-group employee-management-rg \
  --repo-url https://github.com/nagendraclouddevops/Employee-Management-System \
  --branch main \
  --manual-integration
```

Your Flask API will be at:
`https://employee-management-api.azurewebsites.net`

---

## Step 5 — Update Frontend URLs

In `Frontend/script.js` and `Frontend/login.js`, replace `localhost:5001` with your App Service URL:

```js
fetch("https://employee-management-api.azurewebsites.net/employees")
fetch("https://employee-management-api.azurewebsites.net/login", { ... })
fetch("https://employee-management-api.azurewebsites.net/add", { ... })
```

---

## Step 6 — Host Frontend on Azure Blob Storage

### Create Storage Account

```bash
az storage account create \
  --name employeefrontendstorage \
  --resource-group employee-management-rg \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2
```

### Enable Static Website Hosting

```bash
az storage blob service-properties update \
  --account-name employeefrontendstorage \
  --static-website \
  --index-document login.html
```

### Upload Frontend Files

```bash
az storage blob upload-batch \
  --account-name employeefrontendstorage \
  --source ./Frontend \
  --destination '$web'
```

### Get the Website URL

```bash
az storage account show \
  --name employeefrontendstorage \
  --resource-group employee-management-rg \
  --query "primaryEndpoints.web" \
  --output tsv
```

Open that URL in your browser — you will see the login page.

---

## Step 7 — (Optional) Add Custom Domain via Azure CDN

```bash
# Create CDN profile
az cdn profile create \
  --name employee-cdn \
  --resource-group employee-management-rg \
  --sku Standard_Microsoft

# Create CDN endpoint pointing to blob storage
az cdn endpoint create \
  --name employee-frontend-cdn \
  --profile-name employee-cdn \
  --resource-group employee-management-rg \
  --origin employeefrontendstorage.z13.web.core.windows.net
```

---

## Cost Estimate

| Service | Free Tier | Paid |
|---|---|---|
| App Service B1 | 30 days free trial | ~$13/month |
| Azure SQL Basic | Not free | ~$5/month |
| Blob Storage | 5 GB free (12 months) | Cents/month |
| CDN | 15 GB free (12 months) | Cents/month |

---

## Verify Deployment

```bash
# Test API
curl https://employee-management-api.azurewebsites.net/employees

# Test login
curl -X POST https://employee-management-api.azurewebsites.net/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Open the Blob Storage website URL in your browser.
