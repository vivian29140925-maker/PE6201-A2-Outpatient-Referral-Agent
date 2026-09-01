# PE6201 A2 — Outpatient Referral Coordination Agent

**Course:** PE6201 Emerging AI Technologies  
**Programme:** MSc Enterprise Artificial Intelligence, Nanyang Technological University  
**Assessment:** A2 — Applied AI System  
**Problem:** B — Outpatient Referral Coordination

## Overview

This project implements a **single-agent ReAct system** for coordinating outpatient referrals in a hospital setting.

The agent receives a referral, dynamically retrieves the required information using tools, evaluates the referral against clinical and operational rules, and produces one of three outcomes:

- **Book** an appropriate outpatient clinic slot
- **Request information** when a mandatory test or required information is missing
- **Escalate** the referral to a triage nurse when automated booking is unsafe or inappropriate

The system is designed around a tool-using **Reason → Act → Observe → Repeat → Final** loop, with explicit guardrails around the gated booking action.

## Problem B — Referral Coordination

The agent works with referral, patient, specialty and clinic-slot information to determine whether a referral can safely proceed.

The core workflow considers:

**Referral → Clinical Criteria → Patient → Available Slots → Booking / Request / Escalation**

The booking operation is simulated locally and does **not** interact with a real hospital or scheduling system.

## Team

| # | Team Member |
|---|---|
| 1 | GONG XINYI |
| 2 | LIU XINYAO |
| 3 | SHEN SHUO |
| 4 | SYEDYASEEN ROSHAN TUSHAR |
| 5 | XIE YULONG |
| 6 | ZHONG YINGMEI |
