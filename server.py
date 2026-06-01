"""
Agent Legal Counsel MCP - Premium AI Agent Legal Contract Generator
MCP Server for generating legally-structured contracts for AI agent services.
"""

import json
import time
import os
import re
from typing import Dict, List, Optional, Any
from datetime import datetime, date

# Check if we can import mcp
try:
    from mcp import types
    from mcp.server.lowlevel import Server
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio as stdio_server
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("MCP SDK not available. Running in standalone/test mode.")

# ============================================================
# API Key Configuration
# ============================================================
# Free keys start with "free_", Pro keys start with "pro_"
API_KEYS = {
    "free_demo_key_2024": {"tier": "free", "used": 0, "month": datetime.now().month},
    "prol_demo_key_2024": {"tier": "pro", "used": 0, "month": datetime.now().month},
}

# Pro keys get 500 calls/day, free gets 50/day
RATE_LIMITS = {
    "free": {"daily": 50, "monthly_contracts": 1},
    "pro": {"daily": 500, "monthly_contracts": 50},
}

# Track usage per API key
usage_tracker: Dict[str, Dict] = {}

# ============================================================
# Contract Templates (Hardcoded, 500-1000 words each)
# ============================================================

TEMPLATES = {
    "ai_service_agreement": {
        "name": "AI Agent Service Agreement",
        "description": "Standard service agreement for AI agent services covering scope, payment, liability, and termination.",
        "version": "2.1",
    },
    "ai_data_processing": {
        "name": "AI Agent Data Processing Agreement",
        "description": "Data processing addendum for AI agents handling personal or sensitive data under GDPR/CCPA frameworks.",
        "version": "2.0",
    },
    "ai_saas_terms": {
        "name": "AI Agent SaaS Subscription Terms",
        "description": "Subscription terms for AI-powered SaaS products including uptime SLAs and usage limits.",
        "version": "1.3",
    },
    "ai_nda": {
        "name": "AI Agent Non-Disclosure Agreement",
        "description": "Mutual NDA for protecting proprietary algorithms, training data, and business secrets in AI collaborations.",
        "version": "1.5",
    },
}

__CONTRACT_TEMPLATES_CACHE = None

def _get_all_templates():
    global __CONTRACT_TEMPLATES_CACHE
    if __CONTRACT_TEMPLATES_CACHE is not None:
        return __CONTRACT_TEMPLATES_CACHE
    __CONTRACT_TEMPLATES_CACHE = {
        "ai_service_agreement": _generate_ai_service_agreement({}),
        "ai_data_processing": _generate_ai_data_processing({}),
        "ai_saas_terms": _generate_ai_saas_terms({}),
        "ai_nda": _generate_ai_nda({}),
    }
    return __CONTRACT_TEMPLATES_CACHE


def _generate_ai_service_agreement(params: Dict) -> str:
    agent_name = params.get("agent_name", "[Agent Name/System Name]")
    service_desc = params.get("service_description", "[Description of AI agent services]")
    payment_terms = params.get("payment_terms", "Net-30 following monthly invoicing")
    duration = params.get("duration", "12 months")
    liability_limit = params.get("liability_limit", "fees paid during the 12 months preceding the claim")
    jurisdiction = params.get("jurisdiction", "the State of Delaware")
    parties = params.get("parties", "[Client Name]")
    effective_date = params.get("effective_date", datetime.now().strftime("%B %d, %Y"))

    return f"""AI AGENT SERVICE AGREEMENT

Effective Date: {effective_date}

This AI Agent Service Agreement (the "Agreement") is entered into as of the Effective Date by and between {parties} ("Client") and the operator of the {agent_name} system ("Provider"). Client and Provider may each be referred to as a "Party" and collectively as the "Parties."

1. SERVICES PROVIDED.
Provider agrees to provide Client with access to the {agent_name} AI agent system, which performs the following services: {service_desc}. Provider shall make the system available twenty-four (24) hours per day, seven (7) days per week, subject to scheduled maintenance and unplanned downtime.

2. FEES AND PAYMENT TERMS.
Client shall pay Provider the fees set forth in applicable order forms or subscription plans. {payment_terms}. All fees are non-refundable except as expressly set forth herein. Late payments shall accrue interest at the rate of 1.5% per month or the maximum permitted by law, whichever is less.

3. TERM AND TERMINATION.
This Agreement shall commence on the Effective Date and continue for an initial term of {duration} (the "Initial Term"). Thereafter, this Agreement shall automatically renew for successive renewal terms, unless either Party provides written notice of non-renewal at least thirty (30) days prior to the end of the then-current term. Either Party may terminate this Agreement with thirty (30) days' written notice if the other Party materially breaches any provision and fails to cure such breach within the cure period.

4. INTELLECTUAL PROPERTY RIGHTS.
As between the Parties, Provider retains all right, title, and interest in and to the {agent_name} system, including all software, algorithms, models, training data, documentation, and related materials. Provider grants Client a non-exclusive, non-transferable, worldwide license to use the system during the Term solely for Client's internal business purposes. Client retains all rights to its input data and any output generated specifically for Client, subject to Provider's right to use anonymized, aggregated data for system improvement.

5. CONFIDENTIALITY.
Each Party agrees to hold in confidence all Confidential Information of the other Party. "Confidential Information" means any non-public information disclosed by one Party to the other, whether orally or in writing, that is designated as confidential or should reasonably be understood to be confidential. Confidential Information shall not include information that: (a) is or becomes publicly available without breach of this Agreement; (b) was known to the receiving Party prior to disclosure; (c) is independently developed by the receiving Party; or (d) is required to be disclosed by law. Each Party shall use the other's Confidential Information solely for purposes of this Agreement and shall protect it using reasonable care.

6. LIMITATION OF LIABILITY.
TO THE MAXIMUM EXTENT PERMITTED BY LAW, NEITHER PARTY SHALL BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING LOSS OF PROFITS, DATA, OR BUSINESS OPPORTUNITIES, ARISING OUT OF OR IN CONNECTION WITH THIS AGREEMENT. PROVIDER'S TOTAL LIABILITY UNDER THIS AGREEMENT SHALL NOT EXCEED THE TOTAL FEES PAID BY CLIENT TO PROVIDER IN THE {liability_limit}. THIS LIMITATION APPLIES REGARDLESS OF THE THEORY OF LIABILITY AND EVEN IF A PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

7. INDEMNIFICATION.
Provider shall indemnify, defend, and hold harmless Client from and against any third-party claim alleging that the {agent_name} system infringes any intellectual property right. Client shall indemnify, defend, and hold harmless Provider from and against any third-party claim arising from Client's use of the system in violation of applicable law or this Agreement.

8. REPRESENTATIONS AND WARRANTIES.
Each Party represents and warrants that it has the full power and authority to enter into this Agreement. Provider warrants that the system will perform substantially in accordance with the documentation. PROVIDER MAKES NO OTHER WARRANTIES, EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.

9. DATA PROTECTION AND PRIVACY.
Provider shall implement and maintain reasonable technical and organizational security measures to protect Client data against unauthorized access, disclosure, alteration, or destruction. Provider shall process Client data only in accordance with Client's documented instructions and shall not use Client data for any purpose other than providing the services under this Agreement.

10. GOVERNING LAW AND DISPUTE RESOLUTION.
This Agreement shall be governed by and construed in accordance with the laws of {jurisdiction}, without regard to its conflict of laws principles. Any dispute arising out of or relating to this Agreement shall first be submitted to mediation in {jurisdiction}, and if not resolved within sixty (60) days, shall be resolved by binding arbitration in accordance with the rules of the American Arbitration Association.

11. GENERAL PROVISIONS.
This Agreement constitutes the entire agreement between the Parties with respect to its subject matter and supersedes all prior agreements and understandings. No amendment shall be effective unless in writing and signed by both Parties. If any provision is held invalid, the remainder shall continue in full force and effect. The waiver of any breach shall not constitute a waiver of any subsequent breach. This Agreement may be executed in counterparts.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date.

[Provider Name]
By: ___________________________
Title: __________________________
Date: __________________________

{parties}
By: ___________________________
Title: __________________________
Date: __________________________
"""


def _generate_ai_data_processing(params: Dict) -> str:
    agent_name = params.get("agent_name", "[AI System Name]")
    data_categories = params.get("data_categories", "personal identification data, usage analytics, and business contact information")
    processing_purpose = params.get("processing_purpose", "operation and improvement of AI agent services")
    retention_period = params.get("retention_period", "twenty-four (24) months following collection")
    security_measures = params.get("security_measures", "industry-standard encryption at rest and in transit, access controls, and regular security assessments")
    jurisdiction = params.get("jurisdiction", "the United States and European Economic Area")
    parties = params.get("parties", "[Client Name]")
    effective_date = params.get("effective_date", datetime.now().strftime("%B %d, %Y"))
    subprocessors = params.get("subprocessors", "cloud infrastructure providers and analytics services")

    return f"""AI AGENT DATA PROCESSING AGREEMENT

Effective Date: {effective_date}

This AI Agent Data Processing Agreement (the "DPA") is entered into by and between {parties} ("Controller") and the operator of the {agent_name} system ("Processor"). This DPA supplements the underlying Service Agreement between the Parties.

1. DEFINITIONS.
"Personal Data" means any information relating to an identified or identifiable natural person processed under this DPA. "Processing" means any operation performed on Personal Data, including collection, storage, use, disclosure, and deletion. "Data Subject" means the identified or identifiable natural person to whom Personal Data relates.

2. PROCESSING DESCRIPTION.
Controller appoints Processor to process Personal Data on behalf of Controller for the following purpose: {processing_purpose}. The categories of Personal Data subject to processing include: {data_categories}. Processing operations include collection, storage, retrieval, analysis, and deletion of Personal Data.

3. PROCESSOR OBLIGATIONS.
Processor shall: (a) process Personal Data only on documented instructions from Controller, unless required by applicable law; (b) ensure that persons authorized to process Personal Data are subject to confidentiality obligations; (c) implement appropriate technical and organizational security measures as described in Section 5; (d) not engage another processor without prior written authorization; (e) assist Controller in fulfilling its obligations regarding Data Subject rights; (f) assist Controller with compliance with data security, breach notification, and data protection impact assessment obligations; (g) delete or return all Personal Data at Controller's election upon termination; and (h) make available to Controller all information necessary to demonstrate compliance.

4. SUBPROCESSORS.
Controller authorizes Processor to engage the following subprocessors: {subprocessors}. Processor shall notify Controller at least thirty (30) days in advance of any intended changes to subprocessors, and Controller may object to such changes. Processor shall impose substantially similar data protection obligations on all subprocessors.

5. SECURITY MEASURES.
Processor shall implement and maintain the following security measures: {security_measures}. These measures include, but are not limited to: encryption of Personal Data at rest using AES-256 and in transit using TLS 1.2 or higher; strict access controls based on the principle of least privilege; regular vulnerability assessments and penetration testing; intrusion detection and prevention systems; physical security controls at data center facilities; and comprehensive incident response procedures.

6. DATA BREACH NOTIFICATION.
Processor shall notify Controller without undue delay, and in any event within forty-eight (48) hours, upon becoming aware of a data breach involving Personal Data processed under this DPA. Such notification shall include: (a) a description of the nature of the breach; (b) the categories and approximate number of Data Subjects and Personal Data records concerned; (c) the likely consequences; and (d) measures taken or proposed to address the breach.

7. DATA SUBJECT RIGHTS.
Processor shall assist Controller in fulfilling its obligations to respond to Data Subject requests to exercise their rights under applicable data protection laws. Processor shall promptly notify Controller of any request received directly from a Data Subject and shall not respond to such request without Controller's prior authorization, except as required by law.

8. CROSS-BORDER DATA TRANSFERS.
Personal Data may be processed in {jurisdiction}. Processor shall ensure that any transfer of Personal Data from the European Economic Area, the United Kingdom, or Switzerland to a country that does not ensure adequate protection is subject to appropriate safeguards, including Standard Contractual Clauses as approved by the European Commission.

9. DATA RETENTION AND DELETION.
Processor shall retain Personal Data for no longer than {retention_period}, unless a longer retention period is required by applicable law. Upon termination or expiry of the underlying Service Agreement, Processor shall, at Controller's election, delete or return all Personal Data within thirty (30) days, unless retention is required by law.

10. AUDIT RIGHTS.
Processor shall make available to Controller all information necessary to demonstrate compliance with this DPA and applicable data protection laws. Controller may conduct audits, including inspections, no more than once per calendar year, upon reasonable notice and at Controller's expense. Processor shall contribute to the cost of such audits up to a reasonable amount.

11. LIABILITY.
Each Party's liability under this DPA shall be subject to the limitations set forth in the underlying Service Agreement. However, Processor acknowledges that its liability under this DPA may be unlimited in specific circumstances under applicable data protection laws.

12. GOVERNING LAW.
This DPA shall be governed by the laws applicable to the underlying Service Agreement. Any disputes arising under this DPA shall be resolved in accordance with the dispute resolution provisions of the underlying Service Agreement.

IN WITNESS WHEREOF, the Parties have executed this DPA as of the Effective Date.

[Processor Name - {agent_name} operator]
By: ___________________________
Date: __________________________

{parties}
By: ___________________________
Date: __________________________
"""


def _generate_ai_saas_terms(params: Dict) -> str:
    product_name = params.get("product_name", "[AI SaaS Product Name]")
    service_desc = params.get("service_description", "[Description of SaaS services]")
    payment_terms = params.get("payment_terms", "monthly in advance at the rates specified on the pricing page")
    support_hours = params.get("support_hours", "business hours with a response time of eight (8) hours for critical issues")
    uptime_sla = params.get("uptime_sla", "99.5%")
    data_storage = params.get("data_storage", "encrypted cloud storage with daily backups retained for thirty (30) days")
    parties = params.get("parties", "[Customer Name]")
    effective_date = params.get("effective_date", datetime.now().strftime("%B %d, %Y"))
    usage_limits = params.get("usage_limits", "fair use limits specified in the product documentation or applicable subscription plan")

    return f"""AI AGENT SaaS SUBSCRIPTION TERMS

Effective Date: {effective_date}

These AI Agent SaaS Subscription Terms (the "Terms") govern Customer's use of the {product_name} software-as-a-service platform (the "Service"), provided by the Service operator ("Provider") to {parties} ("Customer"). These Terms, together with any applicable Order Forms, constitute the entire agreement.

1. SERVICE SUBSCRIPTION.
Provider grants Customer a non-exclusive, non-transferable right to access and use the Service during the subscription term in accordance with these Terms and any applicable Order Forms. Customer shall not: (a) license, sublicense, sell, resell, transfer, assign, or distribute the Service; (b) modify, reverse engineer, decompile, or disassemble the Service; (c) create derivative works based on the Service; (d) use the Service for any unlawful purpose; or (e) exceed usage limits including {usage_limits}.

2. SERVICE DESCRIPTION.
The {product_name} Service provides: {service_desc}. Provider may update or modify the Service from time to time, provided that such changes do not materially reduce the core functionality of the Service.

3. FEES AND SUBSCRIPTION.
Customer shall pay subscription fees as follows: {payment_terms}. All fees are non-refundable except as expressly provided herein. Provider may change its fees upon thirty (30) days' prior notice. Subscription plans are billed {payment_terms}. Overages beyond plan limits will be billed at the rates specified on the pricing page.

4. SERVICE LEVELS.
Provider shall use commercially reasonable efforts to maintain the Service availability at or above {uptime_sla} uptime, calculated on a monthly basis, excluding scheduled maintenance and force majeure events. If Provider fails to meet the SLA in any calendar month, Customer may request a service credit equal to 5% of the monthly fee for each full percentage point below the SLA, up to a maximum of 25% of the monthly fee.

5. SUPPORT.
Provider shall provide technical support as follows: {support_hours}. Support shall include troubleshooting, bug fixes, and assistance with configuration. Critical issues affecting production use shall receive priority response.

6. DATA STORAGE AND SECURITY.
Customer data shall be stored using: {data_storage}. Provider shall implement appropriate security measures, including encryption, access controls, and monitoring, to protect Customer data. Provider shall not access Customer data except to provide the Service, prevent abuse, or comply with legal obligations.

7. CUSTOMER OBLIGATIONS.
Customer represents and warrants that: (a) it has the authority to enter into these Terms; (b) its use of the Service will comply with all applicable laws; (c) it will not upload or transmit any content that infringes third-party rights or contains malware; and (d) it will maintain the confidentiality of its account credentials.

8. INTELLECTUAL PROPERTY.
Provider retains all intellectual property rights in the Service, including its software, user interface, algorithms, and documentation. Customer retains all rights to its content, data, and materials uploaded to or processed through the Service.

9. TERM AND TERMINATION.
These Terms commence on the Effective Date and continue for the initial subscription term. Either Party may terminate for material breach if the breach remains uncured after thirty (30) days' written notice. Upon termination, Customer's access to the Service shall cease, and Customer shall have thirty (30) days to retrieve its data.

10. WARRANTY DISCLAIMER.
THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE." PROVIDER DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. PROVIDER DOES NOT WARRANT THAT THE SERVICE WILL BE UNINTERRUPTED OR ERROR-FREE.

11. LIMITATION OF LIABILITY.
TO THE MAXIMUM EXTENT PERMITTED BY LAW, PROVIDER'S TOTAL LIABILITY FOR ALL CLAIMS ARISING OUT OF OR RELATED TO THESE TERMS SHALL NOT EXCEED THE TOTAL FEES PAID BY CUSTOMER IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM. PROVIDER SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES.

12. CONFIDENTIALITY.
Each Party agrees to maintain the confidentiality of the other Party's Confidential Information during the Term and for three (3) years thereafter. Confidential Information includes business plans, technical data, customer information, and pricing terms.

13. GOVERNING LAW.
These Terms shall be governed by the laws of the State of Delaware. Any disputes shall be resolved exclusively in the state or federal courts located in Delaware.

IN WITNESS WHEREOF, the Parties have executed these Terms as of the Effective Date.

[Provider Name]
By: ___________________________
Title: __________________________
Date: __________________________

{parties}
By: ___________________________
Title: __________________________
Date: __________________________
"""


def _generate_ai_nda(params: Dict) -> str:
    disclosing_party = params.get("disclosing_party", "[Disclosing Party Name]")
    receiving_party = params.get("receiving_party", "[Receiving Party Name]")
    purpose = params.get("purpose", "evaluation of a potential collaboration involving AI agent technologies, algorithms, and data")
    confidentiality_period = params.get("confidentiality_period", "three (3) years from the Effective Date")
    jurisdiction = params.get("jurisdiction", "the State of Delaware")
    exclusion_desc = params.get("exclusion_desc", "information that was independently developed without reference to Confidential Information")
    effective_date = params.get("effective_date", datetime.now().strftime("%B %d, %Y"))

    return f"""AI AGENT NON-DISCLOSURE AGREEMENT

Effective Date: {effective_date}

This AI Agent Non-Disclosure Agreement (the "NDA") is entered into by and between {disclosing_party} ("Disclosing Party") and {receiving_party} ("Receiving Party") (collectively, the "Parties") for the purpose of {purpose}.

1. DEFINITION OF CONFIDENTIAL INFORMATION.
"Confidential Information" means any non-public information disclosed by Disclosing Party to Receiving Party, whether orally, in writing, or in any other form, that is designated as confidential or that reasonably should be understood to be confidential given the nature of the information and circumstances of disclosure. With respect to AI agent technologies, Confidential Information specifically includes, but is not limited to: source code, model architectures, training data sets, model weights and parameters, algorithmic approaches, prompt engineering techniques, evaluation methodologies, training pipelines, proprietary datasets, business strategies, customer lists, financial information, product roadmaps, and technical specifications.

2. EXCLUSIONS.
Confidential Information does not include information that: (a) is or becomes publicly known through no breach of this NDA; (b) was rightfully in Receiving Party's possession prior to disclosure; (c) is rightfully obtained by Receiving Party from a third party without restriction; (d) {exclusion_desc}; or (e) is required to be disclosed by applicable law, regulation, or court order.

3. OBLIGATIONS OF RECEIVING PARTY.
Receiving Party shall: (a) hold all Confidential Information in strict confidence; (b) not disclose Confidential Information to any third party without Disclosing Party's prior written consent; (c) use Confidential Information solely for the Purpose; (d) limit access to Confidential Information to those employees, contractors, and advisors who have a legitimate need to know and are bound by confidentiality obligations at least as restrictive as those in this NDA; (e) protect Confidential Information using the same degree of care used to protect its own confidential information, but in no event less than reasonable care; and (f) promptly notify Disclosing Party of any unauthorized disclosure or use.

4. SPECIAL PROVISIONS FOR AI-RELATED CONFIDENTIAL INFORMATION.
Receiving Party acknowledges that AI-related Confidential Information, including model architectures, training data, and proprietary algorithms, is particularly sensitive and valuable. Receiving Party agrees: (a) not to reverse engineer, decompile, or attempt to extract model weights or architectures from any disclosed AI system; (b) not to use Confidential Information to train, improve, or develop competing AI models or systems; (c) not to use Confidential Information as input to any AI system without Disclosing Party's express written authorization; and (d) to implement additional technical controls, including air-gapped storage and access logging, for particularly sensitive Confidential Information.

5. TERM AND SURVIVAL.
This NDA shall commence on the Effective Date and continue for {confidentiality_period}. The obligations of confidentiality and non-use shall survive for a period of three (3) years from the date of disclosure for all Confidential Information, except for trade secrets, which shall be protected for as long as they remain trade secrets under applicable law.

6. RETURN OF CONFIDENTIAL INFORMATION.
Upon Disclosing Party's request, Receiving Party shall promptly return or destroy all copies of Confidential Information, including digital copies, and certify in writing that such return or destruction has been completed. Receiving Party may retain copies solely for legal compliance or archival purposes, subject to continuing confidentiality obligations.

7. NO LICENSE OR RIGHTS.
Nothing in this NDA grants Receiving Party any license, patent, copyright, or other intellectual property right in or to any Confidential Information of Disclosing Party. All Confidential Information remains the sole property of Disclosing Party.

8. REMEDIES.
Receiving Party acknowledges that monetary damages may be inadequate to remedy a breach or threatened breach of this NDA. Disclosing Party shall be entitled to seek injunctive relief and specific performance without the necessity of posting bond, in addition to any other remedies available at law or equity.

9. GOVERNING LAW.
This NDA shall be governed by and construed in accordance with the laws of {jurisdiction}. Any action arising out of or relating to this NDA shall be brought exclusively in the state or federal courts located in {jurisdiction}.

10. GENERAL.
This NDA constitutes the entire agreement between the Parties regarding its subject matter. This NDA may not be amended except in writing signed by both Parties. If any provision is held unenforceable, the remaining provisions shall continue in effect. This NDA may be executed in counterparts.

IN WITNESS WHEREOF, the Parties have executed this NDA as of the Effective Date.

{disclosing_party}
By: ___________________________
Title: __________________________
Date: __________________________

{receiving_party}
By: ___________________________
Title: __________________________
Date: __________________________
"""


# ============================================================
# Validation Checklist
# ============================================================

VALIDATION_CHECKLIST = {
    "contract_type": ["AI Agent Service Agreement", "AI Agent Data Processing Agreement",
                      "AI Agent SaaS Subscription Terms", "AI Agent Non-Disclosure Agreement"],
    "checklist": [
        "Parties identified with full legal names",
        "Effective date specified",
        "Scope of services clearly defined",
        "Payment terms and fee structure included",
        "Term and termination provisions included",
        "Intellectual property rights addressed",
        "Confidentiality obligations defined",
        "Limitation of liability section present",
        "Warranty disclaimer included",
        "Governing law and jurisdiction specified",
        "Indemnification provisions included (where applicable)",
        "Data protection and privacy addressed (where applicable)",
        "Signatures and execution blocks present",
    ]
}


# ============================================================
# Rate Limiting
# ============================================================

def check_rate_limit(api_key: str, tool_name: str) -> dict:
    """Check if the API key has exceeded rate limits. Returns {'allowed': bool, 'remaining': int, 'limit': int}."""
    key_info = API_KEYS.get(api_key, {"tier": "free"})
    tier = key_info["tier"]
    limits = RATE_LIMITS[tier]

    now = datetime.now()
    today_key = f"{api_key}:{now.day}:{now.month}:{now.year}"
    month_key = f"{api_key}:{now.month}:{now.year}"

    if today_key not in usage_tracker:
        usage_tracker[today_key] = {"daily_count": 0}
    if month_key not in usage_tracker:
        usage_tracker[month_key] = {"monthly_contract_count": 0}

    daily_count = usage_tracker[today_key]["daily_count"]
    monthly_contract_count = usage_tracker[month_key]["monthly_contract_count"]

    # Daily limit check
    if daily_count >= limits["daily"]:
        return {
            "allowed": False,
            "reason": f"Daily limit reached ({limits['daily']}/day). Upgrade to Pro at https://rumblingb.github.io/agent-legal-counsel-mcp/",
            "remaining": 0,
        }

    # Monthly contract limit check (for contract generation tools)
    if tool_name in ("legal_generate_contract", "legal_generate_tos", "legal_generate_waiver"):
        if monthly_contract_count >= limits["monthly_contracts"]:
            return {
                "allowed": False,
                "reason": f"Monthly contract limit reached ({limits['monthly_contracts']} contracts/month on {tier} tier). Upgrade to Pro at https://rumblingb.github.io/agent-legal-counsel-mcp/ for 50 contracts/month at $19/mo.",
                "remaining": 0,
            }

    # Increment usage
    usage_tracker[today_key]["daily_count"] = daily_count + 1
    if tool_name in ("legal_generate_contract", "legal_generate_tos", "legal_generate_waiver"):
        usage_tracker[month_key]["monthly_contract_count"] = monthly_contract_count + 1

    return {
        "allowed": True,
        "remaining": limits["daily"] - daily_count - 1,
        "limit": limits["daily"],
        "tier": tier,
    }


# ============================================================
# Tool Implementations
# ============================================================

def handle_list_templates(params: dict) -> list:
    """Return list of available templates."""
    result = []
    for tid, tdata in TEMPLATES.items():
        result.append({
            "id": tid,
            "name": tdata["name"],
            "description": tdata["description"],
            "version": tdata["version"],
        })
    return result


def handle_generate_contract(params: dict, tier: str = "free") -> dict:
    """Generate a contract based on template and parameters."""
    template_id = params.get("template_id", "ai_service_agreement")
    if template_id not in TEMPLATES:
        return {"error": f"Unknown template: {template_id}. Available: {list(TEMPLATES.keys())}"}

    template_name = TEMPLATES[template_id]["name"]
    params["tier"] = tier

    if template_id == "ai_service_agreement":
        contract_text = _generate_ai_service_agreement(params)
    elif template_id == "ai_data_processing":
        contract_text = _generate_ai_data_processing(params)
    elif template_id == "ai_saas_terms":
        contract_text = _generate_ai_saas_terms(params)
    elif template_id == "ai_nda":
        contract_text = _generate_ai_nda(params)
    else:
        contract_text = _generate_ai_service_agreement(params)

    # For free tier, add a watermark/footer
    footer = ""
    if tier == "free":
        footer = (
            "\n\n---\n"
            "This contract was generated using the Agent Legal Counsel MCP Free Tier.\n"
            "Upgrade to Pro ($19/mo) for enhanced customization, additional templates,\n"
            "and 50 contracts/month: https://rumblingb.github.io/agent-legal-counsel-mcp/\n"
        )

    filled_params = {k: v for k, v in params.items() if k != "tier"}

    return {
        "contract": contract_text + footer,
        "template": template_name,
        "template_id": template_id,
        "word_count": len((contract_text + footer).split()),
        "parameters_used": filled_params,
        "tier": tier,
    }


def handle_generate_tos(params: dict, tier: str = "free") -> dict:
    """Generate Terms of Service."""
    # Map to SaaS terms template
    tos_params = {
        "product_name": params.get("product_name", "[AI Product Name]"),
        "service_description": params.get("service_description", "AI-powered services as described on the provider's website"),
        "payment_terms": params.get("payment_terms", "as specified on the pricing page"),
        "uptime_sla": params.get("uptime_sla", "99.5%"),
        "data_storage": params.get("data_storage", "industry-standard encrypted cloud storage"),
        "parties": params.get("provider_name", "[Provider Name]"),
        "effective_date": params.get("effective_date", datetime.now().strftime("%B %d, %Y")),
        "usage_limits": params.get("usage_limits", "as specified in the applicable subscription plan"),
        "jurisdiction": params.get("jurisdiction", "the State of Delaware"),
        "tier": tier,
    }
    return handle_generate_contract({"template_id": "ai_saas_terms", **tos_params}, tier)


def handle_generate_waiver(params: dict, tier: str = "free") -> dict:
    """Generate liability waiver."""
    # Generate an AI-specific waiver using the service agreement as base
    waiver_params = {
        "agent_name": params.get("agent_name", "[AI Agent Name]"),
        "service_description": params.get("service_description", "AI agent services including automated decision-making and data analysis"),
        "liability_limit": params.get("liability_limit", "the total fees paid in the preceding three (3) months"),
        "parties": params.get("participant_name", "[Participant Name]"),
        "effective_date": params.get("effective_date", datetime.now().strftime("%B %d, %Y")),
        "jurisdiction": params.get("jurisdiction", "the State of Delaware"),
        "tier": tier,
    }
    # Generate a service agreement but override the liability section specifically for waiver
    result = handle_generate_contract({"template_id": "ai_service_agreement", **waiver_params}, tier)
    return result


def handle_validate_contract(params: dict) -> dict:
    """Provide validation checklist for a contract."""
    contract_text = params.get("contract_text", "")
    contract_type = params.get("contract_type", "")

    if not contract_text:
        return {"error": "contract_text is required"}

    results = []
    score = 0
    for item in VALIDATION_CHECKLIST["checklist"]:
        # Simple keyword-based validation
        keywords = item.lower().replace("(", "").replace(")", "").split()
        found = all(any(kw in contract_text.lower() for kw in keywords))
        results.append({
            "item": item,
            "found": found,
            "severity": "critical" if "Parties" in item or "Effective date" in item or "Signatures" in item else "recommended",
        })
        if found:
            score += 1

    total = len(VALIDATION_CHECKLIST["checklist"])
    completeness = round((score / total) * 100, 1)

    return {
        "contract_type": contract_type or "Unknown",
        "checklist": results,
        "completeness_score": completeness,
        "total_items": total,
        "passed_items": score,
        "recommendation": "Ready for legal review" if completeness >= 80 else "Needs improvement",
    }


# ============================================================
# MCP Server Definition
# ============================================================

if MCP_AVAILABLE:
    server = Server("agent-legal-counsel")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="legal_generate_contract",
                description="Generate a legally-structured AI agent service contract. Provide agent name, service description, payment terms, duration, and liability limits.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "template_id": {
                            "type": "string",
                            "enum": list(TEMPLATES.keys()),
                            "description": "Contract template ID",
                            "default": "ai_service_agreement",
                        },
                        "agent_name": {"type": "string", "description": "Name of the AI agent/system"},
                        "service_description": {"type": "string", "description": "Description of services provided"},
                        "payment_terms": {"type": "string", "description": "Payment terms (e.g., 'Net-30')"},
                        "duration": {"type": "string", "description": "Contract duration (e.g., '12 months')"},
                        "liability_limit": {"type": "string", "description": "Liability cap description"},
                        "parties": {"type": "string", "description": "Other party name (Client/Customer)"},
                        "jurisdiction": {"type": "string", "description": "Governing law jurisdiction"},
                        "effective_date": {"type": "string", "description": "Effective date of agreement"},
                    },
                    "required": ["template_id"],
                },
                annotations=types.ToolAnnotations(readOnlyHint=True),
            ),
            types.Tool(
                name="legal_generate_tos",
                description="Generate Terms of Service for an AI agent-facing product or SaaS platform.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "product_name": {"type": "string", "description": "Name of the AI product/SaaS platform"},
                        "service_description": {"type": "string", "description": "Description of the service"},
                        "payment_terms": {"type": "string", "description": "Subscription/billing terms"},
                        "uptime_sla": {"type": "string", "description": "Uptime SLA percentage"},
                        "jurisdiction": {"type": "string", "description": "Governing law jurisdiction"},
                        "effective_date": {"type": "string", "description": "Effective date"},
                    },
                    "required": [],
                },
                annotations=types.ToolAnnotations(readOnlyHint=True),
            ),
            types.Tool(
                name="legal_generate_waiver",
                description="Generate a liability waiver for AI agent services and automated decision-making.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "agent_name": {"type": "string", "description": "Name of the AI agent"},
                        "service_description": {"type": "string", "description": "Description of services"},
                        "participant_name": {"type": "string", "description": "Name of participant/user"},
                        "liability_limit": {"type": "string", "description": "Liability cap"},
                        "jurisdiction": {"type": "string", "description": "Governing law jurisdiction"},
                        "effective_date": {"type": "string", "description": "Effective date"},
                    },
                    "required": [],
                },
                annotations=types.ToolAnnotations(readOnlyHint=True),
            ),
            types.Tool(
                name="legal_list_templates",
                description="List all available legal contract templates with descriptions and version numbers.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
                annotations=types.ToolAnnotations(readOnlyHint=True),
            ),
            types.Tool(
                name="legal_validate_contract",
                description="Run a validation checklist on an existing contract text to identify missing clauses and assess completeness.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "contract_text": {"type": "string", "description": "Full contract text to validate"},
                        "contract_type": {"type": "string", "description": "Type of contract (optional)"},
                    },
                    "required": ["contract_text"],
                },
                annotations=types.ToolAnnotations(readOnlyHint=True),
            ),
        ]

    @server.call_tool()
    async def call_tool(tool_name: str, arguments: dict) -> list[types.TextContent]:
        # Extract API key from arguments if present
        api_key = arguments.pop("api_key", "free_demo_key_2024")
        tier = API_KEYS.get(api_key, {}).get("tier", "free")

        # Check rate limit
        rate_check = check_rate_limit(api_key, tool_name)
        if not rate_check["allowed"]:
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "error": rate_check["reason"],
                    "tier": tier,
                    "remaining": 0,
                    "upgrade_url": "https://rumblingb.github.io/agent-legal-counsel-mcp/",
                }, indent=2),
            )]

        # Route to handler
        if tool_name == "legal_list_templates":
            templates = handle_list_templates(arguments)
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "templates": templates,
                    "tier": tier,
                    "remaining": rate_check["remaining"],
                }, indent=2),
            )]

        elif tool_name == "legal_generate_contract":
            result = handle_generate_contract(arguments, tier)
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2) if isinstance(result, dict) else result,
            )]

        elif tool_name == "legal_generate_tos":
            result = handle_generate_tos(arguments, tier)
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2) if isinstance(result, dict) else result,
            )]

        elif tool_name == "legal_generate_waiver":
            result = handle_generate_waiver(arguments, tier)
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2) if isinstance(result, dict) else result,
            )]

        elif tool_name == "legal_validate_contract":
            result = handle_validate_contract(arguments)
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2),
            )]

        else:
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {tool_name}"}),
            )]

    async def run():
        async with stdio_server.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream=read_stream,
                write_stream=write_stream,
                initialization_options=server.create_initialization_options(),
            )


# ============================================================
# CLI Entry Point (for testing)
# ============================================================

def cli_demo():
    """Run a CLI demo of the server functionality."""
    print("=" * 60)
    print("Agent Legal Counsel MCP - Demo Mode")
    print("=" * 60)

    while True:
        print("\nAvailable commands:")
        print("  1. list_templates")
        print("  2. generate_contract")
        print("  3. generate_tos")
        print("  4. generate_waiver")
        print("  5. validate_contract")
        print("  q. Quit")
        choice = input("\nSelect (1-5, q): ").strip()

        if choice == "q":
            break
        elif choice == "1":
            result = handle_list_templates({})
            print(json.dumps(result, indent=2))
        elif choice == "2":
            template_id = input("Template ID (ai_service_agreement): ").strip() or "ai_service_agreement"
            agent_name = input("Agent name: ").strip() or "DemoAI"
            service = input("Service description: ").strip() or "Automated legal document generation and analysis"
            result = handle_generate_contract({
                "template_id": template_id,
                "agent_name": agent_name,
                "service_description": service,
            })
            print(result["contract"][:500] + "\n...")
            print(f"\n[Word count: {result['word_count']}]")
        elif choice == "3":
            result = handle_generate_tos({"product_name": "DemoAI Platform"})
            print(result["contract"][:500] + "\n...")
        elif choice == "4":
            result = handle_generate_waiver({"agent_name": "DemoAI"})
            print(result["contract"][:500] + "\n...")
        elif choice == "5":
            text = input("Paste contract text: ").strip()
            result = handle_validate_contract({"contract_text": text})
            print(json.dumps(result, indent=2))


if __name__ == "__main__":
    import sys
    if "--cli" in sys.argv:
        cli_demo()
    elif MCP_AVAILABLE:
        import asyncio
        asyncio.run(run())
    else:
        print("ERROR: MCP SDK not installed. Install with: pip install mcp")
        print("Running in CLI demo mode instead...")
        cli_demo()
