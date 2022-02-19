plan:
- hardcode creation of initial competition
- frontend assumes one competition (for now)
- don't worry too much about non-admin users + voting just yet, keep in back of mind

---

- [ ] admin users:
    - [x] exist
    - [x] look diff in UI
    - [ ] can create drawings

- [ ] datamodels for:

    - [ ] drawing
        - id - int (PKEY, AUTOINC)
        - title - string
        - description - string
        - author_id - int
        - uploaded - date
        - created - date
        - metadata - JSON

    - [ ] competition
        - title - string (PKEY)
        - external_url - string
        - start_date - date
        - end_date - date

    - [ ] competition_category
        - title - string (PKEY, COMP)
        - description - string
        - competition_title - string (PKEY, COMP)
        - hidden - boolean

    - [ ] vote
        - ...
