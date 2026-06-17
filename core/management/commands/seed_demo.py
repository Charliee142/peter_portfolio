"""
Seed command — populates the database with Peter Charles cybersecurity portfolio demo data.
Run: python manage.py seed_demo
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

from core.models import SiteSettings, Skill, Experience, Education, Certification
from projects.models import Project, ProjectCategory, Technology, ProjectMetric
from blog.models import Post, BlogCategory
from services.models import Service
from training.models import TrainingProgram
from testimonials.models import Testimonial


class Command(BaseCommand):
    help = "Seed the database with cybersecurity portfolio demo data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding cybersecurity portfolio data...")

        # ─── Site Settings ───────────────────────────────────────
        s, _ = SiteSettings.objects.get_or_create(id=1)
        s.site_name = "Peter Charles | Cybersecurity Engineer & Django Developer"
        s.tagline   = "Cybersecurity Engineer & Django Developer"
        s.about_short = "Building secure digital solutions with Python, Django, and cybersecurity expertise."
        s.about_full = (
            "I am a Cybersecurity Engineer and Django Developer with over 5 years of experience "
            "building secure web applications, conducting cybersecurity research, performing OSINT "
            "investigations, and training the next generation of security professionals.\n\n"
            "Based in Abuja, Nigeria, I work with businesses, startups, and NGOs to develop "
            "secure, scalable digital solutions. My approach is security-first: every application "
            "I build is hardened against the OWASP Top 10, properly tested, and deployed with "
            "production-grade security configurations.\n\n"
            "As an Ethical Hacking Instructor, I have trained 200+ students in penetration testing, "
            "OSINT, and secure development practices."
        )
        s.email = "peter@petercharles.dev"
        s.phone = "+234 901 234 5678"
        s.location = "Abuja, FCT, Nigeria"
        s.linkedin_url = "https://linkedin.com/in/petercharles"
        s.github_url   = "https://github.com/petercharles"
        s.twitter_url  = "https://twitter.com/petercharlesdev"
        s.years_experience = 5
        s.projects_completed = 35
        s.clients_served = 22
        s.certifications_count = 10
        s.students_trained = 200
        s.save()
        self.stdout.write("  ✓ Site settings")

        # ─── Skills ──────────────────────────────────────────────
        skills_data = [
            ("Python",              "python",       92, "fab fa-python",        True),
            ("Django / DRF",        "django",       88, "fas fa-server",        True),
            ("PostgreSQL / SQL",    "django",       85, "fas fa-database",      True),
            ("HTML / CSS / JS",     "django",       80, "fas fa-code",          True),
            ("Docker",              "django",       78, "fab fa-docker",        True),
            ("REST API Design",     "django",       88, "fas fa-plug",          False),
            ("Penetration Testing", "cybersecurity",88, "fas fa-user-secret",   True),
            ("Web App Security",    "cybersecurity",90, "fas fa-lock",          True),
            ("Burp Suite",          "tools",        82, "fas fa-bug",           True),
            ("Kali Linux",          "cybersecurity",85, "fab fa-linux",         True),
            ("Metasploit",          "cybersecurity",75, "fas fa-terminal",      False),
            ("Network Security",    "cybersecurity",80, "fas fa-network-wired", True),
            ("OSINT",               "osint",        85, "fas fa-search",        True),
            ("Maltego",             "osint",        78, "fas fa-project-diagram",False),
            ("Linux / Bash",        "tools",        88, "fab fa-linux",         True),
            ("Nmap / Wireshark",    "tools",        80, "fas fa-terminal",      False),
            ("Git / GitHub",        "tools",        90, "fab fa-github",        False),
            ("AWS",                 "tools",        70, "fab fa-aws",           False),
        ]
        for name, cat, prof, icon, featured in skills_data:
            Skill.objects.update_or_create(
                name=name,
                defaults={"category": cat, "proficiency": prof, "icon_class": icon, "is_featured": featured}
            )
        self.stdout.write(f"  ✓ {len(skills_data)} skills")

        # ─── Experience ──────────────────────────────────────────
        exp_data = [
            ("Senior Cybersecurity Engineer", "SecureOps Africa", "Abuja, Nigeria",
             "2022-03-01", None, True,
             "Lead security assessments and penetration tests for financial institutions and "
             "e-commerce platforms. Develop secure Django web applications with security-first "
             "architecture. Conduct OSINT investigations and threat intelligence research. "
             "Maintain automated vulnerability scanning pipelines using Python.",
             "Python,Django,Kali Linux,Burp Suite,Nmap,PostgreSQL,Docker"),
            ("Django Developer & Security Consultant", "TechBridge Nigeria", "Abuja, Nigeria",
             "2020-06-01", "2022-02-28", False,
             "Built 8 production Django applications for clients across fintech, health, and education. "
             "Performed security audits and code reviews, identifying and resolving OWASP Top 10 "
             "vulnerabilities. Implemented CI/CD pipelines with automated security testing. "
             "Mentored 3 junior developers in secure coding practices.",
             "Python,Django,PostgreSQL,Docker,AWS,REST API,Nginx"),
            ("Ethical Hacking Instructor", "CyberSkills Academy", "Abuja, Nigeria",
             "2019-01-01", "2020-05-31", False,
             "Designed and delivered cybersecurity curriculum for 150+ students. "
             "Covered penetration testing, OSINT, network security, and web application security. "
             "Achieved 94% student satisfaction rating and 70% job placement rate. "
             "Built custom CTF lab environments for hands-on learning.",
             "Kali Linux,Metasploit,Burp Suite,Wireshark,Python,OSINT Tools"),
        ]
        for exp_tuple in exp_data:
            title, company, loc, start, end, current, desc, techs = exp_tuple
            Experience.objects.update_or_create(
                title=title, company=company,
                defaults={
                    "location": loc,
                    "start_date": date.fromisoformat(start),
                    "end_date": date.fromisoformat(end) if end else None,
                    "is_current": current,
                    "description": desc,
                    "technologies": techs,
                }
            )
        self.stdout.write(f"  ✓ {len(exp_data)} experience entries")

        # ─── Education ───────────────────────────────────────────
        Education.objects.update_or_create(
            institution="University of Abuja", degree="BSc Computer Science",
            defaults={"field_of_study": "Computer Science", "start_year": 2015,
                      "end_year": 2019, "is_current": False, "description": "Second Class Upper Division"}
        )
        Education.objects.update_or_create(
            institution="Cybrary / Online", degree="Advanced Cybersecurity Certificate",
            defaults={"field_of_study": "Information Security", "start_year": 2020,
                      "end_year": 2021, "is_current": False, "description": "Penetration Testing & Ethical Hacking track"}
        )
        self.stdout.write("  ✓ 2 education entries")

        # ─── Certifications ──────────────────────────────────────
        cert_data = [
            ("Certified Ethical Hacker (CEH)",                  "EC-Council",          "2021-04-15"),
            ("CompTIA Security+",                               "CompTIA",             "2020-11-01"),
            ("Offensive Security Certified Professional (OSCP)","Offensive Security",  "2022-07-20"),
            ("AWS Certified Security — Specialty",              "Amazon Web Services", "2022-11-10"),
            ("eLearnSecurity Web App Pentester (eWPT)",         "eLearnSecurity",      "2021-09-05"),
            ("Google Cybersecurity Certificate",                "Google / Coursera",   "2023-02-14"),
        ]
        for name, org, issued in cert_data:
            Certification.objects.update_or_create(
                name=name,
                defaults={"issuing_org": org, "issue_date": date.fromisoformat(issued), "is_featured": True}
            )
        self.stdout.write(f"  ✓ {len(cert_data)} certifications")

        # ─── Technologies ────────────────────────────────────────
        tech_names = [
            "Python","Django","PostgreSQL","Docker","Linux","Nginx","AWS",
            "REST API","Git","Burp Suite","Metasploit","Kali Linux","Nmap",
            "Wireshark","OWASP","SQLmap","Maltego","Celery","Redis","Gunicorn",
        ]
        tech_objs = {}
        for name in tech_names:
            t, _ = Technology.objects.get_or_create(name=name)
            tech_objs[name] = t
        self.stdout.write(f"  ✓ {len(tech_names)} technologies")

        # ─── Project Categories ───────────────────────────────────
        cat_data = [
            ("Django Development",    "django-development"),
            ("Cybersecurity",         "cybersecurity"),
            ("OSINT & Research",      "osint-research"),
            ("Automation",            "automation"),
            ("Web App Security",      "web-app-security"),
        ]
        cat_objs = {}
        for name, slug in cat_data:
            c, _ = ProjectCategory.objects.update_or_create(
                slug=slug, defaults={"name": name}
            )
            cat_objs[slug] = c

        # ─── Projects ────────────────────────────────────────────
        Project.objects.all().delete()

        projects_data = [
            {
                "title": "Secure Django E-Commerce Platform",
                "slug": "secure-django-ecommerce",
                "type": "web", "cat": "django-development",
                "desc": "A hardened Django e-commerce platform with OWASP Top 10 mitigations, 2FA, encrypted payments, and automated security scanning.",
                "overview": "Built a production-ready e-commerce platform for a Lagos-based retailer, implementing security-first architecture. The platform processes ₦15M+ in monthly transactions with zero security incidents.",
                "problem": "The client\'s previous platform had been breached twice — once via SQL injection, once via XSS in the product review system. They needed a completely rebuilt, hardened platform.",
                "objectives": "1. Rebuild with OWASP Top 10 as the primary requirement\n2. Implement 2FA and session security\n3. Achieve PCI-DSS alignment for payment handling\n4. Pass independent security audit",
                "architecture": "Django 4.2 backend with DRF API, PostgreSQL with row-level encryption, Nginx + Gunicorn, Docker deployment, Cloudflare WAF, automated Bandit/Safety security scanning in CI/CD.",
                "features": "2FA with TOTP, CSRF/XSS/SQL injection protection, encrypted PII fields, rate-limited login, CSP headers, audit logging, automated dependency vulnerability scanning",
                "challenges": "Encrypting existing customer PII required a zero-downtime migration strategy. The legacy codebase had 47 identified vulnerabilities that needed resolution before launch.",
                "solutions": "Implemented field-level encryption using cryptography library, migrated in batches with rollback capability. Resolved all 47 vulnerabilities systematically, starting with critical severity.",
                "lessons": "Security retrofitting is 10x harder than security-first design. The time invested in a threat model before writing code pays for itself many times over.",
                "techs": ["Python","Django","PostgreSQL","Docker","Nginx","Gunicorn","Redis"],
                "featured": True,
                "metrics": [("Vulnerabilities Fixed","47"),("Transactions/month","₦15M+"),("Security Score","A+ (SSL Labs)"),("Uptime","99.97%")]
            },
            {
                "title": "OSINT Investigation Toolkit",
                "slug": "osint-investigation-toolkit",
                "type": "automation", "cat": "osint-research",
                "desc": "A Python-based OSINT automation toolkit for digital footprint analysis, social media intelligence, and corporate reconnaissance.",
                "overview": "Developed a comprehensive OSINT toolkit used by security researchers and corporate investigators to automate open-source intelligence gathering. The tool aggregates data from 20+ public sources.",
                "problem": "Manual OSINT investigations took 3-8 hours per subject. Investigators were missing critical data points due to the volume of sources to check.",
                "objectives": "1. Automate data collection from 20+ OSINT sources\n2. Reduce investigation time from hours to minutes\n3. Generate structured intelligence reports\n4. Maintain legal compliance across all data sources",
                "architecture": "Python async architecture using aiohttp for concurrent API calls, SQLite for session storage, Jinja2 for report generation, modular plugin system for adding new sources.",
                "features": "Domain intelligence, social media profiling, email validation, phone number lookup, corporate registration data, geolocation analysis, automated PDF report generation, CLI and API modes",
                "challenges": "Rate limiting across 20+ different APIs required intelligent throttling and retry logic. Ensuring all data sources were legally compliant required careful review of each source\'s ToS.",
                "solutions": "Built an adaptive rate limiter with per-domain configuration. Created a compliance checklist and terms-of-service review process for every data source integration.",
                "lessons": "OSINT tools must be designed with ethics as a core feature. Every capability should have a clear legitimate use case documented before implementation.",
                "techs": ["Python","REST API","SQLmap","Maltego","Linux"],
                "featured": True,
                "metrics": [("Data Sources","20+"),("Time Saved","85%"),("Reports Generated","500+"),("Accuracy Rate","94%")]
            },
            {
                "title": "Web Application Penetration Testing Framework",
                "slug": "web-pentest-framework",
                "type": "web", "cat": "cybersecurity",
                "desc": "An automated web application security testing framework built with Python, covering OWASP Top 10 vulnerabilities with detailed reporting.",
                "overview": "Built a custom penetration testing framework for systematically testing web applications against the OWASP Top 10. Used in 25+ client engagements to produce consistent, professional security reports.",
                "problem": "Commercial pen testing tools were expensive and produced generic reports. Client engagements needed customisable testing workflows and reports branded to the client\'s risk context.",
                "objectives": "1. Cover all OWASP Top 10 vulnerability categories\n2. Generate client-ready reports in PDF format\n3. Support both automated and manual testing workflows\n4. Integrate with Burp Suite for manual testing",
                "architecture": "Python core with Burp Suite extension API integration, modular test plugins per vulnerability category, Jinja2 report templates, severity scoring using CVSS 3.1.",
                "features": "SQL injection detection, XSS scanner, CSRF checker, authentication testing, session management analysis, sensitive data exposure detection, CVSS scoring, executive summary generation",
                "challenges": "False positive rates in automated scanners were initially too high to be useful. Calibrating detection heuristics required extensive testing against known-vulnerable applications.",
                "solutions": "Built a confidence scoring system that weighs multiple signals before flagging a vulnerability. Added manual verification workflows for medium/high confidence findings.",
                "lessons": "Automated security testing complements but never replaces human expertise. The framework is a force multiplier, not a replacement for skilled penetration testers.",
                "techs": ["Python","Burp Suite","Kali Linux","OWASP","Nmap"],
                "featured": True,
                "metrics": [("Vulnerabilities Found","340+ across 25 clients"),("OWASP Coverage","100%"),("False Positive Rate","<5%"),("Clients Served","25+")]
            },
            {
                "title": "Django Multi-Tenant SaaS Platform",
                "slug": "django-multitenant-saas",
                "type": "web", "cat": "django-development",
                "desc": "A secure multi-tenant SaaS application built with Django, featuring tenant isolation, RBAC, API rate limiting, and automated billing.",
                "overview": "Built a multi-tenant project management SaaS for a Nigerian startup, serving 50+ organisations with strict data isolation guarantees and enterprise security controls.",
                "problem": "The client needed to serve multiple organisations on a single platform while guaranteeing complete data isolation between tenants — a complex security and architectural challenge.",
                "objectives": "1. Implement schema-based tenant isolation in PostgreSQL\n2. Build RBAC with organisation-level, team-level, and user-level permissions\n3. Rate limit API usage per tenant\n4. Automate billing via Paystack integration",
                "architecture": "Django with django-tenants for schema isolation, DRF for API, Redis + Celery for async tasks, PostgreSQL with row-level security as a secondary isolation layer, Nginx for routing.",
                "features": "Schema-based tenant isolation, 3-tier RBAC, API rate limiting per tenant, automated onboarding flow, Paystack billing integration, tenant admin portal, audit trail",
                "challenges": "django-tenants + DRF authentication required custom middleware to resolve the tenant from the request domain before JWT validation. Migration management across 50+ schemas needed automation.",
                "solutions": "Built custom tenant-aware authentication middleware. Created a management command for automated cross-tenant migrations with rollback support.",
                "lessons": "Multi-tenancy is a security architecture decision, not just an infrastructure one. Design the tenant boundary in the data model before writing any application code.",
                "techs": ["Python","Django","PostgreSQL","Redis","Celery","Docker","Nginx"],
                "featured": True,
                "metrics": [("Tenants","50+ orgs"),("Data Isolation","Schema-level"),("API Uptime","99.95%"),("Security Audits Passed","3")]
            },
            {
                "title": "Automated Vulnerability Scanner",
                "slug": "automated-vulnerability-scanner",
                "type": "automation", "cat": "automation",
                "desc": "A scheduled Python tool that continuously scans production Django applications for newly disclosed CVEs in dependencies and configuration drift.",
                "overview": "Built a continuous vulnerability monitoring tool that watches for new CVEs affecting the Python/Django ecosystem and alerts engineers within hours of disclosure.",
                "problem": "The team was discovering dependency vulnerabilities weeks after disclosure — far too late. Manual security reviews were quarterly, leaving months-long windows of exposure.",
                "objectives": "1. Monitor CVE databases for Python dependency vulnerabilities in real time\n2. Integrate with existing CI/CD pipeline\n3. Alert engineers within 2 hours of critical CVE disclosure\n4. Reduce mean time to patch from 30 days to 48 hours",
                "features": "Real-time CVE feed monitoring, dependency graph analysis, CVSS severity triage, Slack/email alerting, automated PR creation for patch updates, configuration drift detection",
                "challenges": "CVE database APIs have inconsistent schemas and occasional downtime. False alarms cause alert fatigue. Needed smart deduplication and severity filtering.",
                "solutions": "Built an abstraction layer normalising 3 CVE feed sources. Implemented confidence scoring and severity thresholds to only alert on genuinely actionable findings.",
                "lessons": "Security automation only delivers value if engineers trust it. Invest heavily in reducing false positives — one bad alert can train engineers to ignore all alerts.",
                "techs": ["Python","REST API","Git","Docker","Linux","AWS"],
                "featured": False,
                "metrics": [("CVEs Monitored","5,000+ monthly"),("Alert Time","< 2 hours"),("MTTP Reduction","30d → 48h"),("False Positive Rate","< 3%")]
            },
        ]

        for pd in projects_data:
            proj, _ = Project.objects.update_or_create(
                slug=pd["slug"],
                defaults={
                    "title": pd["title"],
                    "project_type": pd["type"],
                    "category": cat_objs.get(pd["cat"]),
                    "short_description": pd["desc"],
                    "overview": pd["overview"],
                    "problem_statement": pd["problem"],
                    "objectives": pd["objectives"],
                    "architecture": pd.get("architecture",""),
                    "features": pd["features"],
                    "challenges": pd["challenges"],
                    "solutions": pd.get("solutions",""),
                    "lessons_learned": pd["lessons"],
                    "is_featured": pd["featured"],
                    "status": "completed",
                }
            )
            proj.technologies.set([tech_objs[t] for t in pd["techs"] if t in tech_objs])
            proj.metrics.all().delete()
            for order, (label, value) in enumerate(pd["metrics"]):
                ProjectMetric.objects.create(project=proj, label=label, value=value, order=order)
        self.stdout.write(f"  ✓ {len(projects_data)} projects")

        # ─── Blog ─────────────────────────────────────────────────
        bcat_objs = {}
        for name, slug in [
            ("Cybersecurity","cybersecurity"), ("Python & Django","python-django"),
            ("OSINT","osint"), ("Career","career"), ("Tutorials","tutorials"),
        ]:
            bc, _ = BlogCategory.objects.update_or_create(slug=slug, defaults={"name": name})
            bcat_objs[slug] = bc

        author, created = User.objects.get_or_create(username="peter")
        if created:
            author.set_password("admin123")
            author.first_name="Peter"; author.last_name="Charles"
            author.is_staff=True; author.is_superuser=True
            author.save()

        posts_data = [
            ("OWASP Top 10: A Practical Django Developer\'s Guide", "owasp-top-10-django-guide",
             "cybersecurity",
             "A hands-on guide to mitigating every OWASP Top 10 vulnerability in Django applications, with real code examples.",
             "The OWASP Top 10 is not a compliance checkbox — it\'s a battle plan.\n\n"
             "In this article I walk through each of the 10 categories and show exactly how they manifest in Django applications, and how to fix them.\n\n"
             "A1: Injection. Always use the Django ORM. Never interpolate user input into raw SQL queries.\n\n"
             "A2: Broken Authentication. Use Django\'s built-in auth, add 2FA with django-otp, and enforce strong password policies.\n\n"
             "Read the full guide for all 10 categories with code examples.", True),
            ("Building a Python OSINT Tool From Scratch", "python-osint-tool-from-scratch",
             "osint",
             "A step-by-step tutorial on building a Python OSINT tool that aggregates public data from multiple sources ethically and legally.",
             "OSINT (Open Source Intelligence) is the practice of collecting intelligence from publicly available sources.\n\n"
             "In this tutorial, we build a Python script that takes a domain name as input and returns:\n"
             "- WHOIS registration data\n- DNS records\n- SSL certificate information\n- Shodan exposure data\n\n"
             "We\'ll use aiohttp for concurrent requests, python-whois, and the Shodan API.\n\n"
             "Always ensure you have authorisation before running OSINT tools against any target.", True),
            ("Django Security Hardening Checklist for Production", "django-security-hardening-checklist",
             "python-django",
             "A comprehensive checklist of 25 security hardening steps every Django application should implement before going live.",
             "After auditing dozens of Django applications, the same security misconfigurations appear repeatedly.\n\n"
             "This checklist covers the 25 most impactful hardening steps:\n\n"
             "1. Set DEBUG=False and configure ALLOWED_HOSTS properly\n"
             "2. Use HTTPS everywhere with HSTS\n"
             "3. Configure Content Security Policy headers\n"
             "4. Enable CSRF protection on all forms\n"
             "5. Use Django\'s SECRET_KEY rotation mechanism\n\n"
             "Implement all 25 before you launch.", True),
        ]
        for title, slug, cat_slug, excerpt, content, featured in posts_data:
            Post.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title, "author": author,
                    "category": bcat_objs.get(cat_slug),
                    "excerpt": excerpt, "content": content,
                    "status": "published", "is_featured": featured,
                    "views_count": 0, "published_at": timezone.now(),
                }
            )
        self.stdout.write(f"  ✓ {len(posts_data)} blog posts")

        # ─── Services ─────────────────────────────────────────────
        services_data = [
            ("Penetration Testing", "penetration-testing", "fas fa-user-secret",
             "Comprehensive web application and network penetration testing with detailed remediation reports.",
             "I perform authorised security assessments of web applications, APIs, and network infrastructure to identify vulnerabilities before attackers do.\n\n"
             "Every engagement follows a structured methodology: reconnaissance, scanning, exploitation, reporting, and remediation guidance.",
             "Scope definition & rules of engagement\nPassive & active reconnaissance\nVulnerability scanning & manual testing\nExploitation (controlled)\nDetailed findings report with CVSS scores\nRemediation guidance & retest",
             "Executive summary\nTechnical findings report (CVSS scored)\nProof-of-concept documentation\nRemediation roadmap\nRetest report",
             250000, "1–3 weeks", True, True),
            ("Secure Django Development", "secure-django-development", "fas fa-server",
             "Full-stack Django web application development with security-first architecture and OWASP compliance.",
             "I build production-ready Django applications where security is not an afterthought but the foundation. "
             "Every project includes threat modelling, secure coding standards, automated security testing, and deployment hardening.",
             "Requirements & threat modelling\nSecurity architecture design\nDjango application development\nSecurity testing (SAST + DAST)\nDocker deployment\nCI/CD with security scanning",
             "Production-ready Django application\nSecurity architecture document\nTest suite (>80% coverage)\nDocumentation\nDeployment configuration",
             300000, "4–16 weeks", True, True),
            ("OSINT Investigation", "osint-investigation", "fas fa-search",
             "Professional OSINT investigations for due diligence, threat intelligence, and digital footprint analysis.",
             "I conduct structured OSINT investigations using a combination of automated tools and manual research techniques. "
             "All investigations are conducted legally, using only publicly available information.",
             "Subject identification & scoping\nDigital footprint analysis\nSocial media intelligence\nCorporate & domain intelligence\nThreat assessment\nStructured intelligence report",
             "Comprehensive intelligence report\nDigital footprint map\nRisk assessment\nRecommendations",
             150000, "3–7 days", True, True),
            ("Cybersecurity Training", "cybersecurity-training", "fas fa-graduation-cap",
             "Hands-on cybersecurity training for individuals and corporate teams — from fundamentals to advanced techniques.",
             "I design and deliver practical cybersecurity training programmes tailored to your team\'s current skill level and objectives. "
             "Training is hands-on, using real tools and real attack/defence scenarios.",
             "Needs assessment\nCustom curriculum design\nHands-on lab setup\nLive instruction (online or in-person)\nCTF exercises\nCertificate of completion",
             "Training materials\nLab environment access\nExercise workbooks\nCertificates",
             100000, "1–5 days", True, True),
        ]
        for title,slug,icon,short,full,feats,delivs,price,duration,featured,active in services_data:
            Service.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title, "icon_class": icon, "short_description": short,
                    "full_description": full, "features": feats, "deliverables": delivs,
                    "price_from": price, "duration": duration,
                    "is_featured": featured, "is_active": active,
                }
            )
        self.stdout.write(f"  ✓ {len(services_data)} services")

        # ─── Training Programs ────────────────────────────────────
        training_data = [
            ("Ethical Hacking Bootcamp", "ethical-hacking-bootcamp", "beginner", "online",
             "A comprehensive 8-week bootcamp covering penetration testing, OSINT, and web application security.",
             "From zero to junior penetration tester in 8 weeks. You will learn the full ethical hacking methodology, work through 20+ hands-on labs, and attempt a final CTF challenge.",
             "Week 1–2: Fundamentals — Networking, Linux, Python for security\nWeek 3: Reconnaissance — Passive & active OSINT\nWeek 4: Scanning & Enumeration — Nmap, Gobuster, Nikto\nWeek 5: Web Application Security — OWASP Top 10, Burp Suite\nWeek 6: Exploitation — Metasploit, manual exploitation\nWeek 7: Post-exploitation & Persistence\nWeek 8: Reporting & CTF Challenge",
             8, 12, 150000, 20, True, True),
            ("Secure Django Development", "secure-django-dev-training", "intermediate", "hybrid",
             "A 6-week programme for Python developers who want to build production-grade, security-hardened Django applications.",
             "Learn how to build Django applications that are secure from the ground up. You will implement authentication systems, secure APIs, and deploy hardened production environments.",
             "Week 1: Django security fundamentals & threat modelling\nWeek 2: Authentication, authorisation & RBAC\nWeek 3: Secure API design with DRF\nWeek 4: OWASP Top 10 in Django — hands-on fixes\nWeek 5: Docker, deployment hardening & CI/CD security\nWeek 6: Security testing & capstone project",
             6, 8, 120000, 15, True, True),
            ("OSINT Masterclass", "osint-masterclass", "intermediate", "online",
             "A practical 4-week OSINT training programme covering digital footprint analysis, social media intelligence, and investigation techniques.",
             "Learn professional OSINT techniques using real tools and real-world scenarios. This course is suitable for security researchers, investigators, journalists, and HR professionals.",
             "Week 1: OSINT fundamentals & legal framework\nWeek 2: Social media & digital footprint analysis\nWeek 3: Domain, email & phone intelligence\nWeek 4: Corporate OSINT & capstone investigation",
             4, 6, 80000, 25, False, True),
        ]
        for title,slug,level,mode,short,full,curr,weeks,hrs,price,max_p,cert,active in training_data:
            TrainingProgram.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title, "level": level, "delivery_mode": mode,
                    "short_description": short, "full_description": full, "curriculum": curr,
                    "duration_weeks": weeks, "hours_per_week": hrs, "price": price,
                    "max_participants": max_p, "certificate_offered": cert,
                    "is_active": active, "is_featured": True,
                    "icon_class": "fas fa-graduation-cap",
                }
            )
        self.stdout.write(f"  ✓ {len(training_data)} training programs")

        # ─── Testimonials ─────────────────────────────────────────
        testimonials_data = [
            ("Chukwuemeka Obi", "CTO", "FinSecure Nigeria",
             "Peter performed a penetration test on our banking API and found 3 critical vulnerabilities that our internal team had missed for over a year. His report was exceptionally clear and actionable. Highly recommended.", 5, True),
            ("Dr. Amaka Eze", "Head of IT", "HealthConnect Africa",
             "Peter rebuilt our patient data platform with a security-first approach. After a previous breach, we needed someone we could trust. He delivered a hardened, NDPR-compliant system on time and within budget.", 5, True),
            ("Bello Usman", "Bootcamp Graduate", "Ethical Hacking Bootcamp",
             "I had no security background when I started Peter\'s bootcamp. Eight weeks later I passed my CEH exam on the first attempt and landed a junior analyst role. The hands-on labs are exceptional.", 5, True),
            ("Fatima Aliyu", "Founder", "TechHub Abuja",
             "Peter built our SaaS platform and his attention to security details was remarkable. He explained every decision in terms we could understand. Our platform passed a third-party security audit with zero critical findings.", 5, True),
            ("Ngozi Okeke", "Security Analyst", "Cyberwatch Africa",
             "Peter\'s OSINT masterclass changed how I approach investigations. The tools and methodologies he taught are immediately applicable to real-world cases. Best training investment I\'ve made.", 5, True),
        ]
        for name, title, company, content, rating, featured in testimonials_data:
            Testimonial.objects.update_or_create(
                client_name=name,
                defaults={
                    "client_title": title, "client_company": company,
                    "content": content, "rating": rating,
                    "is_featured": featured, "is_approved": True,
                }
            )
        self.stdout.write(f"  ✓ {len(testimonials_data)} testimonials")

        self.stdout.write(self.style.SUCCESS("\n✅ Cybersecurity portfolio data seeded!"))
        self.stdout.write("   Admin: peter / admin123")
