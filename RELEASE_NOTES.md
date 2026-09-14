---
name: v1.2.0

body: |
  Add Wagtail 7.0 LTS and CodeRed CMS 6 support while keeping existing tested stacks.

  - Version 1.2.0 widens declared ranges to wagtail>=4.2,<8 and coderedcms>=2.1,<7.
  - New tested environments: py312-wagtail70-crx6 (locked and floating).
  - Existing Wagtail 4.2 / 5.2 / 6.3 and CodeRed CMS 2–5 cells remain in tox and CI.
  - Nested CRX layout blocks still collect assets; BaseLayoutBlock is imported optionally with a StreamValue fallback.

draft: true
prerelease: false
