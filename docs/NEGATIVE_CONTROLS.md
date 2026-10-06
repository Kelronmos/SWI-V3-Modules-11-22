# Negative Controls (V3-0002)

These must be actively blocked:

| Shortcut                                      | Required Response |
|-----------------------------------------------|-------------------|
| timestamp → authority                         | BLOCK             |
| conversation continuity → authority           | BLOCK             |
| sensor observation → authority                | BLOCK             |
| hardware capability → permission              | BLOCK             |
| runtime match → authorization                 | BLOCK             |
| previous approval → new authorization         | BLOCK             |
| CI green → production authorization           | BLOCK             |
| AFTER state → retroactive authorization       | BLOCK             |
| temporary memory → durable authorization      | BLOCK             |

Any implementation that permits the above is non-compliant with V3-0002.
