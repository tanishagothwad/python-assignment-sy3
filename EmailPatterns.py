"""
=====================================================================
 EMAIL PATTERN FINDER USING REGULAR EXPRESSIONS
=====================================================================
IN PLAIN ENGLISH:
  A regular expression (regex) is a SEARCH TEMPLATE. Instead of
  looking for one exact word, we describe the SHAPE of what we want:
  "some characters, then @, then more characters, then a dot, then a
  few more characters." Python then scans the text and pulls out
  every piece that matches that shape \u2014 in this case, email addresses.
=====================================================================
"""

import re


# =====================================================================
# 1. THE EMAIL PATTERN
#    Plain English: local part + @ + domain name + . + domain suffix
# =====================================================================
EMAIL_PATTERN = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+'


# =====================================================================
# 2. FIND ALL EMAILS IN A BLOCK OF TEXT
#    Plain English: scan the whole text and collect every substring
#    that matches the email shape, wherever it appears.
# =====================================================================
def find_emails(text):
    """Returns a list of every email-shaped substring found in `text`."""
    return re.findall(EMAIL_PATTERN, text)


# =====================================================================
# 3. VALIDATE A SINGLE STRING AS AN EMAIL
#    Plain English: fullmatch requires the ENTIRE string to match the
#    pattern from start to end \u2014 useful for validating ONE address
#    typed into a form, rather than searching inside a paragraph.
# =====================================================================
def is_valid_email(candidate):
    """Returns True only if the ENTIRE string is a valid email address."""
    return re.fullmatch(EMAIL_PATTERN, candidate) is not None


# =====================================================================
# 4. DEMO / DRIVER CODE
# =====================================================================
if __name__ == "__main__":

    sample_text = """
    Please contact us for support:
    - General queries: support@examplecorp.com
    - Sales team: sales.team@business-hub.co.in
    - Personal note from Rahul (rahul_23@gmail.com) sent yesterday.
    - Invalid mentions: not-an-email, @missing-local.com, plain.text@
    - Newsletter sign-up: newsletter+promo@my-site.org
    """

    print("Original text:")
    print(sample_text)

    found = find_emails(sample_text)
    print(f"Found {len(found)} email address(es) in the text:")
    for email in found:
        print(f"  - {email}")

    print("\nValidating individual strings with is_valid_email():")
    test_cases = [
        "john.doe@example.com",
        "invalid-email",
        "user@site",
        "user@site.com",
        "plain.text@",
        "a.b-c_d+e@sub.domain.co.in",
    ]
    for candidate in test_cases:
        result = "VALID" if is_valid_email(candidate) else "INVALID"
        print(f"  {candidate:30s} -> {result}")