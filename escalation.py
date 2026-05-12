"""
CloverBot - Slack Escalation
Sends alerts to Slack when the bot escalates to a human.
"""

import logging
import httpx

from config import Config
from database import log_escalation

logger = logging.getLogger("cloverbot.escalation")


async def escalate_to_slack(session_id, visitor_message, bot_response, lead_info=None):
    """
    Send an escalation notification to Slack.

    Args:
        session_id: The chat session ID
        visitor_message: The message that triggered escalation
        bot_response: What CloverBot replied
        lead_info: Optional dict with name/email/company
    """
    # Log to database
    await log_escalation(session_id, "visitor_request", visitor_message)

    # Skip Slack if no webhook configured
    if not Config.SLACK_WEBHOOK_URL:
        logger.warning("Slack webhook not configured -- escalation logged to DB only")
        return

    # Build the Slack message
    lead_text = ""
    if lead_info:
        parts = []
        if lead_info.get("name"):
            parts.append(f"*Name:* {lead_info['name']}")
        if lead_info.get("email"):
            parts.append(f"*Email:* {lead_info['email']}")
        if lead_info.get("company"):
            parts.append(f"*Company:* {lead_info['company']}")
        if parts:
            lead_text = "\n".join(parts) + "\n\n"

    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "[!] CloverBot Escalation",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"A visitor needs human assistance.\n\n"
                        f"{lead_text}"
                        f"*Session:* `{session_id}`\n"
                        f"*Visitor said:*\n>{visitor_message}\n\n"
                        f"*CloverBot replied:*\n>{bot_response[:500]}"
                    ),
                },
            },
            {"type": "divider"},
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Reply in the support channel or contact the visitor directly.",
                    }
                ],
            },
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(Config.SLACK_WEBHOOK_URL, json=payload)
            resp.raise_for_status()
            logger.info("[%s] Escalation sent to Slack", session_id)
    except Exception as e:
        logger.error("[%s] Failed to send Slack escalation: %s", session_id, e)
