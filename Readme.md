

- [x] Proper database reset
    `python manage.py migrate --run-syncdb`
- [x] properly create the registration page
- [x] hide or show the previous entris for private distraction free private writing experience
    - [x] Provide a button to toggle between the two modes
- [x] Implement search functionality through page
    - [ ] Access the search pannel only through the click of the 
    - [ ] Beautify the topbar
- [ ] Implement tags functionality through https://harvesthq.github.io/chosen/
    - [x] Implemented using bootstrap selct
    - [ ] integrate it with the tags button
    - [x] build tag list
    - [x] search through tags
    - [ ] search hrough multiple tags
- [ ] Ignore pagination and for now show the whole page for testing
    - [ ] Copy the pagination style from the rest framework pages 
    - [x] Pagination logic for number of pages
- [ ] proper location of contents like selct is not required in the base
- [ ] Make entries editable
    - [ ] Make tags and desc editable
    - [ ] Make the date editable ?? 