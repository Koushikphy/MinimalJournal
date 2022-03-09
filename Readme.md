# Minimal Journal

[![Version](https://img.shields.io/badge/Web-https://minimaljournal.herokuapp.com/-success.svg)](https://minimaljournal.herokuapp.com/) 
[![Heorku](https://img.shields.io/badge/Heroku-Deployed-blue.svg?style=flat&logo=heroku)](https://minimaljournal.herokuapp.com//)
   
#### A Journal App/API based on django & django-rest-framework


**WIP**: *Work in Progress* 

### TODO:
1. - [x] Initial UI
1. - [x] Backend API
    1. - [x] User Registration/ Log In/ Log Out
    2. - [x] Entry model 
    3. - [x] DRF search
        1. - [x] Different search logic for two fields
    3. - [ ] Seperate Tags model for better performance
2. - [ ] Front end
    1. - [x] Entry list 
    2. - [x] Nav bar
    3. - [x] New entry input
    3. - [ ] Edit/Update functionality
    3. - [ ] Delete functionality
    3. - [x] Pagination for large data
        1. - [x] Long pagination problem
        1. - [x] Hide pagination on just single 
3. - [ ] Bugs
    1. - [ ] Clear tags when going to search and vice-versa
    2. - [ ] Prevent recursive databse queries
4. - [x] Implement PostgresSQL
3. - [x] Deploy to heroku
4. - [ ] Front end React - Next JS
5. - [ ] Encrypt the backend storage so that all entries are secured
