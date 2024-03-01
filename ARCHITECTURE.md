# Milestone.ai Architecture

## Introduction

### Purpose of document
The purpose of this document is to describe the design and architecture of milestone.ai.

### Vision Statement
Around 2021 Kristi Brescia decided to create a document that displayed what
classes students should take at each semester of college and what extra-curricular
activities they should engage in, in order to increase their career readiness. This
document turned out to be successful and various colleges across CUNY decided to
copy it. The goal of this application is to build upon this document and make it
more interactive. Students will not able be able to view this static document,
but interact with it by asking it questions and getting individualized responses.

### Features of the application
- Users will get their personalized graduation milestone box
- User will be able to interact with a chatbot as the adviser

### Scope of the application


#### Must have
- Intro page
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
- postgresql (relational data)
- milvus (semantic data)

## Vector Database Design
- Purpose: the purpose of the vector database will store the contents of the gitbook.
  This will better aid the llm(large language model) response.

- Collections
  - gitbook data

## Backend Routes

## Other
