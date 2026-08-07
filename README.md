# Login Bypass (`sqli-auth-bypass`)

**Category:** sql injection · **Difficulty:** easy · **Points:** 200

The login form builds its query by string concatenation. Bypass authentication with a classic injection to log in as admin, whose profile page shows the key needed to XOR+base64-decode your flag blob.

## Run it

```bash
docker build -t picoclone/sqli-auth-bypass .
# `picoclone start sqli-auth-bypass` (or the web UI) prints the docker run line with your
# PICOCLONE_SERVER + PICOCLONE_INSTANCE_TOKEN
```

## Recover the flag

The delivery blob is XOR-encrypted then base64-encoded. Discover the challenge key, then invert XOR+base64.

The plaintext flag is never written to disk or served — only the encoded delivery blob
is. When you have it:

```bash
picoclone submit sqli-auth-bypass 'picoclone{...}'
```

## Hints

- The username goes straight into the SQL string.
- A tautology like ' OR '1'='1 always evaluates true.
- Log in as admin, read the key from the profile, then undo XOR+base64.
