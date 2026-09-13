INTENTS = {
    "playback_bug": "Music/app playback technical issues — shuffle, repeat, crossfade, skip, crash, search not working, playlist inconsistencies.",
    "login_account_access": "Login failures, password reset issues, account hacked/compromised, unauthorized access.",
    "billing_subscription": "Incorrect charges, premium not activated after payment, trial/cancellation issues, student discount, family plan, refund requests.",
    "downloads_offline": "Downloaded/offline songs disappearing, device download limits.",
    "content_availability": "Specific song/album/artist missing due to licensing, or Spotify unavailable in a country/region.",
    "feature_request": "User suggesting a new feature or app improvement, not reporting a bug.",
    "resolved_positive": "Thank-you messages, confirmation that issue is resolved, no further action needed.",
}

# Which intents should default to auto-handle vs escalate to a human
ESCALATE_BY_DEFAULT = {
    "playback_bug": False,
    "login_account_access": True,   # security-sensitive, often needs account lookup via DM
    "billing_subscription": True,   # money involved, needs account-level verification
    "downloads_offline": False,
    "content_availability": False,  # usually just an informational response
    "feature_request": False,
    "resolved_positive": False,
}