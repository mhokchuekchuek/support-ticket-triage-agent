---
id: kb_041
title: Security and Two-Factor Authentication
category: account
keywords:
  - security
  - 2FA
  - two-factor
  - authentication
  - password
  - session
  - secure
  - MFA
---

## Two-Factor Authentication (2FA)

### Why Enable 2FA?
- Adds extra security layer beyond password
- Protects against unauthorized access
- Required for some organization accounts
- Industry best practice

### Setting Up 2FA

#### Authenticator App (Recommended)
1. Go to **Settings > Security > Two-Factor Authentication**
2. Click **Enable 2FA**
3. Choose **Authenticator App**
4. Scan QR code with your app:
   - Google Authenticator
   - Authy
   - 1Password
   - Microsoft Authenticator
5. Enter 6-digit code to verify
6. Save your backup codes securely

#### SMS (Less Secure)
1. Go to Settings > Security > 2FA
2. Choose **SMS**
3. Enter phone number
4. Verify with code sent via text
5. Save backup codes

**Note**: SMS is less secure due to SIM swapping risks. Authenticator app recommended.

### Backup Codes
- 10 single-use codes provided at setup
- Store securely (password manager, printed, safe)
- Each code works once
- Generate new codes if running low (invalidates old ones)

### Disabling 2FA
1. Go to Settings > Security > 2FA
2. Click **Disable 2FA**
3. Enter current 2FA code to confirm
4. Re-enable recommended if disabled temporarily

## Password Security

### Password Requirements
- Minimum 8 characters
- Mix of uppercase and lowercase
- At least one number
- At least one special character
- Cannot be a commonly used password

### Changing Your Password
1. Settings > Security > Password
2. Enter current password
3. Enter new password (twice)
4. All other sessions logged out

### Password Reset
If you forgot your password:
1. Click "Forgot Password" on login
2. Enter email address
3. Check inbox for reset link
4. Link expires in 24 hours

## Session Management

### Active Sessions
View all logged-in sessions:
- Settings > Security > Sessions
- See device, location, last active
- Identify unrecognized sessions

### Ending Sessions
- **Single session**: Click "End" next to session
- **All sessions**: Click "End All Sessions"
- Current session remains active

### Session Timeout
- Default: 30 days of inactivity
- Admins can set stricter policies
- Enterprise: Configurable per workspace

## Security Alerts

### Automatic Alerts
You'll be notified of:
- New device/browser login
- Password changes
- 2FA changes
- Login from new location
- Multiple failed login attempts

### Responding to Alerts
If you didn't perform the action:
1. Change password immediately
2. End all sessions
3. Review 2FA settings
4. Contact support if compromised

## Enterprise Security Features

### SSO/SAML
- Single Sign-On with identity provider
- Supported providers: Okta, Azure AD, OneLogin, etc.
- Contact sales for setup

### SCIM Provisioning
- Automatic user provisioning/deprovisioning
- Sync with identity provider
- Enterprise plan only

### Advanced Audit Logs
- Detailed activity logging
- Export for compliance
- Retention based on plan

### IP Allowlisting
- Restrict access to specific IPs
- VPN-compatible
- Enterprise plan only

## Security Best Practices

1. **Use unique password** for this account
2. **Enable 2FA** with authenticator app
3. **Review sessions** regularly
4. **Use password manager** for secure storage
5. **Don't share credentials** with others
6. **Verify emails** are from our domain
7. **Report suspicious activity** immediately

## Reporting Security Issues

Found a vulnerability?
- Email: security@example.com
- Bug bounty program available
- Responsible disclosure appreciated
