### Deploy application using AWS EC2, Docker, Nginx, securely using SSL/TLS certificate & Cloudflare | End-to-end automated CI/CD setup with Github Actions.

**Project Objective :** _This project demonstrates a real-world approach to securely deploying a web application on AWS EC2 & automating CI/CD using Github Actions._
_The application is exposed through Nginx as a reverse proxy and load balancer, mapped to a custom domain using GoDaddy, and secured with Cloudflare for HTTPS, DNS protection, and traffic filtering. The setup focuses on security, scalability, and production-grade access patterns commonly used in real deployments._

Key Learnings :

* Real-world CI/CD pipeline design
* Docker-based deployment
* Debugging authentication & deployment issues
* Secrets handling in CI/CD pipeline
* Hosting application using SSL/TLS with Cloudflare

Technologies/Tools used :

* AWS : Networking, Compute, Firewall, IAM policies, roles, ECR
* Github Actions for CI/CD automation
* Docker Containers, docker-compose
* Let's encrypt : SSL/TLS certificate (free)
* Cloudflare (free)
* Nginx as Reverse Proxy
* GoDaddy domain name (paid)

Final Outcome :

* Application code is Tested & Verfied before deployment
* Fully automated deployment
* Zero manual Docker/SSH commands
* Web application accessible through secure HTTPS protocol