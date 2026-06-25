# AWS Deployment Guide — Employee Management System

## Architecture

```
Browser
    │
    ▼
S3 + CloudFront          ← Frontend (HTML/CSS/JS)
    │
    ▼
EC2 (Flask API)          ← Backend (Port 5001)
    │
    ▼
RDS SQL Server           ← Database (Port 1433)
```

---

## Prerequisites

- AWS Account
- AWS CLI installed and configured
- Key pair (.pem file) for EC2 SSH access

---

## Step 1 — Launch EC2 (Flask Backend)

1. Go to **EC2 → Launch Instance**
2. Settings:
   - Name: `employee-management-backend`
   - AMI: **Ubuntu 22.04 LTS**
   - Instance type: **t2.micro** (free tier)
   - Key pair: create or select existing
3. Security Group — open inbound ports:

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 22 | TCP | Your IP | SSH |
| 5001 | TCP | 0.0.0.0/0 | Flask API |

4. Launch and note the **Public IP**

---

## Step 2 — Set Up EC2

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>

# Install dependencies
sudo apt update && sudo apt install python3-pip git -y

# Clone repo
git clone https://github.com/nagendraclouddevops/Employee-Management-System.git
cd Employee-Management-System/backend

# Install Python packages
pip3 install -r requirements.txt
```

---

## Step 3 — Create RDS SQL Server

1. Go to **RDS → Create Database**
2. Settings:
   - Engine: **Microsoft SQL Server**
   - Edition: **Express** (lowest cost)
   - Instance: **db.t3.micro**
   - Master username: `admin`
   - Master password: `YourPassword@123`
   - Public access: **Yes** (or place in same VPC as EC2)
3. Note the **RDS Endpoint**

### Create Tables on RDS

From the EC2 instance:

```bash
# Install sqlcmd
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list \
  | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt update && sudo ACCEPT_EULA=Y apt install mssql-tools18 unixodbc-dev -y

# Create database
/opt/mssql-tools18/bin/sqlcmd -S <RDS-ENDPOINT> -U admin -P 'YourPassword@123' -No \
  -Q "CREATE DATABASE EmployeeDB;"

# Create tables
/opt/mssql-tools18/bin/sqlcmd -S <RDS-ENDPOINT> -U admin -P 'YourPassword@123' -No \
  -d EmployeeDB -Q "
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

## Step 4 — Update Backend Config

Edit `backend/config.py` on EC2:

```python
DB_CONFIG = {
    "server": "<RDS-ENDPOINT>",
    "port": 1433,
    "user": "admin",
    "password": "YourPassword@123",
    "database": "EmployeeDB",
}
```

---

## Step 5 — Run Flask (Persistent)

```bash
sudo apt install screen -y

screen -S flask
cd ~/Employee-Management-System/backend
python3 app.py

# Detach: Ctrl+A then D
# Reattach later: screen -r flask
```

Flask is now running at `http://<EC2-PUBLIC-IP>:5001`

---

## Step 6 — Update Frontend URLs

In `Frontend/script.js` and `Frontend/login.js`, replace `localhost:5001` with your EC2 public IP:

```js
fetch("http://<EC2-PUBLIC-IP>:5001/employees")
fetch("http://<EC2-PUBLIC-IP>:5001/login", { ... })
fetch("http://<EC2-PUBLIC-IP>:5001/add", { ... })
```

---

## Step 7 — Host Frontend on S3

1. Go to **S3 → Create Bucket**
   - Name: `employee-management-frontend`
   - Region: same as EC2
   - Uncheck **Block all public access**

2. Upload these files from `Frontend/`:
   - `index.html`
   - `login.html`
   - `script.js`
   - `login.js`
   - `style.css`

3. Go to **Properties → Static Website Hosting → Enable**
   - Index document: `login.html`

4. Go to **Permissions → Bucket Policy** and paste:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::employee-management-frontend/*"
    }
  ]
}
```

5. Your app is live at the S3 website URL shown under **Static website hosting**

---

## Cost Estimate

| Service | Free Tier | Paid |
|---|---|---|
| EC2 t2.micro | 750 hrs/month (12 months) | ~$8/month |
| RDS SQL Server Express | Not included | ~$25/month |
| S3 | 5 GB storage free | Cents/month |

> **Save cost:** Skip RDS — run SQL Server in Docker on the same EC2 instance using `docker run mcr.microsoft.com/mssql/server:2022-latest`

---

## Verify Deployment

```bash
# Test API
curl http://<EC2-PUBLIC-IP>:5001/employees

# Test login
curl -X POST http://<EC2-PUBLIC-IP>:5001/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Open the S3 URL in your browser — you should see the login page.
