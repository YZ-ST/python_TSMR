Taiwan High Speed Rail Ticket Booking System
============================================

Introduction
------------

This project integrates a mobile application with a Line Bot to facilitate the booking of Taiwan High Speed Rail tickets. It leverages a web crawler to fetch ticket information, which is then communicated back to the user through the bot.

Features
--------

*   **Line Bot Integration**: Users can interact with the system through a Line Bot, making the process more accessible and user-friendly.
*   **Web Crawling**: Utilizes a sophisticated web crawler to scrape the latest ticket information from the Taiwan High Speed Rail website.
*   **Dynamic Rendering**: Handles dynamic content on the web pages to ensure accurate and up-to-date ticket information.

Technical Implementation
------------------------

1.  **Feadper Crawling Framework**: An efficient and robust framework used for web scraping.
2.  **Line Bot**: A chatbot interface on the popular LINE messaging platform for interaction with users.
3.  **AWS (Amazon Web Services)**: Cloud services used for hosting the application and managing the backend infrastructure.
4.  **Ubuntu**: The operating system chosen for its reliability and compatibility with various software requirements.
5.  **Dynamic Rendering**: A technique to process and render the dynamically loaded content on web pages, crucial for accurate web scraping.

How to Use
----------

1.  **Start the Line Bot**: Users start by interacting with the Line Bot.
2.  **Enter Travel Details**: Users input their travel preferences such as date, time, and destination.
3.  **Ticket Information**: The bot triggers the crawler, which fetches the relevant ticket information.
4.  **Receive Ticket Info**: The bot then sends back the ticket information, including booking details and availability.

Future Enhancements
-------------------

*   **Payment Integration**: Implementing a secure payment gateway for completing ticket purchases.
*   **Real-time Updates**: Providing real-time updates and notifications about ticket availability and prices.
