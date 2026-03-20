# Financial API

A FastAPI-based system for validating financial transactions and detecting potential fraud in real time.

## Project Description

This API provides a simple interface to validate financial transactions and flag potentially suspicious activity. It is designed for fintech apps, banks, or any system that needs real-time transaction monitoring.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Dnyaneshsasale/financial-api.git
cd financial-api

## Example Request

POST /validate

```json
{
  "id": 1,
  "amount": 15000,
  "currency": "USD",
  "sender": "Alice",
  "receiver": "Bob"
}