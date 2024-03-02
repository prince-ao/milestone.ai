# Milestone.ai Architecture

## Introduction

### Purpose of document
The purpose of this document is to describe the design and architecture of milestone.ai.

### Vision Statement
Around 2021 Kristi Brescia decided to create a document that displayed what
classes students should take at each semester of college and what extra-curricular
activities they should engage in, in order to increase their career readiness. This
document turned out to be successful. The goal of this application is to build upon
this document and make it more interactive. Students will not able be able to view
this static document, but interact with it by asking it questions and getting
individualized responses.

### Features of the application
- Users will get their personalized graduation milestone box
- User will be able to interact with a chatbot as the adviser

### Scope of the application


#### Must have
- Home page
- Info form
  - Graduation date
  - Number of credits
- Generate relevant milestone table
- Interactive chatbot
  - RAG

#### Should have

#### Could have
- User authentication
- Message saving

#### Wont have

### Architecture Goals
- Implement all necessary features
- Make all user interactions smooth and "reactive"
- Generate accurate llm responses
- Make application as dynamic

## Technology Stack

### Frontend layer
- html (structure)
- htmx (backend glue)
- tailwindcss (styling)
- alpine.js ("reactivity")

### Backend layer
- python (language)
- flask (framework)
- langchain (RAG)
- OpenAI (AI utils) (external api)

### Database layer
- sqlite (relational data)
- milvus (semantic data)

## Vector Database Design
- Purpose: the purpose of the vector database will store the contents of the gitbook.
  This will better aid the llm(large language model) response.
- Data source: https://csi-cs-department.gitbook.io/internship-handbook/sitemap.xml

- Collections
  - gitbook_data
    - refresh_rate := (based on last mod)

## Relational Database Design

### Tables

#### Admins
- id INT PRIMARY KEY
- username VARCHAR(30) NOT NULL UNIQUE
- email VARCHAR(255)
- password VARCHAR(200) NOT NULL // hash

## Backend Routes

### View

#### GET /
- home page: `<insert wireframe>`
  - description: display information basic about application, button to go to the form

#### GET /get-to-know-you
- form page: `<insert wireframe>`
  - description: form to get information, reactively move through the form, transition
  animations

#### GET /confirmation
- confirmation page: `<insert wireframe>`
  - description: will display the user's respective degree milestone map
  - optional: each actionable row might have a checkbox, this will give us information
  to what the user has done already
  - note: this can be added to `/get-to-know-you`

#### GET /chat
- chat page: `<insert wireframe>`
  - description: displays final personalized degree milestone map, 

#### GET /admin/login
- login page for admin: `<insert wireframe>`
  - description: allows admin to login, master login

#### GET /admin
- admin page: `<insert wireframe>`
  - description: allows user to update milestone map, allows admin to add or remove account,
  allows admin to set other admin permissions
  - redirects: `/admin/login` if not logged in

### Api

#### POST /get-to-know-you
  - description: handles view form
  - request:
    - body: (form)

## Other
